"""
Two-Phase Zero-Day Detection Pipeline
Integrates Phase 1 (Autoencoder) and Phase 2 (Random Forest) for comprehensive intrusion detection

Pipeline Flow:
1. Input traffic -> Phase 1 Autoencoder
2. If reconstruction error > threshold -> Flag as ZERO-DAY
3. If reconstruction error <= threshold -> Phase 2 Random Forest -> Classify attack family
"""

import sys
import os
import numpy as np
import pandas as pd
import json
import joblib

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.load_data import load_nsl_kdd
from src.feature_engineering import feature_engineering, encode_categorical, create_labels
from src.autoencoder_model import AutoencoderModel
from src.attack_classifier import AttackClassifier


class TwoPhaseDetector:
    """
    Integrated two-phase detection system
    Phase 1: Autoencoder for zero-day detection
    Phase 2: Random Forest for attack classification
    """
    
    def __init__(self):
        self.phase1_model = None
        self.phase2_model = None
        self.phase1_scaler = None
        self.phase2_scaler = None
        self.phase1_features = None
        self.phase2_features = None
        
    def load_models(self):
        """Load both phase models and preprocessing artifacts"""
        print("\n" + "="*60)
        print("LOADING TWO-PHASE DETECTION SYSTEM")
        print("="*60)
        
        # Load Phase 1 (Autoencoder)
        print("\n[Phase 1] Loading autoencoder...")
        self.phase1_model = AutoencoderModel()
        self.phase1_model.load_model(
            model_path='models/autoencoder_phase1.h5',
            threshold_path='models/autoencoder_threshold.json'
        )
        
        self.phase1_scaler = joblib.load('models/autoencoder_scaler.pkl')
        print("✓ Phase 1 scaler loaded")
        
        with open('models/autoencoder_features.json', 'r') as f:
            self.phase1_features = json.load(f)
        print(f"✓ Phase 1 features loaded: {len(self.phase1_features)}")
        
        # Load Phase 2 (Random Forest)
        print("\n[Phase 2] Loading Random Forest classifier...")
        self.phase2_model = AttackClassifier()
        self.phase2_model.load_model('models/rf_phase2.pkl')
        
        self.phase2_scaler = joblib.load('models/phase2_scaler.pkl')
        print("✓ Phase 2 scaler loaded")
        
        with open('models/phase2_features.json', 'r') as f:
            self.phase2_features = json.load(f)
        print(f"✓ Phase 2 features loaded: {len(self.phase2_features)}")
        
        print("\n✓ All models loaded successfully!")
    
    def preprocess_for_phase1(self, df):
        """Preprocess data for Phase 1"""
        # Encode categorical
        df_encoded = encode_categorical(df)
        
        # Align columns with training features
        for col in self.phase1_features:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        df_encoded = df_encoded[self.phase1_features]
        
        # Scale
        X_scaled = self.phase1_scaler.transform(df_encoded)
        
        return X_scaled
    
    def preprocess_for_phase2(self, df):
        """Preprocess data for Phase 2"""
        # Encode categorical
        df_encoded = encode_categorical(df)
        
        # Align columns with training features
        for col in self.phase2_features:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        
        df_encoded = df_encoded[self.phase2_features]
        
        # Scale
        X_scaled = self.phase2_scaler.transform(df_encoded)
        
        return X_scaled
    
    def detect(self, df):
        """
        Run two-phase detection pipeline
        
        Args:
            df: Input dataframe with network traffic features
        
        Returns:
            results: DataFrame with detection results
        """
        print("\n" + "="*60)
        print("RUNNING TWO-PHASE DETECTION PIPELINE")
        print("="*60)
        print(f"Input samples: {len(df):,}")
        
        # Phase 1: Anomaly detection
        print("\n[Phase 1] Running autoencoder anomaly detection...")
        X_phase1 = self.preprocess_for_phase1(df.copy())
        
        anomaly_flags, reconstruction_errors = self.phase1_model.predict_anomaly(X_phase1)
        
        n_anomalies = np.sum(anomaly_flags)
        n_normal = len(anomaly_flags) - n_anomalies
        
        print(f"✓ Phase 1 complete")
        print(f"  Normal (pass to Phase 2): {n_normal:,} ({n_normal/len(df)*100:.2f}%)")
        print(f"  Anomalies (Zero-Day): {n_anomalies:,} ({n_anomalies/len(df)*100:.2f}%)")
        
        # Phase 2: Attack classification for non-anomalies
        print("\n[Phase 2] Classifying non-anomalous traffic...")
        
        final_predictions = np.array(['ZERO-DAY'] * len(df), dtype=object)
        
        if n_normal > 0:
            # Get indices of normal samples
            normal_indices = np.where(anomaly_flags == 0)[0]
            
            # Preprocess for Phase 2
            df_normal = df.iloc[normal_indices].copy()
            X_phase2 = self.preprocess_for_phase2(df_normal)
            
            # Classify
            phase2_predictions = self.phase2_model.predict(X_phase2)
            
            # Update final predictions
            final_predictions[normal_indices] = phase2_predictions
            
            print(f"✓ Phase 2 complete")
            print(f"  Classified {n_normal:,} samples")
            
            # Show Phase 2 distribution
            unique, counts = np.unique(phase2_predictions, return_counts=True)
            print(f"\n  Phase 2 Classification:")
            for cls, cnt in zip(unique, counts):
                print(f"    {cls}: {cnt:,} ({cnt/len(phase2_predictions)*100:.2f}%)")
        
        # Create results dataframe
        results = pd.DataFrame({
            'reconstruction_error': reconstruction_errors,
            'phase1_anomaly': anomaly_flags,
            'final_prediction': final_predictions
        })
        
        print("\n" + "="*60)
        print("DETECTION COMPLETE")
        print("="*60)
        print(f"\nFinal Detection Summary:")
        unique, counts = np.unique(final_predictions, return_counts=True)
        for cls, cnt in zip(unique, counts):
            print(f"  {cls}: {cnt:,} ({cnt/len(final_predictions)*100:.2f}%)")
        
        return results
    
    def evaluate(self, df, true_labels):
        """
        Evaluate two-phase system with ground truth
        
        Args:
            df: Input dataframe
            true_labels: Ground truth labels
        
        Returns:
            metrics: Evaluation metrics
        """
        # Run detection
        results = self.detect(df)
        
        # Add true labels
        results['true_label'] = true_labels
        
        # Calculate metrics
        print("\n" + "="*60)
        print("EVALUATION METRICS")
        print("="*60)
        
        # Zero-day detection metrics
        print("\n[Zero-Day Detection Performance]")
        
        # Consider attacks not in training as zero-day candidates
        # For NSL-KDD, we can use this as a proxy
        true_zero_day = results['phase1_anomaly']
        pred_zero_day = (results['final_prediction'] == 'ZERO-DAY').astype(int)
        
        from sklearn.metrics import classification_report, confusion_matrix
        
        # Overall classification
        print("\n[Overall Classification Performance]")
        print(classification_report(results['true_label'], results['final_prediction'], zero_division=0))
        
        # Save results
        results.to_csv('results/two_phase_results.csv', index=False)
        print("\n✓ Results saved to: results/two_phase_results.csv")
        
        return results


def main():
    """Main driver script"""
    print("\n" + "="*70)
    print(" " * 15 + "TWO-PHASE ZERO-DAY DETECTION SYSTEM")
    print("="*70)
    print("\nPhase 1: Autoencoder (Anomaly Detection -> Zero-Day)")
    print("Phase 2: Random Forest (Attack Classification -> DoS/Probe/R2L/U2R)")
    print("="*70)
    
    # Initialize detector
    detector = TwoPhaseDetector()
    
    # Load models
    detector.load_models()
    
    # Load test data
    print("\n" + "="*60)
    print("LOADING TEST DATA")
    print("="*60)
    
    test_data = load_nsl_kdd('data/KDDTest+.txt')
    test_data = feature_engineering(test_data)
    test_data = create_labels(test_data)
    
    print(f"\nTest data loaded: {len(test_data):,} samples")
    print(f"\nTrue label distribution:")
    print(test_data['attack_category'].value_counts())
    
    # Separate features and labels
    X_test = test_data.drop(['attack_type', 'attack_category'], axis=1)
    y_test = test_data['attack_category']
    
    # Run evaluation
    results = detector.evaluate(X_test, y_test)
    
    # Generate visualizations
    print("\n" + "="*60)
    print("GENERATING VISUALIZATIONS")
    print("="*60)
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # 1. Reconstruction error distribution by true label
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Box plot
    results_plot = results.copy()
    results_plot = results_plot[results_plot['reconstruction_error'] < results_plot['reconstruction_error'].quantile(0.99)]
    
    ax = axes[0]
    results_plot.boxplot(column='reconstruction_error', by='true_label', ax=ax)
    ax.axhline(detector.phase1_model.threshold, color='red', linestyle='--', linewidth=2, label='Threshold')
    ax.set_xlabel('True Label')
    ax.set_ylabel('Reconstruction Error')
    ax.set_title('Reconstruction Error by Attack Type')
    ax.legend()
    plt.suptitle('')
    
    # Histogram
    ax = axes[1]
    for label in results['true_label'].unique()[:5]:  # Top 5 classes
        data = results[results['true_label'] == label]['reconstruction_error']
        ax.hist(data, bins=30, alpha=0.5, label=label)
    
    ax.axvline(detector.phase1_model.threshold, color='red', linestyle='--', linewidth=2, label='Threshold')
    ax.set_xlabel('Reconstruction Error')
    ax.set_ylabel('Frequency')
    ax.set_title('Reconstruction Error Distribution')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('results/two_phase_reconstruction_analysis.png', dpi=150, bbox_inches='tight')
    print("✓ Reconstruction analysis saved to: results/two_phase_reconstruction_analysis.png")
    plt.close()
    
    # 2. Confusion matrix
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(results['true_label'], results['final_prediction'])
    labels = sorted(results['true_label'].unique())
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=labels, yticklabels=labels, cbar_kws={'label': 'Count'})
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.title('Two-Phase System - Confusion Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/two_phase_confusion_matrix.png', dpi=150, bbox_inches='tight')
    print("✓ Confusion matrix saved to: results/two_phase_confusion_matrix.png")
    plt.close()
    
    # 3. Detection flow diagram
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Total\nSamples', 'Phase 1\nNormal', 'Phase 1\nZero-Day']
    counts = [
        len(results),
        np.sum(results['phase1_anomaly'] == 0),
        np.sum(results['phase1_anomaly'] == 1)
    ]
    colors = ['steelblue', 'green', 'red']
    
    bars = ax.bar(categories, counts, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count:,}\n({count/len(results)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Number of Samples', fontsize=12)
    ax.set_title('Two-Phase Detection Flow', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('results/two_phase_flow.png', dpi=150, bbox_inches='tight')
    print("✓ Detection flow saved to: results/two_phase_flow.png")
    plt.close()
    
    print("\n" + "="*70)
    print(" " * 20 + "PIPELINE COMPLETE!")
    print("="*70)
    print("\nGenerated Files:")
    print("  - results/two_phase_results.csv")
    print("  - results/two_phase_reconstruction_analysis.png")
    print("  - results/two_phase_confusion_matrix.png")
    print("  - results/two_phase_flow.png")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
