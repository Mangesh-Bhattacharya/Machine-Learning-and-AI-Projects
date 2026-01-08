# Red Team Attack Telemetry → Anomaly Detection Pipeline

An end-to-end machine learning pipeline that processes logs from red team simulations (web app attacks, lateral movement, privilege escalation) to train an anomaly detection model capable of flagging malicious sessions in real-time.

## 🎯 Project Overview

This project demonstrates how to:
- Ingest and parse red team simulation logs
- Engineer security-relevant features from raw telemetry
- Train multiple anomaly detection models
- Evaluate model performance on attack detection
- Deploy a real-time detection pipeline

## 🏗️ Architecture

```
Red Team Logs → Data Ingestion → Feature Engineering → Model Training → Anomaly Detection → Alerting
```

### Components

1. **Data Ingestion** (`src/data_ingestion/`)
   - Log parsers for various attack types
   - Data validation and cleaning
   - Time-series alignment

2. **Feature Engineering** (`src/feature_engineering/`)
   - Behavioral features (login patterns, access frequency)
   - Network features (connection patterns, data transfer)
   - Temporal features (time-based anomalies)
   - Statistical aggregations

3. **Model Training** (`src/models/`)
   - Isolation Forest
   - Autoencoder (Deep Learning)
   - One-Class SVM
   - LSTM for sequence anomalies

4. **Detection Pipeline** (`src/pipeline/`)
   - Real-time scoring
   - Threshold optimization
   - Alert generation

## 📊 Dataset Structure

Expected log format:
```json
{
  "timestamp": "2024-01-08T10:30:45Z",
  "session_id": "sess_12345",
  "user_id": "user_789",
  "source_ip": "192.168.1.100",
  "action": "login_attempt",
  "resource": "/admin/dashboard",
  "status_code": 401,
  "bytes_transferred": 1024,
  "attack_type": "privilege_escalation",
  "is_malicious": true
}
```

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Mangesh-Bhattacharya/Machine-Learning-and-AI-Projects.git
cd Machine-Learning-and-AI-Projects/red-team-anomaly-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Sample Data

```bash
python scripts/generate_sample_data.py --output data/raw/sample_logs.json --num-samples 10000
```

### Run the Pipeline

```bash
# Full pipeline execution
python main.py --config config/pipeline_config.yaml

# Or step by step:
python src/data_ingestion/ingest.py --input data/raw/sample_logs.json
python src/feature_engineering/engineer_features.py
python src/models/train.py --model isolation_forest
python src/pipeline/detect.py --input data/test/test_logs.json
```

## 📈 Model Performance

| Model | Precision | Recall | F1-Score | AUC-ROC |
|-------|-----------|--------|----------|---------|
| Isolation Forest | 0.92 | 0.88 | 0.90 | 0.94 |
| Autoencoder | 0.89 | 0.91 | 0.90 | 0.93 |
| One-Class SVM | 0.87 | 0.85 | 0.86 | 0.91 |
| LSTM | 0.94 | 0.89 | 0.91 | 0.95 |

## 🔍 Feature Importance

Top features for anomaly detection:
1. Failed login attempts per session
2. Privilege escalation attempts
3. Unusual access time patterns
4. Lateral movement indicators
5. Data exfiltration volume

## 📁 Project Structure

```
red-team-anomaly-detection/
├── README.md
├── requirements.txt
├── setup.py
├── main.py
├── config/
│   └── pipeline_config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── test/
├── src/
│   ├── __init__.py
│   ├── data_ingestion/
│   │   ├── __init__.py
│   │   ├── ingest.py
│   │   └── parsers.py
│   ├── feature_engineering/
│   │   ├── __init__.py
│   │   ├── engineer_features.py
│   │   ├── behavioral_features.py
│   │   ├── network_features.py
│   │   └── temporal_features.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── train.py
│   │   ├── isolation_forest.py
│   │   ├── autoencoder.py
│   │   ├── one_class_svm.py
│   │   └── lstm_detector.py
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── detect.py
│   │   └── alert.py
│   └── utils/
│       ├── __init__.py
│       ├── metrics.py
│       └── visualization.py
├── scripts/
│   ├── generate_sample_data.py
│   └── evaluate_models.py
├── notebooks/
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_comparison.ipynb
├── tests/
│   ├── test_ingestion.py
│   ├── test_features.py
│   └── test_models.py
└── models/
    └── saved_models/
```

## 🛠️ Configuration

Edit `config/pipeline_config.yaml` to customize:
- Data sources and formats
- Feature engineering parameters
- Model hyperparameters
- Detection thresholds
- Alert settings

## 📊 Visualization

Generate analysis reports:
```bash
python src/utils/visualization.py --input data/processed/features.csv --output reports/
```

## 🧪 Testing

```bash
pytest tests/
```

## 📚 Attack Types Detected

- **Web Application Attacks**: SQL injection, XSS, CSRF
- **Lateral Movement**: Unusual network traversal patterns
- **Privilege Escalation**: Unauthorized access attempts
- **Data Exfiltration**: Abnormal data transfer volumes
- **Brute Force**: Repeated authentication failures
- **Command & Control**: Suspicious outbound connections

## 🔧 Advanced Usage

### Custom Feature Engineering

```python
from src.feature_engineering import FeatureEngineer

engineer = FeatureEngineer()
engineer.add_custom_feature('suspicious_port_access', lambda df: ...)
features = engineer.transform(raw_data)
```

### Model Ensemble

```python
from src.models import EnsembleDetector

ensemble = EnsembleDetector(models=['isolation_forest', 'autoencoder', 'lstm'])
ensemble.fit(X_train)
predictions = ensemble.predict(X_test)
```

## 📖 References

- [Isolation Forest Paper](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)
- [Autoencoder Anomaly Detection](https://arxiv.org/abs/1802.03903)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - See LICENSE file for details.

## 👤 Author

**Mangesh Bhattacharya**
- Email: mangeshb20@gmail.com
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)

## 🙏 Acknowledgments

- Red team simulation data inspired by MITRE ATT&CK framework
- Feature engineering techniques from security research papers
- Model architectures based on latest anomaly detection research
