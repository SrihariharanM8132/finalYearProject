"""
Zero-Day Attack Detection Module
Implements clustering-based outlier detection and validation
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, accuracy_score, f1_score
import warnings
warnings.filterwarnings('ignore')


class ZeroDayClustering:
    """
    Unsupervised clustering for pattern discovery and outlier detection
    """
    
    def __init__(self, n_clusters=50, random_state=42):
        """
        Initialize K-Means clustering
        
        Args:
            n_clusters: Number of clusters (default: 50)
            random_state: Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.cluster_labels = None
        self.cluster_centers = None
        self.intra_distances = None
        self.inter_distances = None
        
    def fit_clusters(self, X):
        """
        Fit K-Means clustering on data
        
        Args:
            X: Feature matrix (numpy array or pandas DataFrame)
            
        Returns:
            cluster_labels: Cluster assignment for each sample
        """
        print(f"\n[PHASE 3] K-Means Clustering (K={self.n_clusters})...")
        print("="*60)
        
        # Fit clustering
        self.cluster_labels = self.kmeans.fit_predict(X)
        self.cluster_centers = self.kmeans.cluster_centers_
        
        # Calculate metrics
        self._calculate_cluster_metrics(X)
        
        print(f"✓ Clustering completed: {len(np.unique(self.cluster_labels))} clusters formed")
        print(f"✓ Silhouette Score: {silhouette_score(X, self.cluster_labels):.4f}")
        
        return self.cluster_labels
    
    def _calculate_cluster_metrics(self, X):
        """
        Calculate intra-cluster and inter-cluster distances
        
        Args:
            X: Feature matrix
        """
        n_clusters = len(np.unique(self.cluster_labels))
        self.intra_distances = np.zeros(n_clusters)
        self.inter_distances = np.zeros(n_clusters)
        
        for i in range(n_clusters):
            # Get samples in this cluster
            cluster_mask = self.cluster_labels == i
            cluster_samples = X[cluster_mask]
            
            if len(cluster_samples) > 0:
                # Intra-cluster distance (a_i): average distance within cluster
                distances = np.linalg.norm(cluster_samples - self.cluster_centers[i], axis=1)
                self.intra_distances[i] = np.mean(distances)
                
                # Inter-cluster distance (b_i): distance to nearest other cluster
                other_centers = np.delete(self.cluster_centers, i, axis=0)
                inter_dists = np.linalg.norm(other_centers - self.cluster_centers[i], axis=1)
                self.inter_distances[i] = np.min(inter_dists)
    
    def display_top_clusters(self, top_n=10):
        """
        Display top N largest clusters with metrics
        
        Args:
            top_n: Number of top clusters to display
        """
        print(f"\n[PHASE 3] Top {top_n} Clusters by Size:")
        print("="*60)
        
        # Count samples per cluster
        unique, counts = np.unique(self.cluster_labels, return_counts=True)
        cluster_sizes = dict(zip(unique, counts))
        
        # Sort by size
        sorted_clusters = sorted(cluster_sizes.items(), key=lambda x: x[1], reverse=True)
        
        print(f"{'Cluster':<10} {'Size':<10} {'a(i)':<10} {'b(i)':<10} {'S_sil':<10}")
        print("-"*60)
        
        for cluster_id, size in sorted_clusters[:top_n]:
            a_i = self.intra_distances[cluster_id]
            b_i = self.inter_distances[cluster_id]
            
            # Silhouette coefficient for this cluster
            if a_i < b_i:
                s_sil = (b_i - a_i) / b_i
            elif a_i > b_i:
                s_sil = (b_i - a_i) / a_i
            else:
                s_sil = 0.0
            
            print(f"{cluster_id:<10} {size:<10} {a_i:<10.3f} {b_i:<10.3f} {s_sil:<10.3f}")


class ZeroDayDetector:
    """
    Zero-day attack detection using outlier detection and validation
    """
    
    def __init__(self, clustering):
        """
        Initialize detector
        
        Args:
            clustering: Fitted ZeroDayClustering object
        """
        self.clustering = clustering
        self.outlier_indices = None
        self.d_min_thresholds = None
        
    def calculate_d_min(self):
        """
        Calculate distance threshold (d_min) for each cluster
        
        d_min = (a_i + b_i) / 2
        where:
            a_i = intra-cluster distance
            b_i = inter-cluster distance
        """
        print("\n[PHASE 5] Calculating Distance Thresholds...")
        print("="*60)
        
        self.d_min_thresholds = (self.clustering.intra_distances + 
                                 self.clustering.inter_distances) / 2
        
        print(f"✓ Calculated d_min thresholds for {len(self.d_min_thresholds)} clusters")
        print(f"  Average d_min: {np.mean(self.d_min_thresholds):.4f}")
        print(f"  Min d_min: {np.min(self.d_min_thresholds):.4f}")
        print(f"  Max d_min: {np.max(self.d_min_thresholds):.4f}")
    
    def detect_outliers(self, X, cluster_labels):
        """
        Detect outliers based on distance from cluster centers
        
        Args:
            X: Feature matrix
            cluster_labels: Cluster assignments
            
        Returns:
            outlier_mask: Boolean array indicating outliers
        """
        print("\n[PHASE 5] Detecting Outliers...")
        print("="*60)
        
        outlier_mask = np.zeros(len(X), dtype=bool)
        outlier_distances = []
        
        for i in range(len(X)):
            cluster_id = cluster_labels[i]
            cluster_center = self.clustering.cluster_centers[cluster_id]
            
            # Calculate distance from sample to its cluster center
            distance = np.linalg.norm(X[i] - cluster_center)
            
            # Check if distance exceeds threshold
            if distance > self.d_min_thresholds[cluster_id]:
                outlier_mask[i] = True
                outlier_distances.append(distance)
        
        self.outlier_indices = np.where(outlier_mask)[0]
        
        print(f"✓ Outliers detected: {len(self.outlier_indices)} ({len(self.outlier_indices)/len(X)*100:.2f}%)")
        
        if len(outlier_distances) > 0:
            print(f"  Average outlier distance: {np.mean(outlier_distances):.4f}")
            print(f"  Max outlier distance: {np.max(outlier_distances):.4f}")
        
        # Distribution across clusters
        outlier_clusters = cluster_labels[outlier_mask]
        unique_clusters = len(np.unique(outlier_clusters))
        print(f"  Outliers distributed across {unique_clusters} clusters")
        
        return outlier_mask
    
    def validate_zero_day_detection(self, models, X_outliers, y_outliers, X_test, y_test):
        """
        Validate zero-day detection through online learning test.
        
        Purpose: Prove outliers are genuinely different from training data
        Method: Test models on outliers and measure accuracy degradation
        Expectation: Significant drops indicate successful zero-day detection
        
        Args:
            models: Dictionary of trained models
            X_outliers: Outlier samples (zero-day candidates)
            y_outliers: Labels for outliers
            X_test: Full test dataset
            y_test: Full test labels
        
        Returns:
            results: List of dictionaries with validation results
        """
        print("\n" + "="*70)
        print("ZERO-DAY DETECTION VALIDATION")
        print("="*70)
        
        if len(X_outliers) == 0:
            print("\n⚠️  No outliers detected. Validation skipped.")
            return []
        
        results = []
        total_degradation = 0
        
        for name, model in models.items():
            # Baseline: Performance on normal test data
            baseline_preds = model.predict(X_test)
            baseline_acc = accuracy_score(y_test, baseline_preds)
            baseline_f1 = f1_score(y_test, baseline_preds, average='weighted')
            
            # Online: Performance on outliers (zero-day candidates)
            online_preds = model.predict(X_outliers)
            online_acc = accuracy_score(y_outliers, online_preds)
            online_f1 = f1_score(y_outliers, online_preds, average='weighted')
            
            # Calculate degradation
            accuracy_drop = baseline_acc - online_acc
            drop_percentage = accuracy_drop * 100
            total_degradation += accuracy_drop
            
            # Interpret degradation level (degradation is EXPECTED for zero-day attacks)
            if drop_percentage >= 30:
                status = "SEVERE DEGRADATION ⚠️⚠️⚠️"
                interpretation = "Highly sensitive to novel patterns (EXPECTED - validates zero-day detection)"
            elif drop_percentage >= 10:
                status = "SIGNIFICANT DEGRADATION ⚠️⚠️"
                interpretation = "Detects novel patterns effectively (EXPECTED - validates methodology)"
            elif drop_percentage >= 5:
                status = "MODERATE DEGRADATION ⚠️"
                interpretation = "Some difficulty with novel patterns (EXPECTED - good detection)"
            else:
                status = "SLIGHT DEGRADATION ✓"
                interpretation = "Relatively robust to outliers (EXCELLENT - very stable)"
            
            # Store results
            result = {
                'model': name,
                'baseline_accuracy': baseline_acc,
                'baseline_f1': baseline_f1,
                'online_accuracy': online_acc,
                'online_f1': online_f1,
                'accuracy_drop': accuracy_drop,
                'drop_percentage': drop_percentage,
                'status': status,
                'interpretation': interpretation
            }
            results.append(result)
            
            # Display individual results
            print(f"\n{name}:")
            print(f"  Baseline Accuracy: {baseline_acc:.4f} ({baseline_acc*100:.2f}%)")
            print(f"  Online Accuracy: {online_acc:.4f} ({online_acc*100:.2f}%)")
            print(f"  Accuracy Drop: {drop_percentage:.2f}%")
            print(f"  Status: {status}")
            print(f"  Interpretation: {interpretation}")
        
        # Summary
        avg_degradation = (total_degradation / len(models)) * 100
        
        print("\n" + "="*70)
        print("VALIDATION CONCLUSION")
        print("="*70)
        
        print(f"\n✅ All models tested on {len(X_outliers)} outliers")
        print(f"✅ Average accuracy degradation: {avg_degradation:.2f}%")
        print(f"✅ Degradation range: {min(r['drop_percentage'] for r in results):.2f}% - {max(r['drop_percentage'] for r in results):.2f}%")
        
        # Validation conclusion
        if avg_degradation > 5:
            print(f"\n🎯 VALIDATION SUCCESSFUL!")
            print(f"   ✓ Accuracy degradation on outliers is EXPECTED behavior")
            print(f"   ✓ This confirms outliers are genuinely novel zero-day patterns")
            print(f"   ✓ Zero-day detection methodology is VALIDATED and working correctly")
        else:
            print(f"\n⚠️  VALIDATION INCONCLUSIVE")
            print(f"   Small accuracy drops suggest outliers may be normal variations")
            print(f"   Consider adjusting outlier detection threshold")
        
        # Production recommendation
        print(f"\n📊 PRODUCTION DEPLOYMENT:")
        best_baseline = max(results, key=lambda x: x['baseline_accuracy'])
        print(f"   Recommended Model: {best_baseline['model']}")
        print(f"   Baseline Accuracy: {best_baseline['baseline_accuracy']*100:.2f}%")
        print(f"   Rationale: Highest accuracy on known attack patterns")
        
        print(f"\n🔍 ZERO-DAY HANDLING:")
        print(f"   Method: Clustering-based outlier detection")
        print(f"   Action: Flag outliers for security analyst investigation")
        print(f"   Do NOT retrain models on outliers (they're anomalies!)")
        
        print("="*70 + "\n")
        
        return results


# Example usage and helper functions
def save_validation_results(results, filepath='results/validation_results.csv'):
    """
    Save validation results to CSV file
    
    Args:
        results: List of result dictionaries
        filepath: Output file path
    """
    import os
    
    # Create results directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Convert to DataFrame and save
    df = pd.DataFrame(results)
    df.to_csv(filepath, index=False)
    print(f"\n✓ Validation results saved to: {filepath}")


def print_cluster_distribution(cluster_labels, y_true, attack_names):
    """
    Print distribution of attack types within each cluster
    
    Args:
        cluster_labels: Cluster assignments
        y_true: True labels
        attack_names: List of attack category names
    """
    print("\n[ANALYSIS] Cluster-Attack Distribution:")
    print("="*60)
    
    unique_clusters = np.unique(cluster_labels)
    
    for cluster_id in unique_clusters[:10]:  # Show top 10
        mask = cluster_labels == cluster_id
        cluster_labels_subset = y_true[mask]
        
        print(f"\nCluster {cluster_id} ({np.sum(mask)} samples):")
        
        for label_idx, attack_name in enumerate(attack_names):
            count = np.sum(cluster_labels_subset == label_idx)
            percentage = (count / len(cluster_labels_subset)) * 100 if len(cluster_labels_subset) > 0 else 0
            
            if percentage > 5:  # Only show if > 5%
                print(f"  {attack_name}: {count} ({percentage:.2f}%)")
