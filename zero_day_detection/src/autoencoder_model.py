"""
Phase 1 Autoencoder Model for Zero-Day Detection
Trains on Normal class data and uses reconstruction error for anomaly detection
"""

import numpy as np
import json
import os
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


class AutoencoderModel:
    """
    Autoencoder for anomaly detection in network traffic
    Trained only on Normal class data
    """
    
    def __init__(self, input_dim=None, encoding_dim=8):
        """
        Initialize autoencoder
        
        Args:
            input_dim: Number of input features
            encoding_dim: Dimension of bottleneck layer
        """
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.model = None
        self.threshold = None
        self.history = None
        
    def build_model(self, input_dim):
        """
        Build symmetric encoder-decoder architecture
        
        Args:
            input_dim: Number of input features
        """
        self.input_dim = input_dim
        
        # Encoder
        encoder_input = layers.Input(shape=(input_dim,))
        encoded = layers.Dense(64, activation='relu')(encoder_input)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        encoded = layers.Dense(32, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        encoded = layers.Dense(16, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        
        # Bottleneck
        bottleneck = layers.Dense(self.encoding_dim, activation='relu', name='bottleneck')(encoded)
        
        # Decoder (symmetric)
        decoded = layers.Dense(16, activation='relu')(bottleneck)
        decoded = layers.BatchNormalization()(decoded)
        
        decoded = layers.Dense(32, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        decoded = layers.Dense(64, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        # Output layer
        decoder_output = layers.Dense(input_dim, activation='linear')(decoded)
        
        # Build model
        self.model = models.Model(encoder_input, decoder_output)
        
        # Compile
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        print(f"\n{'='*60}")
        print("Autoencoder Architecture")
        print(f"{'='*60}")
        self.model.summary()
        
        return self.model
    
    def train(self, X_train, X_val=None, epochs=100, batch_size=256, verbose=1):
        """
        Train autoencoder on normal data
        
        Args:
            X_train: Training data (normal class only)
            X_val: Validation data (optional)
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Verbosity level
        """
        if self.model is None:
            self.build_model(X_train.shape[1])
        
        # Split validation if not provided
        if X_val is None:
            X_train, X_val = train_test_split(X_train, test_size=0.2, random_state=42)
        
        print(f"\n{'='*60}")
        print("Training Autoencoder on Normal Class Data")
        print(f"{'='*60}")
        print(f"Training samples: {X_train.shape[0]:,}")
        print(f"Validation samples: {X_val.shape[0]:,}")
        print(f"Features: {X_train.shape[1]}")
        
        # Callbacks
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        )
        
        # Train (autoencoder reconstructs input, so X is both input and target)
        self.history = self.model.fit(
            X_train, X_train,
            validation_data=(X_val, X_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, reduce_lr],
            verbose=verbose
        )
        
        print(f"\n✓ Training complete!")
        print(f"Final training loss: {self.history.history['loss'][-1]:.6f}")
        print(f"Final validation loss: {self.history.history['val_loss'][-1]:.6f}")
        
        return self.history
    
    def calculate_threshold(self, X_normal, method='statistical', percentile=95, k=3):
        """
        Calculate threshold for anomaly detection
        
        Args:
            X_normal: Normal class data for threshold calculation
            method: 'statistical' (mean + k*std) or 'percentile'
            percentile: Percentile for percentile method (default 95)
            k: Number of standard deviations for statistical method (default 3)
        
        Returns:
            threshold: Reconstruction error threshold
        """
        # Calculate reconstruction errors
        reconstructions = self.model.predict(X_normal, verbose=0)
        errors = np.mean(np.square(X_normal - reconstructions), axis=1)
        
        if method == 'statistical':
            mean_error = np.mean(errors)
            std_error = np.std(errors)
            self.threshold = mean_error + k * std_error
            print(f"\n{'='*60}")
            print("Threshold Calculation (Statistical Method)")
            print(f"{'='*60}")
            print(f"Mean reconstruction error: {mean_error:.6f}")
            print(f"Std reconstruction error: {std_error:.6f}")
            print(f"Threshold (mean + {k}*std): {self.threshold:.6f}")
        
        elif method == 'percentile':
            self.threshold = np.percentile(errors, percentile)
            print(f"\n{'='*60}")
            print("Threshold Calculation (Percentile Method)")
            print(f"{'='*60}")
            print(f"{percentile}th percentile: {self.threshold:.6f}")
        
        else:
            raise ValueError("Method must be 'statistical' or 'percentile'")
        
        # Calculate coverage
        normal_flagged = np.sum(errors > self.threshold)
        coverage = (1 - normal_flagged / len(errors)) * 100
        print(f"Normal samples above threshold: {normal_flagged}/{len(errors)} ({100-coverage:.2f}%)")
        print(f"Coverage on normal data: {coverage:.2f}%")
        
        return self.threshold, errors
    
    def predict_anomaly(self, X):
        """
        Predict anomalies based on reconstruction error
        
        Args:
            X: Input data
        
        Returns:
            predictions: Binary array (1 = anomaly, 0 = normal)
            errors: Reconstruction errors
        """
        if self.threshold is None:
            raise ValueError("Threshold not set. Call calculate_threshold() first.")
        
        # Calculate reconstruction errors
        reconstructions = self.model.predict(X, verbose=0)
        errors = np.mean(np.square(X - reconstructions), axis=1)
        
        # Flag anomalies
        predictions = (errors > self.threshold).astype(int)
        
        return predictions, errors
    
    def save_model(self, model_path='models/autoencoder_phase1.h5', 
                   threshold_path='models/autoencoder_threshold.json'):
        """
        Save trained model and threshold
        
        Args:
            model_path: Path to save model
            threshold_path: Path to save threshold metadata
        """
        # Create directory if needed
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model
        self.model.save(model_path)
        print(f"\n✓ Model saved to: {model_path}")
        
        # Save threshold and metadata
        metadata = {
            'threshold': float(self.threshold),
            'input_dim': int(self.input_dim),
            'encoding_dim': int(self.encoding_dim)
        }
        
        with open(threshold_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✓ Threshold saved to: {threshold_path}")
    
    def load_model(self, model_path='models/autoencoder_phase1.h5',
                   threshold_path='models/autoencoder_threshold.json'):
        """
        Load trained model and threshold
        
        Args:
            model_path: Path to model file
            threshold_path: Path to threshold metadata
        """
        # Load model
        self.model = keras.models.load_model(model_path)
        print(f"\n✓ Model loaded from: {model_path}")
        
        # Load threshold
        with open(threshold_path, 'r') as f:
            metadata = json.load(f)
        
        self.threshold = metadata['threshold']
        self.input_dim = metadata['input_dim']
        self.encoding_dim = metadata['encoding_dim']
        
        print(f"✓ Threshold loaded: {self.threshold:.6f}")
        print(f"✓ Input dimension: {self.input_dim}")
        print(f"✓ Encoding dimension: {self.encoding_dim}")
    
    def plot_training_history(self, save_path='results/autoencoder_training_loss.png'):
        """
        Plot training history
        
        Args:
            save_path: Path to save plot
        """
        if self.history is None:
            print("No training history available")
            return
        
        plt.figure(figsize=(12, 4))
        
        # Loss plot
        plt.subplot(1, 2, 1)
        plt.plot(self.history.history['loss'], label='Training Loss')
        plt.plot(self.history.history['val_loss'], label='Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('MSE Loss')
        plt.title('Autoencoder Training Loss')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # MAE plot
        plt.subplot(1, 2, 2)
        plt.plot(self.history.history['mae'], label='Training MAE')
        plt.plot(self.history.history['val_mae'], label='Validation MAE')
        plt.xlabel('Epoch')
        plt.ylabel('MAE')
        plt.title('Mean Absolute Error')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Training plot saved to: {save_path}")
        plt.close()
    
    def plot_reconstruction_errors(self, errors_normal, errors_attack=None,
                                   save_path='results/autoencoder_reconstruction_errors.png'):
        """
        Plot reconstruction error distribution
        
        Args:
            errors_normal: Reconstruction errors for normal samples
            errors_attack: Reconstruction errors for attack samples (optional)
            save_path: Path to save plot
        """
        plt.figure(figsize=(12, 5))
        
        # Histogram
        plt.subplot(1, 2, 1)
        plt.hist(errors_normal, bins=50, alpha=0.7, label='Normal', color='blue', edgecolor='black')
        if errors_attack is not None:
            plt.hist(errors_attack, bins=50, alpha=0.7, label='Attack', color='red', edgecolor='black')
        
        if self.threshold is not None:
            plt.axvline(self.threshold, color='green', linestyle='--', linewidth=2, label='Threshold')
        
        plt.xlabel('Reconstruction Error (MSE)')
        plt.ylabel('Frequency')
        plt.title('Reconstruction Error Distribution')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Box plot
        plt.subplot(1, 2, 2)
        data_to_plot = [errors_normal]
        labels = ['Normal']
        
        if errors_attack is not None:
            data_to_plot.append(errors_attack)
            labels.append('Attack')
        
        plt.boxplot(data_to_plot, labels=labels)
        
        if self.threshold is not None:
            plt.axhline(self.threshold, color='green', linestyle='--', linewidth=2, label='Threshold')
            plt.legend()
        
        plt.ylabel('Reconstruction Error (MSE)')
        plt.title('Reconstruction Error Box Plot')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Save
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Reconstruction error plot saved to: {save_path}")
        plt.close()


if __name__ == "__main__":
    # Quick test
    print("Autoencoder Model Module")
    print("=" * 60)
    print("This module provides the AutoencoderModel class for Phase 1 anomaly detection")
    print("\nUsage:")
    print("  from src.autoencoder_model import AutoencoderModel")
    print("  model = AutoencoderModel(encoding_dim=8)")
    print("  model.train(X_normal)")
    print("  model.calculate_threshold(X_normal)")
    print("  predictions, errors = model.predict_anomaly(X_test)")
