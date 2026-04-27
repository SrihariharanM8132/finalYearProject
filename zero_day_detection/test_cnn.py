import numpy as np
from src.cnn_model import build_1d_cnn

print("Testing CNN model...")

# Create dummy data
X_dummy = np.random.rand(100, 20)
y_dummy = np.random.randint(0, 5, 100)

# Build model
model = build_1d_cnn(input_shape=20, num_classes=5)
print("✓ CNN model created")

# Test prediction
predictions = model.predict(X_dummy[:10])
print(f"✓ Predictions shape: {predictions.shape}")

# Quick training (1 epoch)
print("\n✓ Testing training (1 epoch)...")
history = model.fit(X_dummy, y_dummy, epochs=1, verbose=0)
print(f"✓ Training works! Loss: {history.history['loss'][0]:.4f}")

print("\n✅ CNN model test passed!")
