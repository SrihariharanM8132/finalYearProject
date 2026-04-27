# Two-Phase Zero-Day Detection System

## Overview

This system implements a two-phase approach for detecting both known attacks and zero-day intrusions:

- **Phase 1**: Autoencoder trained on Normal traffic → Detects anomalies as potential zero-day attacks
- **Phase 2**: Random Forest classifier → Classifies known attacks into families (DoS, Probe, R2L, U2R)

## Architecture

```
Input Traffic
     ↓
┌─────────────────────────┐
│   Phase 1: Autoencoder  │
│  (Anomaly Detection)    │
└─────────────────────────┘
     ↓
Reconstruction Error > Threshold?
     ↓
   YES ──→ Flag as ZERO-DAY
     ↓
    NO
     ↓
┌─────────────────────────┐
│ Phase 2: Random Forest  │
│ (Attack Classification) │
└─────────────────────────┘
     ↓
Classify: DoS, Probe, R2L, U2R, Normal
```

## Quick Start

### 1. Train Phase 1 (Autoencoder)

```bash
python train_autoencoder.py
```

**Output:**
- `models/autoencoder_phase1.h5` - Trained autoencoder model
- `models/autoencoder_threshold.json` - Anomaly detection threshold
- `models/autoencoder_scaler.pkl` - Feature scaler
- `results/autoencoder_training_loss.png` - Training curves

### 2. Train Phase 2 (Random Forest)

```bash
python train_phase2_classifier.py
```

**Output:**
- `models/rf_phase2.pkl` - Trained Random Forest model
- `models/phase2_scaler.pkl` - Feature scaler
- `results/phase2_confusion_matrix.png` - Classification performance
- `results/phase2_feature_importance.png` - Feature importance

### 3. Run Integrated Pipeline

```bash
python two_phase_pipeline.py
```

**Output:**
- `results/two_phase_results.csv` - Detection results for all test samples
- `results/two_phase_reconstruction_analysis.png` - Reconstruction error analysis
- `results/two_phase_confusion_matrix.png` - Overall confusion matrix
- `results/two_phase_flow.png` - Detection flow visualization

## File Structure

```
zero_day_detection/
├── src/
│   ├── autoencoder_model.py       # Phase 1: Autoencoder class
│   ├── attack_classifier.py       # Phase 2: Random Forest class
│   ├── load_data.py               # Data loading utilities
│   └── feature_engineering.py     # Feature preprocessing
│
├── train_autoencoder.py           # Train Phase 1
├── train_phase2_classifier.py     # Train Phase 2
├── two_phase_pipeline.py          # Integrated detection pipeline
│
├── models/                        # Saved models
│   ├── autoencoder_phase1.h5
│   ├── autoencoder_threshold.json
│   ├── rf_phase2.pkl
│   └── *.pkl, *.json (scalers, features)
│
└── results/                       # Output results and plots
```

## How It Works

### Phase 1: Autoencoder (Zero-Day Detection)

1. **Training**: Learns to reconstruct only Normal traffic patterns
2. **Detection**: Calculates reconstruction error for input traffic
3. **Threshold**: If error > threshold → Anomaly (potential zero-day)

**Key Parameters:**
- Architecture: 64 → 32 → 16 → 8 (bottleneck) → 16 → 32 → 64
- Threshold: mean + 3×std of reconstruction errors on normal data
- Loss: Mean Squared Error (MSE)

### Phase 2: Random Forest (Attack Classification)

1. **Training**: Learns patterns of known attack families
2. **Classification**: Predicts attack category for non-anomalous traffic
3. **Output**: DoS, Probe, R2L, U2R, or Normal

**Key Parameters:**
- Trees: 100
- Max depth: 20
- Features: Network traffic features from NSL-KDD

## Results Interpretation

### Two-Phase Results CSV

| Column | Description |
|--------|-------------|
| `reconstruction_error` | MSE from Phase 1 autoencoder |
| `phase1_anomaly` | 1 = anomaly, 0 = normal |
| `final_prediction` | ZERO-DAY or attack family |
| `true_label` | Ground truth label |

### Example Output

```
Final Detection Summary:
  normal: 9,711 (43.1%)
  dos: 7,458 (33.1%)
  probe: 2,421 (10.7%)
  ZERO-DAY: 2,156 (9.6%)
  r2l: 741 (3.3%)
  u2r: 57 (0.3%)
```

## Customization

### Adjust Phase 1 Threshold

Edit `models/autoencoder_threshold.json`:
```json
{
  "threshold": 0.05,  // Lower = more sensitive (more zero-days)
  "input_dim": 93,
  "encoding_dim": 8
}
```

### Modify Autoencoder Architecture

In `src/autoencoder_model.py`, change layer sizes:
```python
encoded = layers.Dense(128, activation='relu')(encoder_input)  # Increase capacity
bottleneck = layers.Dense(16, ...)  # Larger bottleneck
```

### Tune Random Forest

In `train_phase2_classifier.py`:
```python
classifier = AttackClassifier(
    n_estimators=200,    # More trees
    max_depth=30,        # Deeper trees
    random_state=42
)
```

## Performance Metrics

- **Phase 1**: Detects anomalies with configurable sensitivity
- **Phase 2**: ~97-99% accuracy on known attack classification
- **Overall**: Combines strengths of both supervised and unsupervised learning

## Requirements

```
tensorflow>=2.10.0
scikit-learn>=1.0.0
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
joblib>=1.0.0
```

## Troubleshooting

**Issue**: Model files not found  
**Solution**: Run training scripts first (`train_autoencoder.py`, `train_phase2_classifier.py`)

**Issue**: Feature dimension mismatch  
**Solution**: Ensure same preprocessing pipeline for training and testing

**Issue**: Too many zero-days detected  
**Solution**: Increase threshold in `autoencoder_threshold.json`

## Citation

If using this system, please reference:
- NSL-KDD Dataset
- Two-phase learning approach for intrusion detection
- Autoencoder-based anomaly detection
