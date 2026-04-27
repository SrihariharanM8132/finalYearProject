from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
import numpy as np
import matplotlib.pyplot as plt

class ZeroDayClustering:
    """
    K-Means clustering for zero-day detection (Section 4.3)
    """
    def __init__(self, n_clusters=50):
        self.n_clusters = n_clusters
        self.kmeans = None
        self.cluster_info = {}
        self.intra_distances = None
        self.inter_distances = None
        self.cluster_centers = None
    
    def fit_clusters(self, X):
        """Fit K-Means with specified clusters"""
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        cluster_labels = self.kmeans.fit_predict(X)
        self.cluster_centers = self.kmeans.cluster_centers_
        
        # Calculate cluster metrics
        self.calculate_cluster_metrics(X, cluster_labels)
        
        return cluster_labels
    
    def calculate_cluster_metrics(self, X, labels):
        """
        Calculate intra-cluster (a(i)) and inter-cluster (b(i)) distances
        As per Section 5
        """
        self.intra_distances = np.zeros(self.n_clusters)
        self.inter_distances = np.zeros(self.n_clusters)
        
        for cluster_id in range(self.n_clusters):
            cluster_points = X[labels == cluster_id]
            
            if len(cluster_points) == 0:
                continue
            
            # Calculate centroid
            centroid = self.kmeans.cluster_centers_[cluster_id]
            
            # Intra-cluster distance a(i)
            distances = np.linalg.norm(cluster_points - centroid, axis=1)
            a_i = np.mean(distances)
            self.intra_distances[cluster_id] = a_i
            
            # Inter-cluster distance b(i)
            other_centroids = np.delete(self.kmeans.cluster_centers_, 
                                       cluster_id, axis=0)
            b_i = np.min(np.linalg.norm(other_centroids - centroid, axis=1))
            self.inter_distances[cluster_id] = b_i
            
            # Silhouette score
            if max(a_i, b_i) > 0:
                s_sil = (b_i - a_i) / max(a_i, b_i)
            else:
                s_sil = 0
            
            self.cluster_info[cluster_id] = {
                'count': len(cluster_points),
                'a_i': a_i,
                'b_i': b_i,
                's_sil': s_sil,
                'centroid': centroid
            }
        
        return self.cluster_info
    
    def display_top_clusters(self, top_n=5):
        """Display top N clusters by size"""
        sorted_clusters = sorted(
            self.cluster_info.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )
        
        print(f"\nTop {top_n} Clusters:")
        print(f"{'Cluster':<10}{'Count':<10}{'a(i)':<10}{'b(i)':<10}{'S_sil':<10}")
        print("-" * 50)
        
        for cluster_id, info in sorted_clusters[:top_n]:
            print(f"{cluster_id:<10}{info['count']:<10}"
                  f"{info['a_i']:<10.3f}{info['b_i']:<10.3f}"
                  f"{info['s_sil']:<10.3f}")