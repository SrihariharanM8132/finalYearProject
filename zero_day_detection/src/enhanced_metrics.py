"""
Enhanced Evaluation Metrics Module
Provides comprehensive model evaluation with precision, recall, F1-score, and ROC-AUC
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_curve, auc, roc_auc_score,
    classification_report, precision_recall_curve
)
import os


class EnhancedMetrics:
    """Calculate and visualize comprehensive evaluation metrics"""
    
    def __init__(self, results_dir='results'):
        self.results_dir = results_dir
        os.makedirs(f"{results_dir}/plots", exist_ok=True)
        os.makedirs(f"{results_dir}/metrics", exist_ok=True)
    
    def calculate_detailed_metrics(self, y_true, y_pred, y_proba=None, class_names=None):
        """
        Calculate precision, recall, F1-score for each class
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Prediction probabilities (optional, for ROC-AUC)
            class_names: List of class names
            
        Returns:
            dict: Dictionary containing all metrics
        """
        # Multi-class metrics
        precision_micro = precision_score(y_true, y_pred, average='micro', zero_division=0)
        precision_macro = precision_score(y_true, y_pred, average='macro', zero_division=0)
        precision_weighted = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        
        recall_micro = recall_score(y_true, y_pred, average='micro', zero_division=0)
        recall_macro = recall_score(y_true, y_pred, average='macro', zero_division=0)
        recall_weighted = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        
        f1_micro = f1_score(y_true, y_pred, average='micro', zero_division=0)
        f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)
        f1_weighted = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Per-class metrics
        precision_per_class = precision_score(y_true, y_pred, average=None, zero_division=0)
        recall_per_class = recall_score(y_true, y_pred, average=None, zero_division=0)
        f1_per_class = f1_score(y_true, y_pred, average=None, zero_division=0)
        
        metrics = {
            'precision_micro': precision_micro,
            'precision_macro': precision_macro,
            'precision_weighted': precision_weighted,
            'recall_micro': recall_micro,
            'recall_macro': recall_macro,
            'recall_weighted': recall_weighted,
            'f1_micro': f1_micro,
            'f1_macro': f1_macro,
            'f1_weighted': f1_weighted,
            'precision_per_class': precision_per_class,
            'recall_per_class': recall_per_class,
            'f1_per_class': f1_per_class
        }
        
        # Add ROC-AUC if probabilities provided
        if y_proba is not None:
            try:
                roc_auc = roc_auc_score(y_true, y_proba, multi_class='ovr', average='weighted')
                metrics['roc_auc_weighted'] = roc_auc
            except:
                metrics['roc_auc_weighted'] = None
        
        return metrics
    
    def create_metrics_table(self, metrics_dict, class_names, save_path=None):
        """
        Create a detailed metrics table
        
        Args:
            metrics_dict: Dictionary of metrics from calculate_detailed_metrics
            class_names: List of class names
            save_path: Path to save CSV
            
        Returns:
            DataFrame: Metrics table
        """
        # Create per-class table
        data = {
            'Class': class_names,
            'Precision': metrics_dict['precision_per_class'],
            'Recall': metrics_dict['recall_per_class'],
            'F1-Score': metrics_dict['f1_per_class']
        }
        
        df = pd.DataFrame(data)
        
        # Add average rows
        avg_row = pd.DataFrame({
            'Class': ['Micro Average'],
            'Precision': [metrics_dict['precision_micro']],
            'Recall': [metrics_dict['recall_micro']],
            'F1-Score': [metrics_dict['f1_micro']]
        })
        
        macro_row = pd.DataFrame({
            'Class': ['Macro Average'],
            'Precision': [metrics_dict['precision_macro']],
            'Recall': [metrics_dict['recall_macro']],
            'F1-Score': [metrics_dict['f1_macro']]
        })
        
        weighted_row = pd.DataFrame({
            'Class': ['Weighted Average'],
            'Precision': [metrics_dict['precision_weighted']],
            'Recall': [metrics_dict['recall_weighted']],
            'F1-Score': [metrics_dict['f1_weighted']]
        })
        
        df = pd.concat([df, avg_row, macro_row, weighted_row], ignore_index=True)
        
        if save_path is None:
            save_path = f"{self.results_dir}/metrics/detailed_metrics.csv"
        
        df.to_csv(save_path, index=False)
        print(f"✓ Detailed metrics saved to {save_path}")
        
        return df
    
    def plot_metrics_comparison(self, metrics_dict, class_names, save_path=None):
        """Plot precision, recall, and F1-score comparison"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        x = np.arange(len(class_names))
        width = 0.25
        
        precision = metrics_dict['precision_per_class']
        recall = metrics_dict['recall_per_class']
        f1 = metrics_dict['f1_per_class']
        
        ax.bar(x - width, precision, width, label='Precision', color='#3498db', edgecolor='black')
        ax.bar(x, recall, width, label='Recall', color='#2ecc71', edgecolor='black')
        ax.bar(x + width, f1, width, label='F1-Score', color='#e74c3c', edgecolor='black')
        
        ax.set_xlabel('Attack Class', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=12, fontweight='bold')
        ax.set_title('Precision, Recall, and F1-Score by Class', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(class_names, rotation=45, ha='right')
        ax.legend(fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, 1.1)
        
        # Add value labels
        for i, (p, r, f) in enumerate(zip(precision, recall, f1)):
            ax.text(i - width, p + 0.02, f'{p:.2f}', ha='center', va='bottom', fontsize=8)
            ax.text(i, r + 0.02, f'{r:.2f}', ha='center', va='bottom', fontsize=8)
            ax.text(i + width, f + 0.02, f'{f:.2f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/metrics_comparison.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Metrics comparison saved to {save_path}")
        plt.close()
    
    def plot_roc_curves(self, models_dict, X_test, y_test, class_names, save_path=None):
        """
        Plot ROC curves for multiple models
        
        Args:
            models_dict: Dictionary of {model_name: model}
            X_test: Test features
            y_test: Test labels
            class_names: List of class names
            save_path: Path to save plot
        """
        n_classes = len(class_names)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = sns.color_palette("husl", len(models_dict))
        
        for idx, (model_name, model) in enumerate(models_dict.items()):
            try:
                # Get prediction probabilities
                if hasattr(model, 'predict_proba'):
                    y_proba = model.predict_proba(X_test)
                else:
                    continue
                
                # Calculate ROC AUC (micro-average)
                from sklearn.preprocessing import label_binarize
                y_test_bin = label_binarize(y_test, classes=range(n_classes))
                
                fpr, tpr, _ = roc_curve(y_test_bin.ravel(), y_proba.ravel())
                roc_auc = auc(fpr, tpr)
                
                ax.plot(fpr, tpr, color=colors[idx], lw=2,
                       label=f'{model_name} (AUC = {roc_auc:.3f})')
            except Exception as e:
                print(f"Could not plot ROC for {model_name}: {e}")
                continue
        
        ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate', fontsize=12, fontweight='bold')
        ax.set_ylabel('True Positive Rate', fontsize=12, fontweight='bold')
        ax.set_title('ROC Curves - Multi-Model Comparison', fontsize=14, fontweight='bold')
        ax.legend(loc="lower right", fontsize=10)
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/roc_curves.png"
        
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ ROC curves saved to {save_path}")
        plt.close()
    
    def print_classification_report(self, y_true, y_pred, class_names):
        """Print detailed classification report"""
        print("\n" + "="*80)
        print("DETAILED CLASSIFICATION REPORT")
        print("="*80)
        report = classification_report(y_true, y_pred, target_names=class_names, 
                                      zero_division=0, digits=4)
        print(report)
        print("="*80 + "\n")
        
        return report


def print_metrics_summary(metrics_dict):
    """Print a formatted summary of metrics"""
    print("\n" + "="*80)
    print("COMPREHENSIVE METRICS SUMMARY")
    print("="*80)
    print(f"Precision (Weighted): {metrics_dict['precision_weighted']:.4f}")
    print(f"Recall (Weighted):    {metrics_dict['recall_weighted']:.4f}")
    print(f"F1-Score (Weighted):  {metrics_dict['f1_weighted']:.4f}")
    
    if 'roc_auc_weighted' in metrics_dict and metrics_dict['roc_auc_weighted'] is not None:
        print(f"ROC-AUC (Weighted):   {metrics_dict['roc_auc_weighted']:.4f}")
    
    print("="*80)
    print(f"Precision (Macro):    {metrics_dict['precision_macro']:.4f}")
    print(f"Recall (Macro):       {metrics_dict['recall_macro']:.4f}")
    print(f"F1-Score (Macro):     {metrics_dict['f1_macro']:.4f}")
    print("="*80 + "\n")
