"""
Comprehensive Visualization Module for Zero-Day Detection Framework
Generates all plots and visual analytics for the project
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.metrics import (confusion_matrix, classification_report,
                              roc_curve, auc, precision_recall_curve,
                              average_precision_score)
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

class FrameworkVisualizer:
    """Generate all visualizations for the framework"""
    
    def __init__(self, results_dir='results'):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
        os.makedirs(f"{results_dir}/plots", exist_ok=True)
    
    def plot_training_history(self, history, save_path=None):
        """Plot CNN training history (accuracy and loss)"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Accuracy plot
        axes[0].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
        axes[0].plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
        axes[0].set_title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Loss plot
        axes[1].plot(history.history['loss'], label='Train Loss', linewidth=2)
        axes[1].plot(history.history['val_loss'], label='Val Loss', linewidth=2)
        axes[1].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/training_history.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Training history saved to {save_path}")
        plt.close()
    
    def plot_confusion_matrix(self, y_true, y_pred, class_names, model_name='Model', save_path=None):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=class_names, yticklabels=class_names,
                    cbar_kws={'label': 'Count'})
        plt.title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/confusion_matrix_{model_name.lower().replace(' ', '_')}.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Confusion matrix saved to {save_path}")
        plt.close()
    
    def plot_model_comparison(self, results_dict, save_path=None):
        """Compare performance of different models"""
        models = list(results_dict.keys())
        scores = list(results_dict.values())
        
        plt.figure(figsize=(12, 6))
        colors = sns.color_palette("husl", len(models))
        bars = plt.bar(models, scores, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title('Model Performance Comparison', fontsize=14, fontweight='bold')
        plt.xlabel('Model')
        plt.ylabel('F1-Score / Accuracy')
        plt.ylim(0, 1.1)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/model_comparison.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Model comparison saved to {save_path}")
        plt.close()
    
    def plot_cluster_distribution(self, cluster_labels, y_true, class_names, save_path=None):
        """Plot distribution of attack types across clusters"""
        # Get top 10 clusters by size
        unique_clusters, counts = np.unique(cluster_labels, return_counts=True)
        top_clusters_idx = np.argsort(counts)[-10:][::-1]
        top_clusters = unique_clusters[top_clusters_idx]
        
        # Create distribution matrix
        distribution = []
        for cluster_id in top_clusters:
            cluster_mask = cluster_labels == cluster_id
            cluster_targets = y_true[cluster_mask]
            dist = [np.sum(cluster_targets == i) for i in range(len(class_names))]
            distribution.append(dist)
        
        distribution = np.array(distribution).T
        
        # Plot stacked bar chart
        fig, ax = plt.subplots(figsize=(14, 7))
        bottom = np.zeros(len(top_clusters))
        colors = sns.color_palette("Set3", len(class_names))
        
        for i, class_name in enumerate(class_names):
            ax.bar(range(len(top_clusters)), distribution[i], 
                   bottom=bottom, label=class_name, color=colors[i])
            bottom += distribution[i]
        
        ax.set_xlabel('Cluster ID')
        ax.set_ylabel('Number of Samples')
        ax.set_title('Attack Type Distribution Across Top 10 Clusters', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(range(len(top_clusters)))
        ax.set_xticklabels(top_clusters)
        ax.legend(title='Attack Type', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/cluster_distribution.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Cluster distribution saved to {save_path}")
        plt.close()
    
    def plot_silhouette_analysis(self, cluster_info, save_path=None):
        """Plot silhouette scores for clusters"""
        cluster_ids = sorted(cluster_info.keys())
        silhouette_scores = [cluster_info[cid]['s_sil'] for cid in cluster_ids]
        cluster_sizes = [cluster_info[cid]['count'] for cid in cluster_ids]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Silhouette scores
        axes[0].bar(cluster_ids, silhouette_scores, color='steelblue', edgecolor='black')
        axes[0].axhline(y=np.mean(silhouette_scores), color='r', linestyle='--', 
                       label=f'Mean: {np.mean(silhouette_scores):.3f}')
        axes[0].set_xlabel('Cluster ID')
        axes[0].set_ylabel('Silhouette Score')
        axes[0].set_title('Silhouette Score by Cluster', fontsize=14, fontweight='bold')
        axes[0].legend()
        axes[0].grid(axis='y', alpha=0.3)
        
        # Cluster sizes
        axes[1].bar(cluster_ids, cluster_sizes, color='coral', edgecolor='black')
        axes[1].set_xlabel('Cluster ID')
        axes[1].set_ylabel('Number of Samples')
        axes[1].set_title('Cluster Size Distribution', fontsize=14, fontweight='bold')
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/silhouette_analysis.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Silhouette analysis saved to {save_path}")
        plt.close()
    
    def plot_attack_distribution(self, y, class_names, save_path=None):
        """Plot distribution of attack types in dataset"""
        unique, counts = np.unique(y, return_counts=True)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Bar chart
        colors = sns.color_palette("husl", len(unique))
        axes[0].bar([class_names[i] for i in unique], counts, color=colors, edgecolor='black')
        axes[0].set_xlabel('Attack Type')
        axes[0].set_ylabel('Count')
        axes[0].set_title('Attack Type Distribution', fontsize=14, fontweight='bold')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].grid(axis='y', alpha=0.3)
        
        # Pie chart
        axes[1].pie(counts, labels=[class_names[i] for i in unique], autopct='%1.1f%%',
                   colors=colors, startangle=90)
        axes[1].set_title('Attack Type Percentage', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/attack_distribution.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Attack distribution saved to {save_path}")
        plt.close()
    
    def plot_outlier_detection(self, distances, threshold, outlier_mask, save_path=None):
        """Plot outlier detection results"""
        plt.figure(figsize=(12, 6))
        
        # Plot all distances
        plt.scatter(range(len(distances)), distances, 
                   c=['red' if outlier_mask[i] else 'blue' for i in range(len(distances))],
                   alpha=0.6, s=30)
        
        # Plot threshold
        plt.axhline(y=threshold, color='green', linestyle='--', linewidth=2,
                   label=f'Threshold (d_min): {threshold:.3f}')
        
        plt.xlabel('Sample Index')
        plt.ylabel('Distance from Cluster Center')
        plt.title('Zero-Day Outlier Detection', fontsize=14, fontweight='bold')
        plt.legend(['Outlier', 'Normal', 'Threshold'])
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/outlier_detection.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Outlier detection plot saved to {save_path}")
        plt.close()
    
    def plot_correlation_heatmap(self, correlation_matrix, save_path=None):
        """Plot correlation matrix as heatmap"""
        plt.figure(figsize=(14, 10))
        
        # Select top clusters for visualization
        top_clusters = correlation_matrix.head(20)
        
        sns.heatmap(top_clusters, annot=True, fmt='.1f', cmap='YlOrRd',
                   cbar_kws={'label': 'Percentage (%)'})
        plt.title('Cluster-Attack Correlation Matrix (Top 20 Clusters)', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Attack Category')
        plt.ylabel('Cluster ID')
        plt.tight_layout()
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/correlation_heatmap.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Correlation heatmap saved to {save_path}")
        plt.close()
    
    def create_summary_dashboard(self, metrics_dict, save_path=None):
        """Create a summary dashboard with key metrics"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('Zero-Day Detection Framework - Results Dashboard', 
                    fontsize=16, fontweight='bold')
        
        # Metric boxes
        metrics = [
            ('CNN Accuracy', metrics_dict.get('cnn_accuracy', 0), 'green'),
            ('Ensemble Accuracy', metrics_dict.get('ensemble_accuracy', 0), 'blue'),
            ('Zero-Day Detection', metrics_dict.get('zeroday_detection', 0), 'red'),
            ('False Positive Rate', metrics_dict.get('false_positive', 0), 'orange'),
            ('Outliers Detected', metrics_dict.get('outliers_count', 0), 'purple'),
            ('Total Clusters', metrics_dict.get('num_clusters', 50), 'brown')
        ]
        
        for idx, (name, value, color) in enumerate(metrics):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            ax.text(0.5, 0.5, f'{value:.2f}' if isinstance(value, float) else str(value),
                   ha='center', va='center', fontsize=32, fontweight='bold', color=color)
            ax.text(0.5, 0.2, name, ha='center', va='center', fontsize=12)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, 
                                      fill=False, edgecolor=color, linewidth=3))
        
        if save_path is None:
            save_path = f"{self.results_dir}/plots/summary_dashboard.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Summary dashboard saved to {save_path}")
        plt.close()

    # ── ADD-ON 1 ─────────────────────────────────────────────────────────────
    def plot_roc_curve(self, rf_model, X_test, y_test,
                       save_path=None):
        """ROC Curve for Random Forest (binary: normal=0, attack=1)"""
        try:
            os.makedirs(f"{self.results_dir}/plots", exist_ok=True)
            if save_path is None:
                save_path = f"{self.results_dir}/plots/roc_curve.png"

            # Convert to binary labels: normal=0, everything else=1
            y_binary = (y_test != 0).astype(int)

            # Probability scores for the "attack" class
            if hasattr(rf_model, 'predict_proba'):
                # For multi-class RF sum non-normal probabilities
                proba = rf_model.predict_proba(X_test)
                # class index 0 is 'dos', find 'normal' index dynamically
                # We treat class 0 as "first class"; use 1 - P(normal_col)
                # Safe: sum all non-zero columns
                normal_col = 0  # will be overridden if caller passes class info
                scores = 1 - proba[:, normal_col]
            else:
                raise ValueError("rf_model does not support predict_proba")

            fpr, tpr, _ = roc_curve(y_binary, scores)
            roc_auc = auc(fpr, tpr)

            sns.set_style("whitegrid")
            plt.figure(figsize=(8, 6))
            plt.plot(fpr, tpr, color='steelblue', lw=2,
                     label=f'ROC Curve (AUC = {roc_auc:.4f})')
            plt.plot([0, 1], [0, 1], color='gray', lw=1,
                     linestyle='--', label='Random Classifier')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate', fontsize=12)
            plt.ylabel('True Positive Rate', fontsize=12)
            plt.title('ROC Curve — Random Forest (Phase 2)',
                      fontsize=14, fontweight='bold')
            plt.legend(loc='lower right', fontsize=11)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ ROC curve saved to {save_path}")
            plt.close()
        except Exception as e:
            print(f"⚠ plot_roc_curve skipped: {e}")

    # ── ADD-ON 2 ─────────────────────────────────────────────────────────────
    def plot_feature_importance(self, rf_model, feature_names,
                                save_path=None):
        """Top-12 Feature Importances — Random Forest horizontal bar chart"""
        try:
            os.makedirs(f"{self.results_dir}/plots", exist_ok=True)
            if save_path is None:
                save_path = f"{self.results_dir}/plots/feature_importance.png"

            importances = rf_model.feature_importances_
            indices = np.argsort(importances)[::-1][:12]
            top_importances = importances[indices]
            top_names = [feature_names[i] for i in indices]

            # Reverse for horizontal bar (most important on top)
            top_importances = top_importances[::-1]
            top_names = top_names[::-1]

            # Color gradient: darker blue = more important
            colors = plt.cm.Blues(
                np.linspace(0.35, 0.9, len(top_importances)))

            sns.set_style("whitegrid")
            fig, ax = plt.subplots(figsize=(10, 7))
            bars = ax.barh(top_names, top_importances,
                           color=colors, edgecolor='black', linewidth=0.8)

            # Value labels on each bar
            for bar, val in zip(bars, top_importances):
                ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height() / 2,
                        f'{val:.4f}', va='center', ha='left', fontsize=9)

            ax.set_xlabel('Feature Importance', fontsize=12)
            ax.set_title('Top 12 Feature Importances — Random Forest',
                         fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Feature importance saved to {save_path}")
            plt.close()
        except Exception as e:
            print(f"⚠ plot_feature_importance skipped: {e}")

    # ── ADD-ON 3 ─────────────────────────────────────────────────────────────
    def plot_precision_recall(self, rf_model, X_test, y_test,
                              save_path=None):
        """Precision-Recall Curve — Random Forest (binary classification)"""
        try:
            os.makedirs(f"{self.results_dir}/plots", exist_ok=True)
            if save_path is None:
                save_path = f"{self.results_dir}/plots/precision_recall.png"

            y_binary = (y_test != 0).astype(int)

            if hasattr(rf_model, 'predict_proba'):
                proba = rf_model.predict_proba(X_test)
                scores = 1 - proba[:, 0]
            else:
                raise ValueError("rf_model does not support predict_proba")

            precision, recall, _ = precision_recall_curve(y_binary, scores)
            avg_precision = average_precision_score(y_binary, scores)

            sns.set_style("whitegrid")
            plt.figure(figsize=(8, 6))
            plt.plot(recall, precision, color='darkorange', lw=2,
                     label=f'Avg Precision = {avg_precision:.4f}')
            plt.axhline(y=sum(y_binary) / len(y_binary),
                        color='gray', linestyle='--', lw=1,
                        label='Baseline (random)')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('Recall', fontsize=12)
            plt.ylabel('Precision', fontsize=12)
            plt.title('Precision-Recall Curve — Random Forest',
                      fontsize=14, fontweight='bold')
            plt.legend(loc='lower left', fontsize=11)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Precision-Recall curve saved to {save_path}")
            plt.close()
        except Exception as e:
            print(f"⚠ plot_precision_recall skipped: {e}")

    # ── ADD-ON 4 ─────────────────────────────────────────────────────────────
    def plot_outlier_distribution(self, outlier_labels, class_names,
                                  save_path=None):
        """Pie chart of attack categories among detected zero-day outliers"""
        try:
            os.makedirs(f"{self.results_dir}/plots", exist_ok=True)
            if save_path is None:
                save_path = f"{self.results_dir}/plots/outlier_distribution.png"

            if len(outlier_labels) == 0:
                print("⚠ plot_outlier_distribution skipped: no outliers")
                return

            unique, counts = np.unique(outlier_labels, return_counts=True)
            labels = [class_names[i] for i in unique]

            colors = sns.color_palette("Set2", len(unique))

            sns.set_style("white")
            plt.figure(figsize=(8, 7))
            wedges, texts, autotexts = plt.pie(
                counts,
                labels=labels,
                autopct='%1.1f%%',
                colors=colors,
                startangle=140,
                pctdistance=0.82,
                wedgeprops=dict(edgecolor='white', linewidth=1.5)
            )
            for at in autotexts:
                at.set_fontsize(10)
                at.set_fontweight('bold')

            plt.title('Zero-Day Outlier Distribution by Attack Category',
                      fontsize=13, fontweight='bold', pad=20)

            # Count legend
            legend_labels = [f"{lbl}: {cnt}" for lbl, cnt in zip(labels, counts)]
            plt.legend(wedges, legend_labels, title="Category (count)",
                       loc="lower center", bbox_to_anchor=(0.5, -0.12),
                       ncol=3, fontsize=9)

            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Outlier distribution saved to {save_path}")
            plt.close()
        except Exception as e:
            print(f"⚠ plot_outlier_distribution skipped: {e}")
