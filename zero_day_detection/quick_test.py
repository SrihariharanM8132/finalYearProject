print("="*60)
print("QUICK TEST - 2 MINUTE VALIDATION")
print("="*60)

import warnings
warnings.filterwarnings('ignore')

# Test 1: Imports
print("\n[1/5] Testing imports...")
try:
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    print("✓ All libraries imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    exit(1)

# Test 2: Load data
print("\n[2/5] Loading dataset...")
try:
    from src.load_data import load_nsl_kdd
    df = load_nsl_kdd('data/KDDTrain+.txt')
    print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# Test 3: Feature engineering
print("\n[3/5] Testing feature engineering...")
try:
    from src.feature_engineering import (feature_engineering, encode_categorical, 
                                         create_labels, normalize_data)
    
    # Use small sample for speed
    df_sample = df.sample(n=1000, random_state=42)
    df_sample = feature_engineering(df_sample)
    df_sample = create_labels(df_sample)
    df_sample = encode_categorical(df_sample)
    
    print(f"✓ Feature engineering complete: {df_sample.shape[1]} features")
except Exception as e:
    print(f"✗ Feature engineering error: {e}")
    exit(1)

# Test 4: Model creation
print("\n[4/5] Testing CNN model creation...")
try:
    from src.cnn_model import build_1d_cnn
    
    X_sample = df_sample.drop(['attack_type', 'attack_category'], axis=1)
    y_sample = LabelEncoder().fit_transform(df_sample['attack_category'])
    
    model = build_1d_cnn(X_sample.shape[1], len(np.unique(y_sample)))
    print(f"✓ CNN model created")
    print(f"  Input shape: {X_sample.shape[1]}")
    print(f"  Output classes: {len(np.unique(y_sample))}")
except Exception as e:
    print(f"✗ Model creation error: {e}")
    exit(1)

# Test 5: Quick training (1 epoch)
print("\n[5/5] Testing training (1 epoch)...")
try:
    X_train, X_test, y_train, y_test = train_test_split(
        X_sample, y_sample, test_size=0.2, random_state=42
    )
    
    X_train_norm, X_test_norm, scaler = normalize_data(X_train, X_test)
    
    history = model.fit(X_train_norm, y_train, epochs=1, verbose=0, batch_size=32)
    
    loss = history.history['loss'][0]
    print(f"✓ Training works! Loss: {loss:.4f}")
except Exception as e:
    print(f"✗ Training error: {e}")
    exit(1)

print("\n" + "="*60)
print("✅ ALL TESTS PASSED!")
print("="*60)
print("\nYour setup is working perfectly!")
print("\nNext step: Run the full pipeline")
print("Command: python main_simple.py")