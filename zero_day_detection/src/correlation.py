import pandas as pd
import numpy as np

class CorrelationTable:
    """
    Create correlation between supervised targets and unsupervised clusters
    (Section 4.4)
    """
    def __init__(self):
        self.correlation_matrix = None
    
    def create_correlation(self, cluster_labels, supervised_targets):
        """
        Map each cluster to target classes
        """
        correlation_dict = {}
        
        for cluster_id in np.unique(cluster_labels):
            # Get indices of points in this cluster
            cluster_mask = cluster_labels == cluster_id
            
            # Get corresponding targets
            cluster_targets = supervised_targets[cluster_mask]
            
            # Calculate percentage of each target in cluster
            unique, counts = np.unique(cluster_targets, return_counts=True)
            total = len(cluster_targets)
            
            target_percentages = {}
            for target, count in zip(unique, counts):
                percentage = (count / total) * 100
                target_percentages[f"target_{target}"] = percentage
            
            correlation_dict[f"cluster_{cluster_id}"] = target_percentages
        
        # Convert to DataFrame
        self.correlation_matrix = pd.DataFrame(correlation_dict).T.fillna(0)
        
        return self.correlation_matrix
    
    def display_correlation(self):
        """Display correlation table"""
        print("\nCorrelation Table (Top 10 Clusters):")
        print(self.correlation_matrix.head(10).to_string())
    
    def save_correlation(self, filepath='results/correlation_table.csv'):
        """Save correlation table"""
        self.correlation_matrix.to_csv(filepath)
        print(f"\nCorrelation table saved to {filepath}")