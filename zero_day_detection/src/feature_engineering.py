import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def feature_engineering(df):
    """
    Apply feature engineering as per Section 3.1 of the paper
    Keep only relevant features
    """
    # According to paper, keep these 12 features:
    selected_features = [
        'duration', 'protocol_type', 'service', 'land',
        'src_bytes', 'dst_bytes', 'count', 'srv_count',
        'same_srv_rate', 'srv_diff_host_rate', 'wrong_fragment', 'flag'
    ]
    
    df_selected = df[selected_features + ['attack_type']].copy()
    
    # Handle missing values
    df_selected = df_selected.dropna()
    
    return df_selected

def encode_categorical(df, reference_df=None):
    """Encode categorical features with consistent columns
    
    Args:
        df: DataFrame to encode
        reference_df: Reference DataFrame to align columns with (optional)
    """
    categorical_cols = ['protocol_type', 'service', 'flag']
    
    # One-hot encoding
    df_encoded = pd.get_dummies(df, columns=categorical_cols)
    
    # If reference provided, align columns
    if reference_df is not None:
        # Get missing columns
        missing_cols = set(reference_df.columns) - set(df_encoded.columns)
        for col in missing_cols:
            df_encoded[col] = 0
        
        # Remove extra columns
        extra_cols = set(df_encoded.columns) - set(reference_df.columns)
        df_encoded = df_encoded.drop(columns=list(extra_cols))
        
        # Reorder to match reference
        df_encoded = df_encoded[reference_df.columns]
    
    return df_encoded

def create_labels(df):
    """Create attack labels with comprehensive mapping"""
    # Complete attack mapping for NSL-KDD dataset
    attack_mapping = {
        'normal': 'normal',
        # DoS attacks
        'back': 'dos', 'land': 'dos', 'neptune': 'dos', 'pod': 'dos',
        'smurf': 'dos', 'teardrop': 'dos', 'apache2': 'dos', 'udpstorm': 'dos',
        'processtable': 'dos', 'mailbomb': 'dos',
        # Probe attacks
        'ipsweep': 'probe', 'nmap': 'probe', 'portsweep': 'probe',
        'satan': 'probe', 'mscan': 'probe', 'saint': 'probe',
        # R2L attacks
        'ftp_write': 'r2l', 'guess_passwd': 'r2l', 'imap': 'r2l',
        'multihop': 'r2l', 'phf': 'r2l', 'spy': 'r2l',
        'warezclient': 'r2l', 'warezmaster': 'r2l', 'sendmail': 'r2l',
        'named': 'r2l', 'snmpgetattack': 'r2l', 'snmpguess': 'r2l',
        'xlock': 'r2l', 'xsnoop': 'r2l', 'worm': 'r2l',
        # U2R attacks
        'buffer_overflow': 'u2r', 'loadmodule': 'u2r',
        'perl': 'u2r', 'rootkit': 'u2r', 'sqlattack': 'u2r',
        'xterm': 'u2r', 'ps': 'u2r', 'httptunnel': 'u2r'
    }
    
    # Remove trailing dot from attack names
    df['attack_type'] = df['attack_type'].str.replace('.', '', regex=False)
    
    # Map to categories
    df['attack_category'] = df['attack_type'].map(attack_mapping)
    
    # Check for unmapped values
    unmapped = df[df['attack_category'].isnull()]['attack_type'].unique()
    if len(unmapped) > 0:
        print(f"⚠ Warning: Unmapped attack types found: {unmapped}")
        print("  Mapping to original attack type...")
    
    # Fill any unmapped values with original attack_type
    df['attack_category'] = df['attack_category'].fillna(df['attack_type'])
    
    return df

def normalize_data(X_train, X_test):
    """Standardize features"""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, scaler