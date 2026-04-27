import pandas as pd
import numpy as np

# Column names for NSL-KDD
columns = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes',
           'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
           'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
           'su_attempted', 'num_root', 'num_file_creations', 'num_shells',
           'num_access_files', 'num_outbound_cmds', 'is_host_login',
           'is_guest_login', 'count', 'srv_count', 'serror_rate',
           'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
           'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
           'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
           'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
           'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
           'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
           'dst_host_srv_rerror_rate', 'attack_type', 'difficulty']

def load_nsl_kdd(filepath):
    """Load NSL-KDD dataset with validation"""
    try:
        df = pd.read_csv(filepath, names=columns)
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {filepath}")
    except Exception as e:
        raise Exception(f"Error loading dataset: {str(e)}")
    
    # Remove difficulty column
    df = df.drop(['difficulty'], axis=1)
    
    # Print detailed info
    print(f"\n{'='*60}")
    print(f"Dataset loaded: {filepath}")
    print(f"{'='*60}")
    print(f"Shape: {df.shape[0]:,} samples × {df.shape[1]} features")
    print(f"Unique attack types: {df['attack_type'].nunique()}")
    print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    if missing > 0:
        print(f"⚠ Warning: {missing} missing values detected")
    else:
        print("✓ No missing values")
    
    return df

# Test it
if __name__ == "__main__":
    train_data = load_nsl_kdd('../data/KDDTrain+.txt')
    print(train_data.head())