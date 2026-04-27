# PROJECT SYNOPSIS

## DUAL-PHASE LEARNING APPROACH FOR ZERO-DAY INTRUSION DETECTION USING NSL-KDD

---

**Student:** Srihariharan M  
**Roll No:** 9047258132  
**Guide:** Archana P / AP-CSE  
**Institution:** [Your College Name]  
**Department:** Computer Science and Engineering

---

## ABSTRACT

This project presents a dual-phase learning approach for detecting zero-day intrusions using the NSL-KDD dataset. In Phase 1, multiple supervised models, including Random Forest, CNN, Decision Tree, KNN and Naive Bayes, classify normal and known attack traffic with high accuracy. In Phase 2, K-Means clustering models traffic behaviour and identifies distant outliers as zero-day candidates, which are validated through an online learning experiment. By correlating cluster assignments and classifier outputs, the system distinguishes new attack behaviours from normal anomalies, improving zero-day detection capability while maintaining strong performance on known intrusions.

---

## 1. PROBLEM DEFINITION / EXISTING SYSTEM

### 1.1 Problem Statement

Existing Intrusion Detection Systems (IDS) detect known attacks well but struggle with zero-day intrusions that do not match stored signatures or training patterns. Machine-learning based IDS improve accuracy, yet most models are trained as a single-phase classifier and cannot clearly separate normal/known attacks from novel behaviours, leading to missed zero-day flows or many false alarms on NSL-KDD-like traffic.

### 1.2 Limitations of Existing Systems

1. **Signature-Based Limitations**: Traditional IDS rely on known attack signatures and fail to detect novel attack patterns
2. **Single-Phase Classification**: Most ML-based IDS use only supervised learning, which cannot identify previously unseen attack types
3. **High False Alarm Rate**: Systems struggle to distinguish between legitimate anomalies and actual zero-day attacks
4. **Training Data Dependency**: Models can only detect attacks similar to those seen during training
5. **Delayed Response**: Zero-day attacks often go undetected until new signatures are created and deployed

### 1.3 Need for Dual-Phase Approach

- **Zero-day attacks** are a major risk and are not caught by signature-based IDS
- **NSL-KDD dataset** is still widely used to benchmark ML-based IDS, but many works only report accuracy on known attacks
- A clear **two-phase pipeline** (known-attack classification + zero-day discovery) helps students and practitioners understand, implement and extend research frameworks in a reproducible way

---

## 2. LITERATURE SURVEY

### 2.1 Base Papers Overview

#### Primary Base Paper

**A. Touré et al.**, "A framework for detecting zero-day exploits in network flows," *Computer Networks*, vol. 248, 110476, 2024.

**Key Contributions:**
- Proposes a hybrid framework combining supervised learning, clustering and online learning
- Focuses specifically on zero-day exploit detection in network flows
- Demonstrates the effectiveness of multi-phase approaches for novel attack detection

#### Supporting Papers

**S. Chawla and P. Banerjee**, "Hybrid approach for intrusion detection model using combination of K-means clustering with machine learning classifiers," *IJES*, vol. 6, no. 1, pp. 93–97, 2017.

**Key Contributions:**
- Introduces hybrid IDS combining K-Means clustering with ML classifiers (RF, SVM)
- Shows improved detection accuracy through clustering-based feature extraction
- Validates approach on standard intrusion detection datasets

**A. J. Nugroho et al.**, "A hybrid intrusion detection system with K-means and CNN+LSTM on NSL-KDD dataset," *EAI Endorsed Transactions on Security and Safety*, 2024.

**Key Contributions:**
- Implements hybrid IDS specifically on NSL-KDD dataset
- Combines K-Means clustering with deep learning (CNN/LSTM)
- Demonstrates state-of-the-art performance on multi-class intrusion detection

### 2.2 Comparative Analysis

| Aspect | Touré et al. (2024) | Chawla & Banerjee (2017) | Nugroho et al. (2024) | **Our Approach** |
|--------|---------------------|--------------------------|------------------------|------------------|
| **Dataset** | Network flows | Standard IDS datasets | NSL-KDD | **NSL-KDD** |
| **Methods** | Supervised + Clustering + Online Learning | K-Means + RF/SVM | K-Means + CNN/LSTM | **5 ML Models + K-Means + Online Learning** |
| **Zero-Day Handling** | ✅ Explicit zero-day detection | ⚠️ Implicit anomaly detection | ⚠️ Limited zero-day focus | **✅ Explicit dual-phase zero-day detection** |
| **Supervised Models** | Limited details | RF, SVM | CNN, LSTM | **RF, CNN, DT, KNN, NB** |
| **Clustering** | Yes | Yes | Yes | **Yes (50 clusters)** |
| **Online Learning** | ✅ Yes | ❌ No | ❌ No | **✅ Yes (validation phase)** |
| **Evaluation Metrics** | Basic accuracy | Accuracy, Precision, Recall | Accuracy, F1-Score | **Accuracy, Precision, Recall, F1, ROC-AUC** |

### 2.3 Research Gap Addressed

While existing works demonstrate the effectiveness of hybrid approaches for intrusion detection, they lack:

1. **Clear separation** between known-attack classification and zero-day discovery phases
2. **Comprehensive model comparison** across multiple supervised learning algorithms
3. **Validation mechanism** for zero-day candidates through online learning
4. **Reproducible implementation** with detailed documentation for educational purposes

Our work adapts and extends the hybrid direction proposed by Touré et al., implementing a clear dual-phase learning approach with comprehensive evaluation on the NSL-KDD benchmark dataset.

---

## 3. PROPOSED SYSTEM

### 3.1 System Overview

The proposed system implements a **dual-phase learning approach** that combines the strengths of supervised and unsupervised learning to detect both known attacks and zero-day intrusions.

### 3.2 Phase 1: Supervised Learning for Known Attacks

**Objective:** Classify network traffic into normal and known attack categories with high accuracy

**Models Implemented:**
1. **Random Forest (RF)** - Ensemble of decision trees for robust classification
2. **Convolutional Neural Network (CNN)** - Deep learning for pattern recognition
3. **Decision Tree (DT)** - Rule-based transparent classifier
4. **K-Nearest Neighbors (KNN)** - Distance-based instance learning
5. **Naive Bayes (NB)** - Probabilistic Bayesian classifier

**Output:** Predicted class labels (Normal, DoS, Probe, R2L, U2R) with performance metrics

### 3.3 Phase 2: Unsupervised Learning for Zero-Day Detection

**Objective:** Identify previously unseen attack patterns through clustering and outlier analysis

**Approach:**
1. **K-Means Clustering** - Group similar network traffic patterns into 50 clusters
2. **Distance Calculation** - Compute distance from each sample to its cluster centroid
3. **Threshold Detection** - Flag samples exceeding distance threshold as potential zero-day attacks
4. **Correlation Analysis** - Map cluster assignments to supervised model predictions
5. **Online Learning Validation** - Incrementally retrain models with detected outliers

**Output:** Zero-day candidate flows with validation metrics

### 3.4 Key Innovations

1. **Multi-Model Ensemble**: Five diverse supervised models for robust known-attack detection
2. **Outlier-Based Zero-Day Detection**: Statistical approach using cluster distance thresholds
3. **Correlation Framework**: Novel mapping between clustering and classification results
4. **Online Learning Validation**: Experimental validation of zero-day detection effectiveness
5. **Comprehensive Metrics**: Full evaluation with Precision, Recall, F1-Score, and ROC-AUC

---

## 4. PROJECT REQUIREMENTS

### 4.1 Why This Project is Needed

#### 4.1.1 Security Perspective
- Zero-day attacks exploit previously unknown vulnerabilities and pose significant security risks
- Traditional signature-based IDS cannot detect attacks without prior knowledge
- Real-time detection of novel attack patterns is critical for network security

#### 4.1.2 Research Perspective
- NSL-KDD remains a widely-used benchmark for evaluating ML-based IDS
- Most existing works focus only on accuracy for known attacks
- Limited research on explicit zero-day detection with validation mechanisms

#### 4.1.3 Educational Perspective
- A clear two-phase pipeline helps students understand hybrid IDS architectures
- Reproducible implementation enables practitioners to extend research frameworks
- Comprehensive documentation serves as learning resource for ML-based security systems

### 4.2 Functional Requirements

#### 4.2.1 Input Requirements
- **NSL-KDD Training Dataset**: KDDTrain+.txt (125,973 samples)
- **NSL-KDD Test Dataset**: KDDTest+.txt (22,544 samples)
- **Feature Set**: 41 original features + engineered features (93 total)

#### 4.2.2 Processing Requirements

**Phase 1: Supervised Learning**
1. Data preprocessing and feature engineering
2. Train five supervised learning models
3. Evaluate models on test data
4. Generate comprehensive performance metrics

**Phase 2: Unsupervised Learning**
1. Apply K-Means clustering on test data
2. Calculate sample-to-centroid distances
3. Identify and mark outliers as zero-day candidates
4. Correlate clustering results with classification predictions
5. Perform online learning validation

#### 4.2.3 Output Requirements
1. **Performance Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC per model
2. **Classification Results**: Predicted labels for all test samples
3. **Zero-Day Candidates**: List of samples flagged as potential zero-day attacks
4. **Cluster Analysis**: Silhouette score, cluster purity, size distribution
5. **Visualizations**: Confusion matrices, ROC curves, cluster distributions
6. **Online Learning Results**: Accuracy changes after incremental training

### 4.3 Non-Functional Requirements

1. **Performance**: Process 22,544 test samples in < 5 minutes
2. **Accuracy**: > 95% accuracy on known attack classification
3. **Scalability**: Handle larger datasets with minimal code changes
4. **Reproducibility**: Consistent results with fixed random seeds
5. **Documentation**: Comprehensive code comments and user guides

---

## 5. COST AND TIME ESTIMATION

### 5.1 Hardware Requirements

| Component | Specification | Cost |
|-----------|---------------|------|
| Processor | Intel i5/i7 or equivalent | Existing lab PC |
| RAM | 8-16 GB | No additional cost |
| Storage | 10 GB free space | Available |
| **Total Hardware Cost** | | **₹0** (Using existing resources) |

### 5.2 Software Requirements

| Software | Purpose | Cost |
|----------|---------|------|
| Python 3.8+ | Programming language | Free (Open-source) |
| scikit-learn | ML algorithms | Free (Open-source) |
| TensorFlow/Keras | Deep learning (CNN) | Free (Open-source) |
| Pandas, NumPy | Data processing | Free (Open-source) |
| Matplotlib, Plotly | Visualization | Free (Open-source) |
| Streamlit | Dashboard | Free (Open-source) |
| Jupyter/VS Code | Development environment | Free (Open-source) |
| **Total Software Cost** | | **₹0** (All open-source) |

### 5.3 Time Estimation

| Task | Estimated Hours | Notional Cost @ ₹300/hr |
|------|----------------|-------------------------|
| **1. Data Preprocessing & EDA** | 20 hours | ₹6,000 |
| - Dataset loading and cleaning | 5 hours | ₹1,500 |
| - Feature engineering | 8 hours | ₹2,400 |
| - Exploratory data analysis | 7 hours | ₹2,100 |
| **2. Model Training & Tuning** | 25 hours | ₹7,500 |
| - Supervised model implementation | 12 hours | ₹3,600 |
| - Hyperparameter tuning | 8 hours | ₹2,400 |
| - Model evaluation | 5 hours | ₹1,500 |
| **3. Clustering & Zero-Day Detection** | 25 hours | ₹7,500 |
| - K-Means implementation | 8 hours | ₹2,400 |
| - Outlier detection algorithm | 10 hours | ₹3,000 |
| - Online learning validation | 7 hours | ₹2,100 |
| **4. Visualization & Dashboard** | 15 hours | ₹4,500 |
| - Plot generation | 7 hours | ₹2,100 |
| - Interactive dashboard | 8 hours | ₹2,400 |
| **5. Documentation & Presentation** | 30 hours | ₹9,000 |
| - Code documentation | 8 hours | ₹2,400 |
| - Project report writing | 12 hours | ₹3,600 |
| - PPT preparation | 6 hours | ₹1,800 |
| - Conference paper formatting | 4 hours | ₹1,200 |
| **6. Testing & Refinement** | 10 hours | ₹3,000 |
| - Bug fixing | 5 hours | ₹1,500 |
| - Performance optimization | 5 hours | ₹1,500 |
| **TOTAL** | **125 hours** | **₹37,500** |

### 5.4 Project Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Literature Review | Week 1-2 | Survey document |
| Data Preparation | Week 3 | Preprocessed dataset |
| Phase 1 Implementation | Week 4-5 | Supervised models |
| Phase 2 Implementation | Week 6-7 | Clustering & zero-day detection |
| Dashboard Development | Week 8 | Interactive visualization |
| Documentation | Week 9-10 | Complete report |
| Testing & Refinement | Week 11 | Final project |
| Presentation Preparation | Week 12 | PPT & demo |

**Total Project Duration**: 12 weeks (3 months)

---

## 6. SYSTEM ARCHITECTURE

### 6.1 Block Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      NSL-KDD DATASET                        │
│              (KDDTrain+.txt / KDDTest+.txt)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│         PREPROCESSING & FEATURE ENGINEERING                 │
│   • One-hot encoding (protocol, service, flag)              │
│   • Normalization (StandardScaler)                          │
│   • Feature extraction (93 features from 41 original)       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
┌──────────────────────┐          ┌──────────────────────────┐
│  PHASE 1: SUPERVISED │          │  PHASE 2: UNSUPERVISED   │
│      LEARNING        │          │       CLUSTERING         │
├──────────────────────┤          ├──────────────────────────┤
│ • Random Forest      │          │ • K-Means (50 clusters)  │
│ • CNN                │          │ • Distance calculation   │
│ • Decision Tree      │          │ • Threshold detection    │
│ • KNN                │          │ • Silhouette analysis    │
│ • Naive Bayes        │          └────────────┬─────────────┘
├──────────────────────┤                       │
│ Output:              │                       │
│ • Class predictions  │                       │
│ • Accuracy: 97-100%  │                       │
│ • Metrics: P,R,F1    │                       │
└──────────┬───────────┘                       │
           │                                   │
           └───────────┬───────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│      CORRELATION & ZERO-DAY CANDIDATE SELECTION             │
│   • Cluster ↔ Class mapping                                 │
│   • Outlier identification (distance > d_min)               │
│   • List of zero-day candidates                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│           ONLINE LEARNING VALIDATION                        │
│   • Incremental training with outliers                      │
│   • Accuracy/F1-Score change measurement                    │
│   • Zero-day detection validation                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│        ZERO-DAY INTRUSION ALERTS & REPORTS                  │
│   • Performance dashboards                                  │
│   • Visualization (confusion matrix, ROC curves)            │
│   • Detailed metrics tables                                 │
│   • Alert notifications                                     │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Data Flow Architecture

1. **Input Layer**: Load NSL-KDD training and test datasets
2. **Preprocessing Layer**: Feature encoding, scaling, and engineering
3. **Dual Processing Layer**:
   - **Branch A**: Supervised learning for known attack classification
   - **Branch B**: Unsupervised clustering for pattern analysis
4. **Integration Layer**: Correlate clustering and classification results
5. **Validation Layer**: Online learning with zero-day candidates
6. **Output Layer**: Metrics, visualizations, and alerts

---

## 7. MODULE STRUCTURE

### 7.1 High-Level Program Organization

```
zero_day_detection/
│
├── src/                              # Source code modules
│   ├── data_preprocess.py           # Data loading and preprocessing
│   ├── feature_engineering.py       # Feature extraction and scaling
│   ├── supervised_models.py         # ML classifier implementations
│   ├── clustering_outliers.py       # K-Means and outlier detection
│   ├── correlation_online.py        # Correlation and online learning
│   └── utils.py                     # Utility functions
│
├── data/                             # Dataset directory
│   ├── KDDTrain+.txt
│   └── KDDTest+.txt
│
├── models/                           # Saved trained models
│   ├── random_forest.pkl
│   ├── cnn_model.h5
│   ├── decision_tree.pkl
│   ├── knn.pkl
│   ├── naive_bayes.pkl
│   └── kmeans_50.pkl
│
├── results/                          # Output results
│   ├── metrics/                     # Performance metrics
│   ├── plots/                       # Visualizations
│   └── zero_day_candidates.csv
│
├── dashboard.py                      # Streamlit interactive dashboard
├── main.py                          # Main execution script
├── config.py                        # Configuration parameters
└── requirements.txt                 # Python dependencies
```

### 7.2 Module Descriptions

#### 7.2.1 `data_preprocess.py`

**Purpose**: Load and preprocess NSL-KDD dataset

**Functions**:
- `load_nsl_kdd()`: Load training and test datasets
- `encode_features()`: One-hot encoding for categorical features
- `normalize_features()`: StandardScaler normalization
- `split_features_labels()`: Separate features and labels

**Input**: Raw NSL-KDD .txt files  
**Output**: Preprocessed feature matrices and label vectors

#### 7.2.2 `feature_engineering.py`

**Purpose**: Extract and engineer features from network traffic data

**Functions**:
- `create_statistical_features()`: Generate statistical aggregations
- `create_temporal_features()`: Extract time-based features
- `create_interaction_features()`: Compute feature interactions
- `select_features()`: Feature selection based on importance

**Input**: Preprocessed dataset  
**Output**: Engineered feature set (93 features)

#### 7.2.3 `supervised_models.py`

**Purpose**: Train and evaluate supervised learning models

**Classes**:
- `RandomForestClassifier`: Ensemble decision tree model
- `CNNClassifier`: Convolutional neural network
- `DecisionTreeClassifier`: Single decision tree
- `KNNClassifier`: K-nearest neighbors
- `NaiveBayesClassifier`: Gaussian Naive Bayes

**Functions**:
- `train_model()`: Train individual model
- `evaluate_model()`: Compute metrics (Accuracy, P, R, F1, ROC-AUC)
- `save_model()`: Persist trained model
- `load_model()`: Load pre-trained model

**Input**: Training data (X_train, y_train)  
**Output**: Trained models + performance metrics

#### 7.2.4 `clustering_outliers.py`

**Purpose**: K-Means clustering and zero-day outlier detection

**Functions**:
- `train_kmeans()`: Train K-Means with optimal K (50 clusters)
- `calculate_distances()`: Compute sample-to-centroid distances
- `detect_outliers()`: Identify samples exceeding distance threshold
- `compute_silhouette()`: Calculate clustering quality metrics
- `analyze_clusters()`: Cluster size, purity, and composition analysis

**Input**: Test features (X_test)  
**Output**: Cluster assignments + outlier flags + metrics

#### 7.2.5 `correlation_online.py`

**Purpose**: Correlation analysis and online learning validation

**Functions**:
- `map_clusters_to_classes()`: Correlate cluster IDs with attack classes
- `identify_zero_day_candidates()`: Select outliers for validation
- `online_learning_experiment()`: Incremental retraining with outliers
- `compute_accuracy_change()`: Measure performance impact
- `generate_correlation_table()`: Create cluster-class mapping table

**Input**: Cluster assignments + Predictions + Outlier flags  
**Output**: Zero-day candidates + Online learning metrics

#### 7.2.6 `main.py`

**Purpose**: Orchestrate complete dual-phase pipeline

**Workflow**:
```python
# 1. Load and preprocess data
X_train, y_train, X_test, y_test = preprocess_data()

# 2. Phase 1: Train supervised models
models = train_supervised_models(X_train, y_train)
predictions = evaluate_models(models, X_test, y_test)

# 3. Phase 2: Clustering and outlier detection
clusters, outliers = detect_zero_day(X_test)

# 4. Correlation and validation
zero_day_candidates = correlate_results(predictions, clusters, outliers)
online_metrics = validate_online_learning(zero_day_candidates)

# 5. Generate reports
generate_visualizations()
save_results()
```

---

## 8. EXPECTED OUTCOMES

### 8.1 Quantitative Outcomes

1. **Supervised Learning Performance**:
   - Accuracy: 97-100% on known attack types
   - Precision: > 0.95 across all attack classes
   - Recall: > 0.95 for critical attack types (DoS, Probe)
   - F1-Score: > 0.95 weighted average

2. **Clustering Quality**:
   - Silhouette Score: 0.50-0.60 (good cluster separation)
   - 50 well-formed clusters with distinct attack patterns
   - Cluster purity: > 90% for majority of clusters

3. **Zero-Day Detection**:
   - 2-5% of test samples flagged as potential zero-day attacks
   - Demonstrated detection of outlier patterns
   - Validation through online learning accuracy changes

### 8.2 Qualitative Outcomes

1. **Hybrid Framework**: Working implementation of dual-phase learning approach
2. **Reproducible Research**: Well-documented codebase for educational use
3. **Interactive Dashboard**: Real-time visualization for demonstration
4. **Comprehensive Documentation**: Complete project report and user guides

---

## 9. FUTURE ENHANCEMENTS

1. **Real-Time Processing**: Deploy system for live network traffic analysis
2. **Additional Datasets**: Validate on CICIDS, UNSW-NB15 datasets
3. **Deep Learning**: Experiment with advanced architectures (LSTM, Transformer)
4. **Automated Response**: Integrate with firewall for automatic threat mitigation
5. **Ensemble Voting**: Combine multiple model predictions for improved accuracy
6. **Feature Learning**: Implement autoencoder-based feature extraction

---

## 10. CONCLUSION

This project successfully implements a dual-phase learning approach for zero-day intrusion detection using the NSL-KDD dataset. By combining supervised learning for known attack classification with unsupervised clustering for novel pattern discovery, the system achieves high accuracy on known attacks while maintaining capability to detect previously unseen threats. The comprehensive evaluation framework and reproducible implementation provide valuable contributions for both academic research and practical network security applications.

---

## REFERENCES

1. A. Touré et al., "A framework for detecting zero-day exploits in network flows," *Computer Networks*, vol. 248, 110476, 2024.

2. S. Chawla and P. Banerjee, "Hybrid approach for intrusion detection model using combination of K-means clustering with machine learning classifiers," *International Journal of Engineering Sciences*, vol. 6, no. 1, pp. 93–97, 2017.

3. A. J. Nugroho et al., "A hybrid intrusion detection system with K-means and CNN+LSTM on NSL-KDD dataset," *EAI Endorsed Transactions on Security and Safety*, 2024.

4. M. Tavallaee et al., "A detailed analysis of the KDD CUP 99 data set," in *IEEE Symposium on Computational Intelligence for Security and Defense Applications*, 2009.

5. L. Dhanabal and S. P. Shantharajah, "A study on NSL-KDD dataset for intrusion detection system based on classification algorithms," *International Journal of Advanced Research in Computer and Communication Engineering*, vol. 4, no. 6, pp. 446–452, 2015.

---

**Document Prepared By**: Srihariharan M  
**Date**: December 15, 2025  
**Version**: 1.0
