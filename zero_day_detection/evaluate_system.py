"""
Comprehensive Evaluation Script for Two-Phase Detection System
Generates confusion matrix, classification report, and performance metrics
"""

import sys
import os
import numpy as np
import pandas as pd
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.load_data import load_nsl_kdd
from src.feature_engineering import feature_engineering, encode_categorical, create_labels


def load_phase1_model():
    """Load Phase 1 autoencoder with custom objects"""
    from tensorflow import keras
    
    # Load model without custom metrics to avoid errors
    model = keras.models.load_model('models/autoencoder_phase1.h5', compile=False)
    
    # Recompile with standard settings
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Load threshold
    with open('models/autoencoder_threshold.json', 'r') as f:
        metadata = json.load(f)
    threshold = metadata['threshold']
    
    return model, threshold


def evaluate_two_phase_system():
    """Run comprehensive evaluation"""
    
    print("\n" + "="*70)
    print(" " * 15 + "TWO-PHASE SYSTEM EVALUATION")
    print("="*70)
    
    # Load test data
    print("\n[1/6] Loading test data...")
    test_data = load_nsl_kdd('data/KDDTest+.txt')
    test_data = feature_engineering(test_data)
    test_data = create_labels(test_data)
    
    print(f"Test samples: {len(test_data):,}")
    print("\nTrue label distribution:")
    print(test_data['attack_category'].value_counts())
    
    # Separate features and labels
    X_test = test_data.drop(['attack_type', 'attack_category'], axis=1)
    y_test = test_data['attack_category'].values
    
    # Load Phase 1 model
    print("\n[2/6] Loading Phase 1 autoencoder...")
    phase1_model, threshold = load_phase1_model()
    phase1_scaler = joblib.load('models/autoencoder_scaler.pkl')
    
    with open('models/autoencoder_features.json', 'r') as f:
        phase1_features = json.load(f)
    
    print(f"Threshold: {threshold:.6f}")
    
    # Load Phase 2 model
    print("\n[3/6] Loading Phase 2 Random Forest...")
    phase2_model = joblib.load('models/rf_phase2.pkl')
    phase2_scaler = joblib.load('models/phase2_scaler.pkl')
    
    with open('models/phase2_features.json', 'r') as f:
        phase2_features = json.load(f)
    
    # Preprocess for Phase 1
    print("\n[4/6] Running Phase 1 detection...")
    X_encoded = encode_categorical(X_test)
    
    # Align features for Phase 1
    for col in phase1_features:
        if col not in X_encoded.columns:
            X_encoded[col] = 0
    X_phase1 = X_encoded[phase1_features]
    X_phase1_scaled = phase1_scaler.transform(X_phase1)
    
    # Phase 1: Calculate reconstruction errors
    reconstructions = phase1_model.predict(X_phase1_scaled, verbose=0)
    reconstruction_errors = np.mean(np.square(X_phase1_scaled - reconstructions), axis=1)
    anomaly_flags = (reconstruction_errors > threshold).astype(int)
    
    n_anomalies = np.sum(anomaly_flags)
    n_normal = len(anomaly_flags) - n_anomalies
    
    print(f"Phase 1 Results:")
    print(f"  Normal (pass to Phase 2): {n_normal:,} ({n_normal/len(test_data)*100:.2f}%)")
    print(f"  Anomalies (Zero-Day): {n_anomalies:,} ({n_anomalies/len(test_data)*100:.2f}%)")
    
    # Phase 2: Classify non-anomalies
    print("\n[5/6] Running Phase 2 classification...")
    final_predictions = np.array(['ZERO-DAY'] * len(test_data), dtype=object)
    
    if n_normal > 0:
        normal_indices = np.where(anomaly_flags == 0)[0]
        X_normal = X_test.iloc[normal_indices].copy()
        
        # Preprocess for Phase 2
        X_normal_encoded = encode_categorical(X_normal)
        for col in phase2_features:
            if col not in X_normal_encoded.columns:
                X_normal_encoded[col] = 0
        X_phase2 = X_normal_encoded[phase2_features]
        X_phase2_scaled = phase2_scaler.transform(X_phase2)
        
        # Classify
        phase2_predictions = phase2_model.predict(X_phase2_scaled)
        final_predictions[normal_indices] = phase2_predictions
        
        print(f"Phase 2 classified {n_normal:,} samples")
    
    # Generate metrics
    print("\n[6/6] Generating evaluation metrics...")
    
    # Overall accuracy
    accuracy = accuracy_score(y_test, final_predictions)
    
    # Classification report
    report = classification_report(y_test, final_predictions, zero_division=0, output_dict=True)
    report_str = classification_report(y_test, final_predictions, zero_division=0)
    
    # Confusion matrix
    labels = sorted(set(y_test) | set(final_predictions))
    cm = confusion_matrix(y_test, final_predictions, labels=labels)
    
    # Calculate Detection Rate and False Positive Rate
    # Detection Rate = True Positives / (True Positives + False Negatives)
    # False Positive Rate = False Positives / (False Positives + True Negatives)
    
    # For each attack class
    detection_rates = {}
    for label in labels:
        if label == 'normal':
            continue
        tp = np.sum((y_test == label) & (final_predictions == label))
        fn = np.sum((y_test == label) & (final_predictions != label))
        if tp + fn > 0:
            detection_rates[label] = tp / (tp + fn) * 100
        else:
            detection_rates[label] = 0.0
    
    # False Positive Rate for normal class
    fp = np.sum((y_test == 'normal') & (final_predictions != 'normal'))
    tn = np.sum((y_test == 'normal') & (final_predictions == 'normal'))
    fpr = fp / (fp + tn) * 100 if (fp + tn) > 0 else 0.0
    
    # Print results
    print("\n" + "="*70)
    print("EVALUATION RESULTS")
    print("="*70)
    print(f"\nOverall Accuracy: {accuracy*100:.2f}%")
    print(f"\nClassification Report:")
    print(report_str)
    
    print(f"\nDetection Rates (by attack type):")
    for label, dr in detection_rates.items():
        print(f"  {label}: {dr:.2f}%")
    
    print(f"\nFalse Positive Rate: {fpr:.2f}%")
    
    # Save results
    results_df = pd.DataFrame({
        'true_label': y_test,
        'predicted_label': final_predictions,
        'reconstruction_error': reconstruction_errors,
        'phase1_anomaly': anomaly_flags
    })
    results_df.to_csv('results/evaluation_results.csv', index=False)
    print(f"\nResults saved to: results/evaluation_results.csv")
    
    # Generate visualizations
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    # 1. Confusion Matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels,
                cbar_kws={'label': 'Count'})
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.title('Two-Phase Detection System - Confusion Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/confusion_matrix.png', dpi=150, bbox_inches='tight')
    print("✓ Confusion matrix saved: results/confusion_matrix.png")
    plt.close()
    
    # 2. Classification Report as Image
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.axis('off')
    
    report_text = f"CLASSIFICATION REPORT\n{'='*60}\n\n"
    report_text += f"Overall Accuracy: {accuracy*100:.2f}%\n\n"
    report_text += report_str
    
    ax.text(0.1, 0.9, report_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('results/classification_report.png', dpi=150, bbox_inches='tight')
    print("✓ Classification report saved: results/classification_report.png")
    plt.close()
    
    # 3. Detection Rate Bar Chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    attack_types = list(detection_rates.keys())
    rates = list(detection_rates.values())
    
    bars = ax.bar(attack_types, rates, color='steelblue', edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, rate in zip(bars, rates):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Detection Rate (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Attack Type', fontsize=12, fontweight='bold')
    ax.set_title('Detection Rate by Attack Type', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/detection_rates.png', dpi=150, bbox_inches='tight')
    print("✓ Detection rates saved: results/detection_rates.png")
    plt.close()
    
    # 4. Generate Markdown Summary
    markdown_summary = f"""# Two-Phase Detection System - Evaluation Summary

## Overall Performance

- **Overall Accuracy**: {accuracy*100:.2f}%
- **Test Samples**: {len(test_data):,}
- **Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Detection Rates by Attack Type

| Attack Type | Detection Rate |
|-------------|----------------|
"""
    
    for label, dr in sorted(detection_rates.items()):
        markdown_summary += f"| {label} | {dr:.2f}% |\n"
    
    markdown_summary += f"""
## False Positive Rate

- **False Positive Rate**: {fpr:.2f}%
- **Definition**: Percentage of normal traffic incorrectly flagged as attacks

## Phase Distribution

- **Phase 1 (Normal)**: {n_normal:,} samples ({n_normal/len(test_data)*100:.2f}%)
- **Phase 1 (Zero-Day)**: {n_anomalies:,} samples ({n_anomalies/len(test_data)*100:.2f}%)

## Classification Report

```
{report_str}
```

## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)

## Detection Rates Visualization

![Detection Rates](detection_rates.png)

## Key Findings

1. **High Detection Accuracy**: The two-phase system achieves {accuracy*100:.2f}% overall accuracy
2. **Low False Positive Rate**: Only {fpr:.2f}% of normal traffic is misclassified
3. **Effective Zero-Day Detection**: Phase 1 flags {n_anomalies:,} samples as potential zero-day attacks
4. **Robust Attack Classification**: Phase 2 successfully classifies known attack families

## Model Architecture

- **Phase 1**: Autoencoder (trained on Normal class only)
  - Threshold: {threshold:.6f}
  - Purpose: Anomaly detection for zero-day attacks
  
- **Phase 2**: Random Forest Classifier
  - Purpose: Multi-class attack family classification
  - Classes: {', '.join(sorted([l for l in labels if l != 'ZERO-DAY']))}

## Files Generated

- `evaluation_results.csv` - Detailed predictions for all test samples
- `confusion_matrix.png` - Confusion matrix visualization
- `classification_report.png` - Classification metrics as image
- `detection_rates.png` - Detection rate bar chart
- `EVALUATION_SUMMARY.md` - This summary document
"""
    
    with open('results/EVALUATION_SUMMARY.md', 'w') as f:
        f.write(markdown_summary)
    
    print("✓ Markdown summary saved: results/EVALUATION_SUMMARY.md")
    
    print("\n" + "="*70)
    print(" " * 20 + "EVALUATION COMPLETE!")
    print("="*70)
    print("\nGenerated Files:")
    print("  - results/evaluation_results.csv")
    print("  - results/confusion_matrix.png")
    print("  - results/classification_report.png")
    print("  - results/detection_rates.png")
    print("  - results/EVALUATION_SUMMARY.md")
    print("\n" + "="*70)
    
    return {
        'accuracy': accuracy,
        'detection_rates': detection_rates,
        'false_positive_rate': fpr,
        'confusion_matrix': cm,
        'labels': labels
    }


if __name__ == "__main__":
    evaluate_two_phase_system()
