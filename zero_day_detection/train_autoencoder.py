"""
Training Script for Phase 1 Autoencoder
Trains autoencoder on Normal class data from NSL-KDD dataset
"""

import sys
import os
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.load_data import load_nsl_kdd
from src.feature_engineering import feature_engineering, encode_categorical, create_labels, normalize_data
from src.autoencoder_model import AutoencoderModel


def main():
    print("\n" + "="*60)
    print("PHASE 1: AUTOENCODER TRAINING")
    print("Training on Normal Class Data Only")
    print("="*60)
    
    # 1. Load training data
    print("\n[Step 1/6] Loading NSL-KDD training data...")
    train_data = load_nsl_kdd('data/KDDTrain+.txt')
    
    # 2. Feature engineering
    print("\n[Step 2/6] Applying feature engineering...")
    train_data = feature_engineering(train_data)
    train_data = create_labels(train_data)
    
    # 3. Filter only Normal class
    print("\n[Step 3/6] Filtering Normal class samples...")
    print(f"Total training samples: {len(train_data):,}")
    print(f"\nClass distribution:")
    print(train_data['attack_category'].value_counts())
    
    normal_data = train_data[train_data['attack_category'] == 'normal'].copy()
    print(f"\nNormal class samples: {len(normal_data):,}")
    
    if len(normal_data) == 0:
        print("ERROR: No normal samples found!")
        return
    
    # 4. Encode and normalize
    print("\n[Step 4/6] Encoding and normalizing features...")
    
    # Separate features and labels
    X_normal = normal_data.drop(['attack_type', 'attack_category'], axis=1)
    
    # Encode categorical features
    X_normal_encoded = encode_categorical(X_normal)
    
    # Normalize
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_normal_scaled = scaler.fit_transform(X_normal_encoded)
    
    print(f"Feature shape: {X_normal_scaled.shape}")
    print(f"Features: {X_normal_scaled.shape[1]}")
    
    # 5. Train autoencoder
    print("\n[Step 5/6] Training autoencoder...")
    
    autoencoder = AutoencoderModel(encoding_dim=8)
    autoencoder.build_model(input_dim=X_normal_scaled.shape[1])
    
    history = autoencoder.train(
        X_normal_scaled,
        epochs=100,
        batch_size=256,
        verbose=1
    )
    
    # Plot training history
    autoencoder.plot_training_history('results/autoencoder_training_loss.png')
    
    # 6. Calculate threshold
    print("\n[Step 6/6] Calculating anomaly detection threshold...")
    
    # Use statistical method: mean + 3*std (99.7% confidence)
    threshold, errors = autoencoder.calculate_threshold(
        X_normal_scaled,
        method='statistical',
        k=3
    )
    
    # Plot reconstruction errors
    autoencoder.plot_reconstruction_errors(
        errors,
        save_path='results/autoencoder_reconstruction_errors_train.png'
    )
    
    # 7. Save model
    print("\n[Step 7/7] Saving model and threshold...")
    autoencoder.save_model(
        model_path='models/autoencoder_phase1.h5',
        threshold_path='models/autoencoder_threshold.json'
    )
    
    # Save scaler for later use
    import joblib
    joblib.dump(scaler, 'models/autoencoder_scaler.pkl')
    print("✓ Scaler saved to: models/autoencoder_scaler.pkl")
    
    # Save feature columns for consistency
    feature_cols = list(X_normal_encoded.columns)
    import json
    with open('models/autoencoder_features.json', 'w') as f:
        json.dump(feature_cols, f, indent=2)
    print("✓ Feature columns saved to: models/autoencoder_features.json")
    
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"✓ Model: models/autoencoder_phase1.h5")
    print(f"✓ Threshold: {threshold:.6f}")
    print(f"✓ Input features: {X_normal_scaled.shape[1]}")
    print(f"✓ Encoding dimension: 8")
    print("\nNext step: Run evaluate_autoencoder.py to test on test data")
    print("="*60)


if __name__ == "__main__":
    main()
