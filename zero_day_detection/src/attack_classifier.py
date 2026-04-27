"""
Phase 2 Random Forest Classifier for Attack Family Classification
Classifies attacks into specific families: DoS, Probe, R2L, U2R
"""

import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns


class AttackClassifier:
    """
    Random Forest classifier for attack family classification
    Trained on labeled attack data (DoS, Probe, R2L, U2R)
    """
    
    def __init__(self, n_estimators=100, max_depth=20, random_state=42):
        """
        Initialize Random Forest classifier
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum depth of trees
            random_state: Random seed
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1,
            verbose=1
        )
        self.classes = None
        
    def train(self, X_train, y_train):
        """
        Train Random Forest on attack data
        
        Args:
            X_train: Training features
            y_train: Training labels (attack categories)
        """
        print(f"\n{'='*60}")
        print("Training Phase 2 Random Forest Classifier")
        print(f"{'='*60}")
        print(f"Training samples: {X_train.shape[0]:,}")
        print(f"Features: {X_train.shape[1]}")
        
        # Get class distribution
        unique, counts = np.unique(y_train, return_counts=True)
        print(f"\nClass distribution:")
        for cls, cnt in zip(unique, counts):
            print(f"  {cls}: {cnt:,} ({cnt/len(y_train)*100:.2f}%)")
        
        # Train
        print("\nTraining Random Forest...")
        self.model.fit(X_train, y_train)
        self.classes = self.model.classes_
        
        # Training accuracy
        train_pred = self.model.predict(X_train)
        train_acc = accuracy_score(y_train, train_pred)
        
        print(f"\n✓ Training complete!")
        print(f"Training accuracy: {train_acc*100:.2f}%")
        
        return self.model
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate classifier on test data
        
        Args:
            X_test: Test features
            y_test: Test labels
        
        Returns:
            metrics: Dictionary of evaluation metrics
        """
        print(f"\n{'='*60}")
        print("Evaluating Phase 2 Classifier")
        print(f"{'='*60}")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"\nTest accuracy: {accuracy*100:.2f}%")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred, labels=self.classes)
        
        metrics = {
            'accuracy': accuracy,
            'predictions': y_pred,
            'confusion_matrix': cm,
            'classification_report': classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        }
        
        return metrics
    
    def predict(self, X):
        """
        Predict attack families
        
        Args:
            X: Input features
        
        Returns:
            predictions: Predicted attack categories
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """
        Predict attack family probabilities
        
        Args:
            X: Input features
        
        Returns:
            probabilities: Prediction probabilities for each class
        """
        return self.model.predict_proba(X)
    
    def save_model(self, model_path='models/rf_phase2.pkl'):
        """
        Save trained model
        
        Args:
            model_path: Path to save model
        """
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.model, model_path)
        print(f"\n✓ Phase 2 model saved to: {model_path}")
    
    def load_model(self, model_path='models/rf_phase2.pkl'):
        """
        Load trained model
        
        Args:
            model_path: Path to model file
        """
        self.model = joblib.load(model_path)
        self.classes = self.model.classes_
        print(f"\n✓ Phase 2 model loaded from: {model_path}")
        print(f"✓ Classes: {list(self.classes)}")
    
    def plot_confusion_matrix(self, cm, classes, save_path='results/phase2_confusion_matrix.png'):
        """
        Plot confusion matrix
        
        Args:
            cm: Confusion matrix
            classes: Class labels
            save_path: Path to save plot
        """
        plt.figure(figsize=(10, 8))
        
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=classes,
            yticklabels=classes,
            cbar_kws={'label': 'Count'}
        )
        
        plt.xlabel('Predicted Label', fontsize=12)
        plt.ylabel('True Label', fontsize=12)
        plt.title('Phase 2 Random Forest - Confusion Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to: {save_path}")
        plt.close()
    
    def plot_feature_importance(self, feature_names, top_n=20, save_path='results/phase2_feature_importance.png'):
        """
        Plot feature importance
        
        Args:
            feature_names: List of feature names
            top_n: Number of top features to show
            save_path: Path to save plot
        """
        importances = self.model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        plt.figure(figsize=(10, 8))
        plt.barh(range(top_n), importances[indices], color='steelblue', edgecolor='black')
        plt.yticks(range(top_n), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.title(f'Top {top_n} Feature Importances - Phase 2 Random Forest', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"✓ Feature importance plot saved to: {save_path}")
        plt.close()


if __name__ == "__main__":
    # Quick test
    print("Attack Classifier Module (Phase 2)")
    print("=" * 60)
    print("This module provides the AttackClassifier class for Phase 2 attack classification")
    print("\nUsage:")
    print("  from src.attack_classifier import AttackClassifier")
    print("  classifier = AttackClassifier(n_estimators=100)")
    print("  classifier.train(X_train, y_train)")
    print("  predictions = classifier.predict(X_test)")
