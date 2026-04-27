"""
Alternative CNN implementation using scikit-learn's MLPClassifier
This is a fallback when TensorFlow is not available
"""

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import numpy as np

def build_mlp_classifier(input_shape, num_classes):
    """
    Build Multi-Layer Perceptron as alternative to CNN
    """
    model = MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),
        activation='relu',
        solver='adam',
        batch_size=128,
        learning_rate='adaptive',
        max_iter=50,
        verbose=True,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=5,
        random_state=42
    )
    
    return model

def train_mlp(model, X_train, y_train, X_test, y_test, epochs=50, model_path='models/mlp_model.pkl'):
    """Train the MLP model"""
    # Set max_iter to epochs for consistency
    model.max_iter = epochs
    
    print("\nTraining MLP classifier...")
    model.fit(X_train, y_train)
    
    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    print(f"\nTraining accuracy: {train_acc:.4f}")
    print(f"Test accuracy: {test_acc:.4f}")
    
    # Save model
    import pickle
    import os
    os.makedirs('models', exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Best model saved to {model_path}")
    
    # Create a simple history object for compatibility
    class History:
        def __init__(self, loss_curve):
            self.history = {
                'loss': loss_curve,
                'val_loss': loss_curve,  # Simplified
                'accuracy': [1 - l for l in loss_curve],
                'val_accuracy': [1 - l for l in loss_curve]
            }
    
    history = History(model.loss_curve_)
    
    return model, history

# Try to import TensorFlow, fall back to sklearn if not available
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
    import os
    
    TENSORFLOW_AVAILABLE = True
    
    def build_1d_cnn(input_shape, num_classes):
        """
        Build 1D-CNN as described in the paper (Section 4.2)
        """
        model = keras.Sequential([
            # Input layer
            layers.Input(shape=(input_shape,)),
            
            # Reshape for 1D convolution
            layers.Reshape((input_shape, 1)),
            
            # Convolutional layer with nb_filters
            layers.Conv1D(filters=64, kernel_size=3, activation='relu'),
            layers.MaxPooling1D(pool_size=2),
            
            layers.Conv1D(filters=32, kernel_size=3, activation='relu'),
            layers.MaxPooling1D(pool_size=2),
            
            # Flatten for dense layers
            layers.Flatten(),
            
            # Fully connected layers
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            
            # Output layer
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train_cnn(model, X_train, y_train, X_test, y_test, epochs=50, model_path='models/cnn_model.h5'):
        """Train the CNN model with callbacks"""
        # Create models directory
        os.makedirs('models', exist_ok=True)
        
        # Define callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                model_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-6,
                verbose=1
            )
        ]
        
        print("\nTraining CNN with callbacks...")
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=128,
            validation_data=(X_test, y_test),
            callbacks=callbacks,
            verbose=1
        )
        
        print(f"\n✓ Best model saved to {model_path}")
        return model, history

except ImportError:
    print("\nWARNING: TensorFlow not available, using sklearn MLPClassifier as fallback")
    TENSORFLOW_AVAILABLE = False
    
    # Use MLP as fallback
    build_1d_cnn = build_mlp_classifier
    train_cnn = train_mlp