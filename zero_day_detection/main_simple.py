import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("ZERO-DAY DETECTION - SIMPLIFIED VERSION")
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

# ===== PHASE 1: LOAD DATA =====
print("\n[PHASE 1] Loading data...")
df = load_nsl_kdd('data/KDDTrain+.txt')

# Take smaller sample for quick testing
df = df.sample(n=5000, random_state=42)
print(f"✓ Using {len(df)} samples for quick test")

# Feature engineering
df = feature_engineering(df)
df = create_labels(df)
df = encode_categorical(df)

# Prepare features and labels
X = df.drop(['attack_type', 'attack_category'], axis=1)
y = LabelEncoder().fit_transform(df['attack_category'])

print(f"✓ Features: {X.shape[1]}")
print(f"✓ Classes: {len(np.unique(y))}")

# ===== PHASE 2: TRAIN MODEL =====
print("\n[PHASE 2] Training models...")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Normalize
X_train_norm, X_test_norm, scaler = normalize_data(X_train, X_test)

# Train CNN (only 5 epochs for speed)
print("Training CNN (5 epochs)...")
cnn_model = build_1d_cnn(X_train_norm.shape[1], len(np.unique(y)))
cnn_model, history = train_cnn(
    cnn_model, X_train_norm, y_train,
    X_test_norm, y_test, epochs=5
)

# Get accuracy
from sklearn.metrics import accuracy_score
cnn_pred = np.argmax(cnn_model.predict(X_test_norm), axis=1)
cnn_acc = accuracy_score(y_test, cnn_pred)
print(f"✓ CNN Accuracy: {cnn_acc:.4f}")

# Train boosting models
print("\nTraining boosting models...")
ensemble = BoostingEnsemble()
ensemble.train_all(X_train_norm, y_train)
results = ensemble.evaluate(X_test_norm, y_test)

# ===== PHASE 3: CLUSTERING =====
print("\n[PHASE 3] Clustering...")
clustering = ZeroDayClustering(n_clusters=10)  # Reduced clusters for speed
cluster_labels = clustering.fit_clusters(X_train_norm)
clustering.display_top_clusters(top_n=3)

# ===== PHASE 4: CORRELATION =====
print("\n[PHASE 4] Correlation analysis...")
correlation = CorrelationTable()
corr_matrix = correlation.create_correlation(cluster_labels, y_train)
print("✓ Correlation table created")

# ===== PHASE 5: ZERO-DAY DETECTION =====
print("\n[PHASE 5] Zero-day detection...")
detector = ZeroDayDetector(clustering)
detector.calculate_d_min()

cluster_labels_test = clustering.kmeans.predict(X_test_norm)
outliers = detector.detect_outliers(X_test_norm, cluster_labels_test)

if len(outliers) > 0:
    print(f"✓ Detected {len(outliers)} potential zero-day attacks!")
else:
    print("⚠ No outliers detected (may need to adjust threshold)")

print("\n" + "="*60)
print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
print("="*60)
print("\nNext steps:")
print("1. Run full version: python main.py")
print("2. Check results in results/ folder")
print("3. View visualizations")