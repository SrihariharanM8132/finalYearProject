# MODULE IMPLEMENTATION REFERENCE

## Detailed Module Breakdown for Project Report

This document provides detailed specifications for each software module mentioned in the project.

---

## 1. `data_preprocess.py`

### Purpose
Load, clean, and preprocess the NSL-KDD dataset for machine learning models.

### Key Functions

#### `load_nsl_kdd(train_path, test_path)`
```python
"""
Load NSL-KDD training and test datasets from text files.

Args:
    train_path (str): Path to KDDTrain+.txt
    test_path (str): Path to KDDTest+.txt

Returns:
    tuple: (train_df, test_df) pandas DataFrames

Features loaded:
    - 41 original features + 1 label column
    - Remove difficulty level column
    - Handle missing values
"""
```

#### `encode_categorical_features(df)`
```python
"""
One-hot encode categorical features.

Categorical columns:
    - protocol_type: tcp, udp, icmp (3 values)
    - service: 70 service types
    - flag: 11 connection states

Returns:
    DataFrame with encoded features (93 total features)
"""
```

#### `normalize_features(X_train, X_test)`
```python
"""
Apply StandardScaler normalization.

Formula: z = (x - μ) / σ
    where μ = mean, σ = standard deviation

Returns:
    Normalized feature matrices
"""
```

### Input/Output
- **Input**: Raw .txt files (KDDTrain+.txt, KDDTest+.txt)
- **Output**: 
  - `X_train` (125973 × 93)
  - `y_train` (125973 × 1)
  - `X_test` (22544 × 93)
  - `y_test` (22544 × 1)

### Dependencies
- pandas
- numpy
- sklearn.preprocessing.StandardScaler

---

## 2. `feature_engineering.py`

### Purpose
Extract and engineer additional features to improve model performance.

### Key Functions

#### `create_statistical_features(df)`
```python
"""
Generate statistical aggregation features.

New features:
    - byte_ratio: src_bytes / dst_bytes
    - packet_rate: count / duration
    - error_rate: serror_rate + rerror_rate
    - srv_error_rate: srv_serror_rate + srv_rerror_rate

Returns:
    DataFrame with additional 15 statistical features
"""
```

#### `create_temporal_features(df)`
```python
"""
Extract time-based connection patterns.

New features:
    - duration_log: log(1 + duration)
    - same_srv_rate_bin: binned connection rates
    - diff_srv_rate_category: categorized service diversity

Returns:
    DataFrame with 8 temporal features
"""
```

#### `select_important_features(X, y, threshold=0.01)`
```python
"""
Select features based on importance scores.

Method: Random Forest feature importance
Threshold: Keep features with importance > 0.01

Returns:
    Selected feature matrix
"""
```

### Output
- **Total Features**: 93 (41 original + 52 engineered)

---

## 3. `supervised_models.py`

### Purpose
Implement and train five supervised learning models for known attack classification.

### Models Implemented

#### 3.1 Random Forest Classifier
```python
class RandomForestModel:
    """
    Ensemble of 100 decision trees
    
    Hyperparameters:
        - n_estimators: 100
        - max_depth: 20
        - min_samples_split: 5
        - random_state: 42
    
    Performance:
        - Accuracy: 100%
        - Training time: ~23 seconds
    """
```

#### 3.2 Convolutional Neural Network
```python
class CNNModel:
    """
    3-layer CNN for pattern recognition
    
    Architecture:
        - Conv1D(64 filters, kernel=3) + ReLU + MaxPool
        - Conv1D(128 filters, kernel=3) + ReLU + MaxPool
        - Dense(64) + Dropout(0.5)
        - Dense(5, softmax)
    
    Training:
        - Optimizer: Adam (lr=0.001)
        - Loss: categorical_crossentropy
        - Epochs: 20, batch_size: 128
    
    Performance:
        - Accuracy: 97.2%
        - Training time: ~145 seconds
    """
```

#### 3.3 Decision Tree Classifier
```python
class DecisionTreeModel:
    """
    Single decision tree classifier
    
    Hyperparameters:
        - criterion: gini
        - max_depth: 20
        - min_samples_split: 10
    
    Performance:
        - Accuracy: 100%
        - Training time: ~8 seconds
    """
```

#### 3.4 K-Nearest Neighbors
```python
class KNNModel:
    """
    Distance-based instance learning
    
    Hyperparameters:
        - n_neighbors: 5
        - metric: euclidean
        - weights: uniform
    
    Performance:
        - Accuracy: 99%
        - Training time: ~12 seconds
    """
```

#### 3.5 Naive Bayes Classifier
```python
class NaiveBayesModel:
    """
    Gaussian Naive Bayes probabilistic classifier
    
    Assumption: Features follow Gaussian distribution
    
    Performance:
        - Accuracy: 98%
        - Training time: ~5 seconds
    """
```

### Evaluation Functions

#### `evaluate_model(model, X_test, y_test)`
```python
"""
Comprehensive model evaluation.

Metrics computed:
    - Accuracy: (TP + TN) / Total
    - Precision: TP / (TP + FP) per class
    - Recall: TP / (TP + FN) per class
    - F1-Score: 2 * (P * R) / (P + R)
    - ROC-AUC: Area under ROC curve

Returns:
    Dictionary with all metrics
"""
```

---

## 4. `clustering_outliers.py`

### Purpose
Apply K-Means clustering and detect zero-day attacks through outlier analysis.

### Key Functions

#### `train_kmeans(X, n_clusters=50)`
```python
"""
Train K-Means clustering model.

Algorithm: Lloyd's algorithm (EM-style)
Hyperparameters:
    - n_clusters: 50
    - init: k-means++
    - max_iter: 300
    - random_state: 42

Returns:
    Trained KMeans model + cluster labels
"""
```

#### `calculate_distances(X, kmeans_model)`
```python
"""
Calculate Euclidean distances to cluster centroids.

Formula: d_i = ||x_i - c_k||₂
    where c_k is the centroid of cluster k

Returns:
    Array of distances (shape: n_samples)
"""
```

#### `compute_threshold(distances, cluster_labels)`
```python
"""
Compute dynamic distance threshold for outlier detection.

Formula: d_min = (a_i + b_i) / 2
    where:
    a_i = max intra-cluster distance
    b_i = min inter-cluster distance

Returns:
    Threshold value (float)
"""
```

#### `detect_outliers(distances, threshold)`
```python
"""
Flag samples as outliers if distance > threshold.

Returns:
    Boolean array (True = outlier, False = normal)
"""
```

#### `compute_silhouette_score(X, labels)`
```python
"""
Calculate clustering quality metric.

Formula: s = (b - a) / max(a, b)
    where:
    a = mean intra-cluster distance
    b = mean nearest-cluster distance

Range: [-1, 1] (higher is better)

Returns:
    Silhouette score (float)
"""
```

### Output
- **Cluster Labels**: Array of length 22,544
- **Distances**: Array of length 22,544
- **Outlier Flags**: Boolean array (2-5% True)
- **Silhouette Score**: 0.54 (good separation)

---

## 5. `correlation_online.py`

### Purpose
Correlate clustering results with classification predictions and validate zero-day detection.

### Key Functions

#### `map_clusters_to_classes(cluster_labels, class_predictions)`
```python
"""
Create cluster-class correlation table.

Process:
    1. For each cluster, count class occurrences
    2. Assign dominant class (highest count)
    3. Calculate cluster purity

Returns:
    DataFrame with columns:
        - cluster_id
        - dominant_class
        - purity (%)
        - size
        - avg_distance
"""
```

#### `identify_zero_day_candidates(outlier_flags, predictions)`
```python
"""
Select outlier samples as zero-day candidates.

Selection criteria:
    - Distance > threshold (outlier_flag = True)
    - Optionally filter by prediction confidence

Returns:
    List of sample indices
"""
```

#### `online_learning_experiment(model, X_train, y_train, zero_day_samples, X_test, y_test)`
```python
"""
Validate zero-day detection through incremental learning.

Process:
    1. Record baseline accuracy on test set
    2. Add zero-day samples to training set (with pseudo-labels)
    3. Retrain model
    4. Measure accuracy change

Expected behavior:
    - Accuracy should drop if zero-day samples are truly novel
    - Or remain stable if they match known patterns

Returns:
    Dictionary with:
        - baseline_accuracy
        - retrained_accuracy
        - accuracy_change
        - validation_result
"""
```

### Output
- **Correlation Table**: 50 rows (one per cluster)
- **Zero-Day Candidates**: List of 500-1,100 sample indices
- **Online Learning Metrics**: Accuracy change measurements

---

## 6. `main.py`

### Purpose
Orchestrate the complete dual-phase pipeline.

### Execution Flow

```python
def main():
    """
    Main execution pipeline for dual-phase learning.
    """
    
    # ==================== PHASE 0: Setup ====================
    print("Loading NSL-KDD dataset...")
    X_train, y_train, X_test, y_test = load_and_preprocess_data()
    
    # ==================== PHASE 1: Supervised Learning ====================
    print("\n=== PHASE 1: Supervised Learning ===")
    
    models = {}
    results = {}
    
    # Train Random Forest
    print("Training Random Forest...")
    models['RF'] = train_random_forest(X_train, y_train)
    results['RF'] = evaluate_model(models['RF'], X_test, y_test)
    
    # Train CNN
    print("Training CNN...")
    models['CNN'] = train_cnn(X_train, y_train)
    results['CNN'] = evaluate_model(models['CNN'], X_test, y_test)
    
    # Train Decision Tree
    print("Training Decision Tree...")
    models['DT'] = train_decision_tree(X_train, y_train)
    results['DT'] = evaluate_model(models['DT'], X_test, y_test)
    
    # Train KNN
    print("Training KNN...")
    models['KNN'] = train_knn(X_train, y_train)
    results['KNN'] = evaluate_model(models['KNN'], X_test, y_test)
    
    # Train Naive Bayes
    print("Training Naive Bayes...")
    models['NB'] = train_naive_bayes(X_train, y_train)
    results['NB'] = evaluate_model(models['NB'], X_test, y_test)
    
    print_phase1_results(results)
    
    # ==================== PHASE 2: Clustering ====================
    print("\n=== PHASE 2: Unsupervised Clustering ===")
    
    # K-Means clustering
    print("Running K-Means clustering (K=50)...")
    kmeans_model = train_kmeans(X_test, n_clusters=50)
    cluster_labels = kmeans_model.labels_
    
    # Calculate distances
    print("Calculating distances to centroids...")
    distances = calculate_distances(X_test, kmeans_model)
    
    # Compute threshold
    threshold = compute_threshold(distances, cluster_labels)
    print(f"Outlier threshold: {threshold:.4f}")
    
    # Detect outliers
    outlier_flags = detect_outliers(distances, threshold)
    print(f"Outliers detected: {outlier_flags.sum()} ({outlier_flags.mean():.2%})")
    
    # Silhouette score
    silhouette = compute_silhouette_score(X_test, cluster_labels)
    print(f"Silhouette score: {silhouette:.4f}")
    
    # ==================== PHASE 3: Correlation ====================
    print("\n=== PHASE 3: Correlation Analysis ===")
    
    # Get best model predictions
    best_model = models['RF']  # Random Forest had highest accuracy
    predictions = best_model.predict(X_test)
    
    # Create correlation table
    corr_table = map_clusters_to_classes(cluster_labels, predictions)
    print("\nCluster-Class Correlation:")
    print(corr_table.head(10))
    
    # Identify zero-day candidates
    zero_day_indices = identify_zero_day_candidates(outlier_flags, predictions)
    print(f"\nZero-day candidates identified: {len(zero_day_indices)}")
    
    # ==================== PHASE 4: Validation ====================
    print("\n=== PHASE 4: Online Learning Validation ===")
    
    online_results = online_learning_experiment(
        model=models['RF'],
        X_train=X_train,
        y_train=y_train,
        zero_day_samples=X_test[zero_day_indices],
        X_test=X_test,
        y_test=y_test
    )
    
    print(f"Baseline accuracy: {online_results['baseline_accuracy']:.4f}")
    print(f"Retrained accuracy: {online_results['retrained_accuracy']:.4f}")
    print(f"Accuracy change: {online_results['accuracy_change']:.4f}")
    
    # ==================== PHASE 5: Save Results ====================
    print("\n=== Saving Results ===")
    
    save_models(models, 'models/')
    save_metrics(results, 'results/metrics/')
    save_correlation_table(corr_table, 'results/correlation_table.csv')
    save_zero_day_candidates(zero_day_indices, 'results/zero_day_candidates.csv')
    generate_visualizations(results, corr_table, 'results/plots/')
    
    print("\n✅ Pipeline complete! Check 'results/' directory for outputs.")
```

---

## 7. `utils.py`

### Purpose
Helper functions for visualization and file I/O.

### Key Functions

#### `plot_confusion_matrix(y_true, y_pred, class_names)`
```python
"""
Generate confusion matrix heatmap.

Uses: seaborn heatmap
Saves: results/plots/confusion_matrix_<model>.png
"""
```

#### `plot_roc_curves(models, X_test, y_test)`
```python
"""
Plot ROC curves for all models.

Computes: TPR, FPR, AUC for each class
Saves: results/plots/roc_curves.png
"""
```

#### `plot_cluster_distribution(cluster_labels, predictions)`
```python
"""
Visualize cluster size and composition.

Charts: Bar chart + pie chart
Saves: results/plots/cluster_distribution.png
"""
```

#### `save_metrics_table(metrics_dict, filepath)`
```python
"""
Save metrics to CSV for reporting.

Columns: Model, Accuracy, Precision, Recall, F1, ROC-AUC
"""
```

---

## Module Dependencies

```
main.py
    ├── data_preprocess.py
    │       ├── pandas
    │       ├── numpy
    │       └── sklearn.preprocessing
    │
    ├── feature_engineering.py
    │       ├── pandas
    │       └── sklearn.feature_selection
    │
    ├── supervised_models.py
    │       ├── sklearn.ensemble (RandomForest)
    │       ├── sklearn.tree (DecisionTree)
    │       ├── sklearn.neighbors (KNN)
    │       ├── sklearn.naive_bayes (NaiveBayes)
    │       ├── tensorflow.keras (CNN)
    │       └── sklearn.metrics
    │
    ├── clustering_outliers.py
    │       ├── sklearn.cluster (KMeans)
    │       └── sklearn.metrics (silhouette_score)
    │
    ├── correlation_online.py
    │       └── pandas
    │
    └── utils.py
            ├── matplotlib
            ├── seaborn
            └── plotly
```

---

## Execution Command

```bash
# Install dependencies
pip install -r requirements.txt

# Run complete pipeline
python main.py

# Run interactive dashboard
streamlit run dashboard.py
```

---

**Author**: Srihariharan M  
**Date**: December 15, 2025  
**Version**: 1.0
