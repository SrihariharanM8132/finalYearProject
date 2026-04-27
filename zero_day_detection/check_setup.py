import os
import sys

def check_setup():
    """Check if everything is ready to run the project"""
    
    print("="*60)
    print("SETUP VERIFICATION")
    print("="*60)
    
    checks_passed = 0
    total_checks = 6
    
    # Check 1: Python version
    print("\n[1/6] Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} (OK)")
        checks_passed += 1
    else:
        print(f"✗ Python {sys.version_info.major}.{sys.version_info.minor} (Need 3.8+)")
    
    # Check 2: Required packages
    print("\n[2/6] Checking required packages...")
    required_packages = ['numpy', 'pandas', 'tensorflow', 'sklearn', 'matplotlib', 'seaborn']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (MISSING)")
            missing.append(package)
    
    if not missing:
        checks_passed += 1
    else:
        print(f"\n  Install missing packages: pip install {' '.join(missing)}")
    
    # Check 3: Folder structure
    print("\n[3/6] Checking folder structure...")
    required_folders = ['data', 'src', 'results', 'notebooks', 'tests']
    folders_ok = True
    
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"  ✓ {folder}/")
        else:
            print(f"  ✗ {folder}/ (MISSING)")
            folders_ok = False
    
    if folders_ok:
        checks_passed += 1
    
    # Check 4: Source files
    print("\n[4/6] Checking source files...")
    required_files = [
        'src/load_data.py',
        'src/feature_engineering.py',
        'src/cnn_model.py',
        'src/boosting_models.py',
        'src/clustering.py',
        'src/correlation.py',
        'src/zero_day_detection.py'
    ]
    files_ok = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (MISSING)")
            files_ok = False
    
    if files_ok:
        checks_passed += 1
    
    # Check 5: Dataset files
    print("\n[5/6] Checking dataset...")
    dataset_files = ['data/KDDTrain+.txt', 'data/KDDTest+.txt']
    dataset_ok = False
    
    for file in dataset_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✓ {file} ({size:,} bytes)")
            dataset_ok = True
        else:
            print(f"  ⚠ {file} (Not found)")
    
    if dataset_ok:
        checks_passed += 1
        print("  ✓ At least one dataset file exists")
    else:
        print("  ✗ No dataset files found!")
    
    # Check 6: Main file
    print("\n[6/6] Checking main.py...")
    if os.path.exists('main.py'):
        print(f"  ✓ main.py exists")
        checks_passed += 1
    else:
        print(f"  ✗ main.py (MISSING)")
    
    # Summary
    print("\n" + "="*60)
    print(f"RESULT: {checks_passed}/{total_checks} checks passed")
    print("="*60)
    
    if checks_passed == total_checks:
        print("\n🎉 All checks passed! You're ready to run the project!")
        return True
    else:
        print(f"\n⚠ {total_checks - checks_passed} issues found. Please fix them first.")
        return False

if __name__ == "__main__":
    check_setup()