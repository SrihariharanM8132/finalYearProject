# Zero-Day Attack Detection Framework

## Project Overview
Implementation of the research paper: "A framework for detecting zero-day exploits in network flows" by Almamy Touré et al.

## Architecture
This project implements a 5-phase framework:
1. **Data Collection**: NSL-KDD dataset processing
2. **Supervised Classification**: CNN + Boosting (DT, RF, KNN, NB)
3. **Unsupervised Clustering**: K-Means clustering
4. **Correlation Analysis**: Linking supervised and unsupervised results
5. **Zero-Day Detection**: Outlier detection + Online learning

## Project Structure
```
project/
├── data/                  # Dataset files
├── src/                   # Source code
│   ├── load_data.py
│   ├── feature_engineering.py
│   ├── cnn_model.py
│   ├── boosting_models.py
│   ├── clustering.py
│   ├── correlation.py
│   ├── zero_day_detection.py
│   └── visualize.py
├── notebooks/             # Jupyter notebooks
├── results/               # Output files and plots
├── main.py               # Main pipeline
└── README.md
```

## Installation

### Requirements
- Python 3.8+
- TensorFlow 2.x
- Scikit-learn
- Pandas, NumPy
- Matplotlib, Seaborn

### Setup
```bash
# Clone repository
git clone <your-repo-url>
cd zero-day-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Download Dataset
Download NSL-KDD from: https://www.unb.ca/cic/datasets/nsl.html
Place files in `data/` folder

### 2. Run Full Pipeline
```bash
python main.py
```

### 3. Run Individual Components
```python
# Load data
from src.load_data import load_nsl_kdd
data = load_nsl_kdd('data/KDDTrain+.txt')

# Train CNN
from src.cnn_model import build_1d_cnn
model = build_1d_cnn(input_shape, num_classes)
```

## Results

### Performance Metrics (Expected)
- **Supervised Classification Accuracy**: 98-100%
- **Zero-Day Detection Rate**: 96-98%
- **False Detection Rate**: <2%

### Key Findings
1. CNN achieves high accuracy for known attacks
2. K-Means effectively clusters network flows
3. Outlier detection successfully identifies zero-day attacks
4. Online learning maintains model performance

## Methodology

### Feature Engineering
Selected 12 key features from 41 original features:
- Duration, Protocol Type, Service
- Source/Destination Bytes
- Connection counts and rates
- Error rates and flags

### Zero-Day Simulation
- Used 'teardrop' attack as simulated zero-day
- Excluded from training set
- Detected through outlier analysis

### Distance Threshold (d_min)
Calculated using silhouette score analysis:
```
d_min = (a(i) + b(i)) / 2
```
where a(i) = intra-cluster distance, b(i) = inter-cluster distance

## Visualizations
The framework generates:
- Training history plots
- Confusion matrices
- Cluster distributions
- Silhouette analysis
- Outlier distance plots
- Model comparison charts

## Limitations
1. Computational intensity for large datasets
2. Fixed K value for clustering
3. Simplified d_min calculation
4. Limited to network flow data

## Future Enhancements
1. Real-time streaming implementation
2. Dynamic K selection
3. Advanced outlier detection algorithms
4. Integration with SIEM systems
5. Multi-dataset validation

## References
- Touré, A., et al. (2024). "A framework for detecting zero-day exploits in network flows." Computer Networks, 248.
- NSL-KDD Dataset: https://www.unb.ca/cic/datasets/nsl.html
- MITRE ATT&CK Framework: https://attack.mitre.org/

## License
MIT License

## Contact
[Your Name] - [Your Email]
Project Link: [GitHub URL]
```

Create `requirements.txt`:
```
numpy>=1.21.0
pandas>=1.3.0
tensorflow>=2.8.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0