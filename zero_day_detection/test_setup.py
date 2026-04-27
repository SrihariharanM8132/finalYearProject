import sys
print("Python version:", sys.version)

try:
    import numpy as np
    print("✓ NumPy installed")
    import pandas as pd
    print("✓ Pandas installed")
    import tensorflow as tf
    print("✓ TensorFlow installed")
    import sklearn
    print("✓ Scikit-learn installed")
    print("\n✅ All packages installed successfully!")
except ImportError as e:
    print(f"❌ Error: {e}")