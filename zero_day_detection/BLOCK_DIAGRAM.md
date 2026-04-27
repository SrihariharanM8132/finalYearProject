# BLOCK DIAGRAM SPECIFICATION

## Dual-Phase Learning System Architecture

This document provides the detailed block diagram for the project presentation and report.

---

## System Flow Diagram

```
                    ╔═══════════════════════════════════════╗
                    ║       NSL-KDD DATASET INPUT          ║
                    ║   • KDDTrain+.txt (125,973 samples)  ║
                    ║   • KDDTest+.txt (22,544 samples)    ║
                    ╚════════════════╤══════════════════════╝
                                     │
                                     ▼
          ╔═══════════════════════════════════════════════════════╗
          ║    DATA PREPROCESSING & FEATURE ENGINEERING          ║
          ║  ┌────────────────────────────────────────────────┐  ║
          ║  │ • One-hot encoding (protocol, service, flag)   │  ║
          ║  │ • StandardScaler normalization                 │  ║
          ║  │ • Feature extraction (41 → 93 features)        │  ║
          ║  │ • Train-test split preservation                │  ║
          ║  └────────────────────────────────────────────────┘  ║
          ╚════════════════════════╤══════════════════════════════╝
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │                                                   │
         ▼                                                   ▼
╔════════════════════════════╗                  ╔═══════════════════════════╗
║  PHASE 1: SUPERVISED       ║                  ║  PHASE 2: UNSUPERVISED    ║
║  LEARNING (Known Attacks)  ║                  ║  CLUSTERING (Zero-Day)    ║
╠════════════════════════════╣                  ╠═══════════════════════════╣
║                            ║                  ║                           ║
║  ┌──────────────────────┐  ║                  ║  ┌─────────────────────┐  ║
║  │ 1. Random Forest     │  ║                  ║  │ K-Means Clustering  │  ║
║  │    └─ 100 trees      │  ║                  ║  │  └─ K = 50 clusters │  ║
║  │                      │  ║                  ║  └─────────────────────┘  ║
║  │ 2. Neural Network    │  ║                  ║           │               ║
║  │    └─ CNN (3 layers) │  ║                  ║           ▼               ║
║  │                      │  ║                  ║  ┌─────────────────────┐  ║
║  │ 3. Decision Tree     │  ║                  ║  │ Distance Calculation│  ║
║  │    └─ Gini criterion │  ║                  ║  │  d = ||x - c_i||    │  ║
║  │                      │  ║                  ║  └─────────────────────┘  ║
║  │ 4. K-NN              │  ║                  ║           │               ║
║  │    └─ K = 5          │  ║                  ║           ▼               ║
║  │                      │  ║                  ║  ┌─────────────────────┐  ║
║  │ 5. Naive Bayes       │  ║                  ║  │ Threshold Detection │  ║
║  │    └─ Gaussian       │  ║                  ║  │  d > d_min?         │  ║
║  └──────────────────────┘  ║                  ║  │  d_min = (a+b)/2    │  ║
║           │                ║                  ║  └─────────────────────┘  ║
║           ▼                ║                  ║           │               ║
║  ┌──────────────────────┐  ║                  ║           ▼               ║
║  │ Model Evaluation     │  ║                  ║  ┌─────────────────────┐  ║
║  │ • Accuracy: 97-100%  │  ║                  ║  │ Outlier Flagging    │  ║
║  │ • Precision, Recall  │  ║                  ║  │ • Silhouette: 0.54  │  ║
║  │ • F1-Score, ROC-AUC  │  ║                  ║  │ • 2-5% outliers     │  ║
║  └──────────────────────┘  ║                  ║  └─────────────────────┘  ║
║           │                ║                  ║           │               ║
║           │                ║                  ║           │               ║
╚═══════════╪════════════════╝                  ╚═══════════╪═══════════════╝
            │                                               │
            │         OUTPUT: Predictions                   │
            │         + Metrics                             │
            └──────────────────┬────────────────────────────┘
                               │
                               ▼
          ╔═══════════════════════════════════════════════════════╗
          ║   CORRELATION & ZERO-DAY CANDIDATE SELECTION         ║
          ║  ┌────────────────────────────────────────────────┐  ║
          ║  │ • Map cluster IDs to attack class labels       │  ║
          ║  │ • Identify outliers (distance > threshold)     │  ║
          ║  │ • Select zero-day candidates                   │  ║
          ║  │ • Generate correlation table                   │  ║
          ║  └────────────────────────────────────────────────┘  ║
          ╚════════════════════════╤══════════════════════════════╝
                                   │
                                   ▼
          ╔═══════════════════════════════════════════════════════╗
          ║          ONLINE LEARNING VALIDATION                  ║
          ║  ┌────────────────────────────────────────────────┐  ║
          ║  │ • Incremental training with outliers           │  ║
          ║  │ • Re-evaluate model performance                │  ║
          ║  │ • Measure accuracy/F1-Score change             │  ║
          ║  │ • Confirm zero-day detection effectiveness     │  ║
          ║  └────────────────────────────────────────────────┘  ║
          ╚════════════════════════╤══════════════════════════════╝
                                   │
                                   ▼
          ╔═══════════════════════════════════════════════════════╗
          ║       ZERO-DAY INTRUSION ALERTS & REPORTS            ║
          ║  ┌────────────────────────────────────────────────┐  ║
          ║  │ Outputs:                                       │  ║
          ║  │ • Performance metrics dashboard                │  ║
          ║  │ • Confusion matrices and ROC curves            │  ║
          ║  │ • Zero-day candidate list                      │  ║
          ║  │ • Cluster analysis tables                      │  ║
          ║  │ • Interactive Streamlit dashboard              │  ║
          ║  │ • Alert notifications for anomalies            │  ║
          ║  └────────────────────────────────────────────────┘  ║
          ╚═══════════════════════════════════════════════════════╝
```

---

## Simplified Presentation Version

For PowerPoint slides, use this simplified version:

```
         NSL-KDD Dataset
               ↓
    Preprocessing & Feature Engineering
               ↓
         ┌─────┴─────┐
         │           │
    PHASE 1      PHASE 2
    Supervised   Unsupervised
    Learning     Clustering
         │           │
    5 ML Models  K-Means (K=50)
         │           │
    Predictions  Outlier Detection
         │           │
         └─────┬─────┘
               ↓
       Correlation Analysis
               ↓
    Online Learning Validation
               ↓
    Zero-Day Detection Results
```

---

## Component Details for Diagram

### Input Layer
- **Dataset**: NSL-KDD (125,973 train + 22,544 test samples)
- **Features**: 41 original attributes per network connection

### Preprocessing Layer
- **Encoding**: One-hot for categorical (protocol_type, service, flag)
- **Scaling**: StandardScaler for numerical features
- **Engineering**: Statistical, temporal, and interaction features

### Phase 1: Supervised Learning
- **Models**: 5 classifiers (RF, CNN, DT, KNN, NB)
- **Training**: Fit on labeled training data
- **Evaluation**: Accuracy, Precision, Recall, F1, ROC-AUC
- **Output**: Class predictions (Normal, DoS, Probe, R2L, U2R)

### Phase 2: Unsupervised Clustering
- **Algorithm**: K-Means with K=50
- **Distance Metric**: Euclidean distance to cluster centroids
- **Threshold**: d_min = (intra-cluster + inter-cluster distance) / 2
- **Output**: Outlier flags for samples with distance > d_min

### Integration Layer
- **Correlation**: Map cluster assignments to predicted classes
- **Selection**: Identify zero-day candidates from outliers
- **Validation**: Online learning experiment with flagged samples

### Output Layer
- **Metrics**: Comprehensive performance tables
- **Visualizations**: Plots, charts, confusion matrices
- **Dashboard**: Interactive Streamlit interface
- **Alerts**: Zero-day attack notifications

---

## Color Coding for Presentation

- **Blue**: Input and preprocessing stages
- **Green**: Phase 1 (Supervised Learning)
- **Orange**: Phase 2 (Unsupervised Clustering)
- **Purple**: Integration and correlation
- **Red**: Output and alerts

---

## Figure Caption for Report

**Figure 1: Dual-Phase Learning System Architecture for Zero-Day Intrusion Detection**

*The proposed system architecture consists of two parallel processing phases: Phase 1 employs five supervised learning models (Random Forest, CNN, Decision Tree, KNN, Naive Bayes) for known attack classification, achieving 97-100% accuracy; Phase 2 uses K-Means clustering (K=50) with distance-based outlier detection to identify potential zero-day attacks. The two phases are integrated through correlation analysis, and zero-day detection effectiveness is validated through online learning experiments.*

---

## Implementation in PowerPoint

1. **Use SmartArt**: Select "Process" or "Hierarchy" layouts
2. **Add Icons**: Use security shield, database, cloud, gear icons
3. **Color Scheme**: Blue → Green/Orange → Purple → Red gradient
4. **Animations**: 
   - Entry: Fade in from left for sequential blocks
   - Emphasis: Pulse for Phase 1 and Phase 2 blocks
   - Path: Arrow paths showing data flow

---

## Alternative Horizontal Layout

```
┌────────────┐    ┌──────────┐    ┌─────────────┐    ┌──────────┐    ┌────────┐
│  NSL-KDD   │───▶│ Preproc. │───▶│   Phase 1   │───▶│Correlation│───▶│ Alerts │
│  Dataset   │    │ Feature  │    │  Supervised │    │  Online   │    │Results │
└────────────┘    │  Eng.    │    │  Learning   │    │ Learning  │    └────────┘
                  └────┬─────┘    └─────────────┘    └────▲──────┘
                       │                                   │
                       └───▶│   Phase 2   │───────────────┘
                            │Unsupervised │
                            │ Clustering  │
                            └─────────────┘
```

---

**Author**: Srihariharan M  
**Date**: December 15, 2025  
**Purpose**: Project presentation and report illustration
