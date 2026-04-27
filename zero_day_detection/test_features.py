from src.load_data import load_nsl_kdd
from src.feature_engineering import feature_engineering, create_labels, encode_categorical

print("Testing feature engineering...")

# Load data
df = load_nsl_kdd('data/KDDTrain+.txt')
print(f"✓ Data loaded: {df.shape}")

# Feature engineering
df = feature_engineering(df)
print(f"✓ Feature engineering: {df.shape}")

# Create labels
df = create_labels(df)
print(f"✓ Labels created")
print(f"  Attack categories: {df['attack_category'].unique()}")

# Encode categorical
df = encode_categorical(df)
print(f"✓ Encoding done: {df.shape}")

print("\n✅ Feature engineering test passed!")