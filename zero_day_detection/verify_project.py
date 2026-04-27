"""
Quick verification script to test project setup
"""

import sys
import os

def test_imports():
    """Test all module imports"""
    print("Testing module imports...")
    print("="*60)
    
    try:
        import numpy as np
        print("✓ NumPy")
    except ImportError as e:
        print(f"✗ NumPy: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas")
    except ImportError as e:
        print(f"✗ Pandas: {e}")
        return False
    
    try:
        import sklearn
        print("✓ Scikit-learn")
    except ImportError as e:
        print(f"✗ Scikit-learn: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ Matplotlib")
    except ImportError as e:
        print(f"✗ Matplotlib: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✓ Seaborn")
    except ImportError as e:
        print(f"✗ Seaborn: {e}")
        return False
    
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow {tf.__version__}")
    except ImportError as e:
        print(f"✗ TensorFlow: {e}")
        return False
    
    try:
        from tqdm import tqdm
        print("✓ tqdm")
    except ImportError as e:
        print(f"✗ tqdm: {e}")
        return False
    
    print("\n✓ All dependencies installed successfully!")
    return True

def test_project_modules():
    """Test project module imports"""
    print("\nTesting project modules...")
    print("="*60)
    
    try:
        from src.load_data import load_nsl_kdd
        print("✓ load_data")
    except ImportError as e:
        print(f"✗ load_data: {e}")
        return False
    
    try:
        from src.feature_engineering import feature_engineering
        print("✓ feature_engineering")
    except ImportError as e:
        print(f"✗ feature_engineering: {e}")
        return False
    
    try:
        from src.cnn_model import build_1d_cnn
        print("✓ cnn_model")
    except ImportError as e:
        print(f"✗ cnn_model: {e}")
        return False
    
    try:
        from src.boosting_models import BoostingEnsemble
        print("✓ boosting_models")
    except ImportError as e:
        print(f"✗ boosting_models: {e}")
        return False
    
    try:
        from src.clustering import ZeroDayClustering
        print("✓ clustering")
    except ImportError as e:
        print(f"✗ clustering: {e}")
        return False
    
    try:
        from src.correlation import CorrelationTable
        print("✓ correlation")
    except ImportError as e:
        print(f"✗ correlation: {e}")
        return False
    
    try:
        from src.zero_day_detection import ZeroDayDetector
        print("✓ zero_day_detection")
    except ImportError as e:
        print(f"✗ zero_day_detection: {e}")
        return False
    
    try:
        from src.visualize import FrameworkVisualizer
        print("✓ visualize")
    except ImportError as e:
        print(f"✗ visualize: {e}")
        return False
    
    print("\n✓ All project modules loaded successfully!")
    return True

def test_dataset():
    """Test dataset files"""
    print("\nTesting dataset files...")
    print("="*60)
    
    train_file = "data/KDDTrain+.txt"
    test_file = "data/KDDTest+.txt"
    
    if os.path.exists(train_file):
        size_mb = os.path.getsize(train_file) / (1024 * 1024)
        print(f"✓ Training dataset found ({size_mb:.2f} MB)")
    else:
        print(f"✗ Training dataset not found: {train_file}")
        return False
    
    if os.path.exists(test_file):
        size_mb = os.path.getsize(test_file) / (1024 * 1024)
        print(f"✓ Test dataset found ({size_mb:.2f} MB)")
    else:
        print(f"✗ Test dataset not found: {test_file}")
        return False
    
    print("\n✓ All dataset files present!")
    return True

def test_directories():
    """Test/create required directories"""
    print("\nChecking directories...")
    print("="*60)
    
    dirs = ['results', 'results/plots', 'models']
    
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"✓ Created: {dir_path}")
        else:
            print(f"✓ Exists: {dir_path}")
    
    print("\n✓ All directories ready!")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("ZERO-DAY DETECTION FRAMEWORK - SETUP VERIFICATION")
    print("="*60 + "\n")
    
    all_passed = True
    
    # Test dependencies
    if not test_imports():
        all_passed = False
        print("\n⚠ Some dependencies are missing!")
        print("Run: pip install -r requirements.txt")
    
    # Test project modules
    if not test_project_modules():
        all_passed = False
        print("\n⚠ Some project modules failed to load!")
    
    # Test dataset
    if not test_dataset():
        all_passed = False
        print("\n⚠ Dataset files are missing!")
    
    # Test directories
    if not test_directories():
        all_passed = False
    
    # Final result
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED - PROJECT IS READY!")
        print("="*60)
        print("\nYou can now run:")
        print("  python main.py          - Full pipeline")
        print("  python demo_interactive.py - Interactive demo")
    else:
        print("✗ SOME TESTS FAILED - PLEASE FIX ISSUES ABOVE")
        print("="*60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
