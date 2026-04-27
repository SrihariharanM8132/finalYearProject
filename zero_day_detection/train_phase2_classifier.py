"""
Training Script for Phase 2 Random Forest Classifier
Trains on labeled attack data (DoS, Probe, R2L, U2R)
"""

import sys
import os
import numpy as np
import pandas as pd

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.load_data import load_nsl_kdd
from src.feature_engineering import feature_engineering, encode_categorical, create_labels, normalize_data
from src.attack_classifier import AttackClassifier


def main():
    print("\n" + "="*60)
    print("PHASE 2: RANDOM FOREST CLASSIFIER TRAINING")
    print("Training on Labeled Attack Data")
    print("="*60)
    
    # 1. Load data
    print("\n[Step 1/6] Loading NSL-KDD data...")
    train_data = load_nsl_kdd('data/KDDTrain+.txt')
    test_data = load_nsl_kdd('data/KDDTest+.txt')
    
    # 2. Feature engineering
    print("\n[Step 2/6] Applying feature engineering...")
    train_data = feature_engineering(train_data)
    train_data = create_labels(train_data)
    
    test_data = feature_engineering(test_data)
    test_data = create_labels(test_data)
    
    # 3. Separate features and labels
    print("\n[Step 3/6] Preparing training data...")
    
    X_train = train_data.drop(['attack_type', 'attack_category'], axis=1)
    y_train = train_data['attack_category']
    
    X_test = test_data.drop(['attack_type', 'attack_category'], axis=1)
    y_test = test_data['attack_category']
    
    # 4. Encode categorical features
    print("\n[Step 4/6] Encoding categorical features...")
    X_train_encoded = encode_categorical(X_train)
    X_test_encoded = encode_categorical(X_test, reference_df=X_train_encoded)
    
    # 5. Normalize
    print("\n[Step 5/6] Normalizing features...")
    X_train_scaled, X_test_scaled, scaler = normalize_data(
        X_train_encoded.values,
        X_test_encoded.values
    )
    
    print(f"Training shape: {X_train_scaled.shape}")
    print(f"Test shape: {X_test_scaled.shape}")
    
    # 6. Train classifier
    print("\n[Step 6/6] Training Random Forest classifier...")
    
    classifier = AttackClassifier(n_estimators=100, max_depth=20, random_state=42)
    classifier.train(X_train_scaled, y_train.values)
    
    # 7. Evaluate on test data
    print("\n[Step 7/7] Evaluating on test data...")
    metrics = classifier.evaluate(X_test_scaled, y_test.values)
    
    # Plot confusion matrix
    classifier.plot_confusion_matrix(
        metrics['confusion_matrix'],
        classifier.classes,
        save_path='results/phase2_confusion_matrix.png'
    )
    
    # Plot feature importance
    classifier.plot_feature_importance(
        list(X_train_encoded.columns),
        top_n=20,
        save_path='results/phase2_feature_importance.png'
    )
    
    # 8. Save model
    print("\n[Step 8/8] Saving model and artifacts...")
    classifier.save_model('models/rf_phase2.pkl')
    
    # Save scaler
    import joblib
    joblib.dump(scaler, 'models/phase2_scaler.pkl')
    print("✓ Scaler saved to: models/phase2_scaler.pkl")
    
    # Save feature columns
    import json
    feature_cols = list(X_train_encoded.columns)
    with open('models/phase2_features.json', 'w') as f:
        json.dump(feature_cols, f, indent=2)
    print("✓ Feature columns saved to: models/phase2_features.json")
    
    # Save evaluation metrics
    results_df = pd.DataFrame({
        'True_Label': y_test.values,
        'Predicted_Label': metrics['predictions']
    })
    results_df.to_csv('results/phase2_predictions.csv', index=False)
    print("✓ Predictions saved to: results/phase2_predictions.csv")
    
    print("\n" + "="*60)
    print("PHASE 2 TRAINING COMPLETE!")
    print("="*60)
    print(f"✓ Model: models/rf_phase2.pkl")
    print(f"✓ Test accuracy: {metrics['accuracy']*100:.2f}%")
    print(f"✓ Classes: {list(classifier.classes)}")
    print("\nNext step: Run two_phase_pipeline.py for integrated detection")
    print("="*60)


if __name__ == "__main__":
    main()
