import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
import time
warnings.filterwarnings('ignore')

def print_phase(phase_num, total_phases, title):
    """Print phase header with progress"""
    print("\n" + "="*60)
    print(f"PHASE {phase_num}/{total_phases}: {title}")
    print("="*60)

def main():
    start_time = time.time()
    total_phases = 5
    
    print("="*60)
    print("ZERO-DAY ATTACK DETECTION FRAMEWORK")
    print("Full Implementation")
    print("="*60)
    
    # Import modules
    from src.load_data import load_nsl_kdd
    from src.feature_engineering import (feature_engineering, encode_categorical, 
                                         create_labels, normalize_data)
    from src.cnn_model import build_1d_cnn, train_cnn
    from src.boosting_models import BoostingEnsemble
    from src.clustering import ZeroDayClustering
    from src.correlation import CorrelationTable
    from src.zero_day_detection import ZeroDayDetector
    
    # ========== PHASE 1 ==========
    print_phase(1, total_phases, "DATA COLLECTION & PREPROCESSING")
    phase_start = time.time()
    
    print("Loading NSL-KDD dataset...")
    train_data = load_nsl_kdd('data/KDDTrain+.txt')
    
    print("Applying feature engineering...")
    train_data = feature_engineering(train_data)
    train_data = create_labels(train_data)
    train_data = encode_categorical(train_data)
    
    # Separate features and labels
    X = train_data.drop(['attack_type', 'attack_category'], axis=1)
    y_category = train_data['attack_category']
    
    # Encode labels
    le = LabelEncoder()
    y = le.fit_transform(y_category)
    
    print(f"\n✓ Phase 1 completed in {time.time()-phase_start:.1f}s")
    print(f"  Total samples: {len(X):,}")
    print(f"  Features: {X.shape[1]}")
    print(f"  Classes: {list(le.classes_)}")
    
    # ========== PHASE 2 ==========
    print_phase(2, total_phases, "SUPERVISED CLASSIFICATION")
    phase_start = time.time()
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"Training set: {len(X_train):,} samples")
    print(f"Test set: {len(X_test):,} samples")
    
    # Normalize
    print("\nNormalizing data...")
    X_train_norm, X_test_norm, scaler = normalize_data(X_train, X_test)
    
    # Build and train CNN
    print("\nBuilding CNN model...")
    input_shape = X_train_norm.shape[1]
    num_classes = len(np.unique(y))
    
    cnn_model = build_1d_cnn(input_shape, num_classes)
    print(f"Model architecture: {cnn_model.count_params():,} parameters")
    
    print("\nTraining CNN (20 epochs)...")
    print("This will take 10-15 minutes...\n")
    
    cnn_model, history = train_cnn(cnn_model, X_train_norm, y_train,
                                   X_test_norm, y_test, epochs=20)
    
    # Get CNN predictions
    cnn_predictions = np.argmax(cnn_model.predict(X_test_norm, verbose=0), axis=1)
    
    from sklearn.metrics import accuracy_score, classification_report
    cnn_acc = accuracy_score(y_test, cnn_predictions)
    print(f"\n✓ CNN Accuracy: {cnn_acc:.4f}")
    
    # Train boosting models
    print("\nTraining boosting ensemble...")
    ensemble = BoostingEnsemble()
    ensemble.train_all(X_train_norm, y_train)
    
    print("\nEvaluating boosting models:")
    ensemble.evaluate(X_test_norm, y_test)
    
    # Combined predictions
    final_predictions = ensemble.predict_with_boosting(X_test_norm, cnn_predictions)
    final_acc = accuracy_score(y_test, final_predictions)
    print(f"\n✓ Combined Accuracy: {final_acc:.4f}")
    
    print(f"\n✓ Phase 2 completed in {time.time()-phase_start:.1f}s")
    
    # ========== PHASE 3 ==========
    print_phase(3, total_phases, "UNSUPERVISED CLUSTERING")
    phase_start = time.time()
    
    print("Running K-Means clustering (K=50)...")
    clustering = ZeroDayClustering(n_clusters=50)
    
    cluster_labels = clustering.fit_clusters(X_train_norm)
    
    print("\nCluster quality metrics:")
    clustering.display_top_clusters(top_n=5)
    
    print(f"\n✓ Phase 3 completed in {time.time()-phase_start:.1f}s")
    
    # ========== PHASE 4 ==========
    print_phase(4, total_phases, "CORRELATION ANALYSIS")
    phase_start = time.time()
    
    print("Creating correlation table...")
    correlation = CorrelationTable()
    corr_matrix = correlation.create_correlation(cluster_labels, y_train)
    correlation.display_correlation()
    correlation.save_correlation()
    
    print(f"\n✓ Phase 4 completed in {time.time()-phase_start:.1f}s")
    
    # ========== PHASE 5 ==========
    print_phase(5, total_phases, "ZERO-DAY DETECTION")
    phase_start = time.time()
    
    # Simulate new data with zero-day (use test set)
    print("Analyzing test data for anomalies...")
    cluster_labels_test = clustering.kmeans.predict(X_test_norm)
    
    # Initialize detector
    detector = ZeroDayDetector(clustering)
    detector.calculate_d_min()
    
    print(f"Calculated d_min for {len(detector.d_min)} clusters")
    
    # Detect outliers
    outlier_indices = detector.detect_outliers(X_test_norm, cluster_labels_test)
    
    # Online learning with outliers
    if len(outlier_indices) > 0:
        print(f"\n✓ Found {len(outlier_indices)} outliers!")
        print("Performing online learning...")
        
        X_outliers = X_test_norm[outlier_indices]
        y_outliers = y_test[outlier_indices]
        
        models = ensemble.models.copy()
        
        results = detector.online_learning(
            models, X_outliers, y_outliers,
            X_test_norm, y_test
        )
        
        # Count models kept
        kept = sum([1 for r in results.values() if r['keep']])
        print(f"\n✓ Models retained: {kept}/{len(results)}")
    else:
        print("\n⚠ No outliers detected (threshold may need adjustment)")
    
    print(f"\n✓ Phase 5 completed in {time.time()-phase_start:.1f}s")
    
    # ========== SUMMARY ==========
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)
    print(f"Total execution time: {total_time/60:.1f} minutes")
    print(f"Dataset size: {len(X):,} samples")
    print(f"CNN Accuracy: {cnn_acc:.4f}")
    print(f"Combined Accuracy: {final_acc:.4f}")
    print(f"Clusters formed: {clustering.n_clusters}")
    print(f"Outliers detected: {len(outlier_indices)}")
    print("\nResults saved to:")
    print("  - results/correlation_table.csv")
    print("\n✅ FRAMEWORK EXECUTION COMPLETED!")
    print("="*60)

if __name__ == "__main__":
    main()