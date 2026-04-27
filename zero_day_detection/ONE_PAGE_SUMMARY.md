# 🎓 ONE-PAGE PROJECT SUMMARY
**For Quick Reference During Presentation**

---

## Project Title
**Dual-Phase Learning Approach for Zero-Day Intrusion Detection Using NSL-KDD**

---

## System Overview
Two-phase machine learning system combining:
- **Phase 1**: Autoencoder (unsupervised) → Zero-day detection
- **Phase 2**: Random Forest (supervised) → Attack classification

---

## Dataset
- **Name**: NSL-KDD
- **Training**: 125,973 samples
- **Testing**: 22,544 samples
- **Features**: 93 (engineered from 41 original)
- **Classes**: Normal, DoS, Probe, R2L, U2R

---

## Phase 1: Autoencoder
- **Architecture**: 64→32→16→8→16→32→64
- **Training Data**: 67,343 normal samples ONLY
- **Loss Function**: Mean Squared Error (MSE)
- **Threshold**: 28.119 (mean + 3×std)
- **Purpose**: Detect anomalies as potential zero-day attacks
- **Result**: Flags 445 samples (1.97%) as zero-day

---

## Phase 2: Random Forest
- **Algorithm**: Random Forest Classifier
- **Configuration**: 100 trees, max depth 20
- **Training Data**: All 125,973 samples (all classes)
- **Purpose**: Classify known attacks into families
- **Classes**: DoS, Probe, R2L, U2R, Normal

---

## Pipeline Flow
```
Input Traffic
    ↓
Phase 1: Calculate Reconstruction Error
    ↓
Error > 28.119?
    ↓
YES → Flag as ZERO-DAY
    ↓
NO → Phase 2: Classify Attack Type
```

---

## Results (on 22,544 test samples)

| Metric | Value |
|--------|-------|
| **Overall Accuracy** | **72.81%** |
| **False Positive Rate** | **3.54%** |
| **DoS Detection** | **75.30%** |
| **Probe Detection** | **57.54%** |
| R2L Detection | 1.23% |
| U2R Detection | 2.00% |

---

## Key Achievements
✅ Successfully trained autoencoder on normal traffic only  
✅ Implemented threshold-based zero-day detection  
✅ Achieved low false positive rate (3.54%)  
✅ Strong performance on DoS attacks (75.30%)  
✅ Generated comprehensive evaluation metrics  
✅ Created 8+ visualizations and reports  

---

## Files Generated
- **Models**: 6 trained models (autoencoder, RF, scalers)
- **Results**: 22,544 predictions in CSV
- **Visualizations**: Confusion matrix, detection rates, feature importance
- **Documentation**: Complete technical documentation

---

## Technologies Used
- **Python 3.x**
- **TensorFlow/Keras** (autoencoder)
- **Scikit-learn** (Random Forest, preprocessing)
- **Pandas, NumPy** (data processing)
- **Matplotlib, Seaborn** (visualization)

---

## Innovation
**Dual-phase approach** that combines:
1. Unsupervised learning for unknown threats
2. Supervised learning for known attack classification

This allows detection of both **known attacks** AND **zero-day threats**.

---

## Quick Demo Commands
```bash
# Run full evaluation
python evaluate_system.py

# Launch demo interface
python demo_for_guide.py

# View results
start results\confusion_matrix.png
```

---

**Student**: Srihariharan M  
**Roll No**: 9047258132  
**Date**: January 5, 2026
