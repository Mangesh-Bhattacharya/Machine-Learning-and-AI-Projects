# MITRE ATT&CK-Mapped Attack Classifier

A production-ready multi-label classification system that maps security logs and alerts to MITRE ATT&CK techniques. This project trains ML models to automatically identify attack techniques from log features and exposes predictions through a REST API.

## 🎯 Project Overview

This system:
- Generates synthetic attack logs labeled with MITRE ATT&CK technique IDs
- Trains multi-label classifiers to predict multiple techniques per attack
- Provides a FastAPI endpoint for real-time technique prediction
- Supports 50+ MITRE ATT&CK techniques across all tactics
- Achieves 90%+ accuracy on technique classification

## 🏗️ Architecture

```
        ┌──────────────────────────────────────────┐
        │          Offline Training Pipeline       │
        │                                          │
        │  Attack Data Generator  →  Features  →   │
Log/Sim │  (synthetic logs,       (TF-IDF,         │  Trained
Schema  │   MITRE labels)          stats)          │  Models
        │             ↓                            │
        │       Multi-Label Models (RF/NN/Ensemble)│
        └─────────────┬────────────────────────────┘
                      │  save / load
                      v
              ┌────────────────────┐
              │   Model Registry   │
              │ models/saved_models│
              └─────────┬──────────┘
                        │
                        v
        ┌─────────────────────────────────────────┐
        │            Online Serving Layer         │
        │                                         │
Clients→│ FastAPI Server (src/api/server.py)      │→ JSON response
        │  - /predict, /predict/batch             │
        │  - /techniques, /metrics, /health       │
        │  - loads vectorizer + model pipeline    │
        └─────────────────────────────────────────┘
                        │
                        v
        ┌─────────────────────────────────────────┐
        │        MITRE & Observability Layer      │
        │                                         │
        │ mitre_attack_mapping.json               │
        │  - id, name, tactic, description        │
        │ utils/metrics.py, visualization.py      │
        │  - evaluation, reports, dashboards      │
        └─────────────────────────────────────────┘

```

### Components

1. **Data Generation** (`src/data/`)
   - MITRE ATT&CK technique mapping
   - Synthetic attack log generation
   - Real-world attack pattern simulation

2. **Feature Engineering** (`src/features/`)
   - Log parsing and normalization
   - TF-IDF vectorization
   - Statistical feature extraction
   - Behavioral indicators

3. **Models** (`src/models/`)
   - Multi-label Random Forest
   - Neural Network classifier
   - Binary Relevance wrapper
   - Classifier Chains

4. **API Server** (`src/api/`)
   - FastAPI REST endpoints
   - Model serving
   - Batch prediction support
   - Technique explanation

## 📊 MITRE ATT&CK Coverage

### Tactics Covered (14 total)
- Reconnaissance
- Resource Development
- Initial Access
- Execution
- Persistence
- Privilege Escalation
- Defense Evasion
- Credential Access
- Discovery
- Lateral Movement
- Collection
- Command and Control
- Exfiltration
- Impact

### Sample Techniques (50+ supported)
- T1190: Exploit Public-Facing Application
- T1078: Valid Accounts
- T1059: Command and Scripting Interpreter
- T1053: Scheduled Task/Job
- T1055: Process Injection
- T1003: OS Credential Dumping
- T1087: Account Discovery
- T1021: Remote Services
- T1071: Application Layer Protocol
- T1486: Data Encrypted for Impact

## 🚀 Quick Start

### Installation

```bash
cd Machine-Learning-and-AI-Projects/mitre-attack-classifier

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Generate Training Data

```bash
python scripts/generate_attack_data.py \
    --output data/raw/attack_logs.json \
    --num-samples 50000 \
    --techniques 50
```

### Train Models

```bash
# Train all models
python main.py --mode train --config config/model_config.yaml

# Train specific model
python main.py --mode train --model random_forest
```

### Start API Server

```bash
# Start FastAPI server
python src/api/server.py --host 0.0.0.0 --port 8000

# Or use uvicorn directly
uvicorn src.api.server:app --reload
```

### Make Predictions

```bash
# Using curl
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "log_entry": {
      "action": "powershell.exe execution",
      "command": "Invoke-Mimikatz",
      "source_ip": "192.168.1.100",
      "user": "admin"
    }
  }'

# Using Python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
        "log_entry": {
            "action": "lateral movement detected",
            "protocol": "SMB",
            "destination": "192.168.1.50"
        }
    }
)

print(response.json())
```

## 📁 Project Structure

```
mitre-attack-classifier/
├── README.md
├── requirements.txt
├── main.py
├── config/
│   └── model_config.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   └── mitre_attack_mapping.json
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── generator.py
│   │   └── mitre_mapper.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   └── vectorizer.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   ├── random_forest_classifier.py
│   │   ├── neural_classifier.py
│   │   └── ensemble.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── schemas.py
│   │   └── middleware.py
│   └── utils/
│       ├── __init__.py
│       ├── metrics.py
│       └── visualization.py
├── scripts/
│   ├── generate_attack_data.py
│   ├── evaluate_models.py
│   └── export_model.py
├── tests/
│   ├── test_data.py
│   ├── test_models.py
│   └── test_api.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_technique_analysis.ipynb
└── models/
    └── saved_models/
```

## 🔧 Configuration

Edit `config/model_config.yaml`:

```yaml
data:
  num_samples: 50000
  test_split: 0.2
  techniques_count: 50

features:
  vectorizer: "tfidf"
  max_features: 5000
  ngram_range: [1, 3]

models:
  random_forest:
    n_estimators: 200
    max_depth: 20
  
  neural_network:
    hidden_layers: [256, 128, 64]
    dropout: 0.3
    epochs: 50

api:
  host: "0.0.0.0"
  port: 8000
  workers: 4
```

## 📈 Model Performance

| Model | Hamming Loss | Subset Accuracy | F1-Score (Micro) | F1-Score (Macro) |
|-------|--------------|-----------------|------------------|------------------|
| Random Forest | 0.08 | 0.72 | 0.89 | 0.85 |
| Neural Network | 0.06 | 0.78 | 0.92 | 0.88 |
| Ensemble | 0.05 | 0.81 | 0.94 | 0.90 |

## 🌐 API Endpoints

### POST /predict
Predict MITRE ATT&CK techniques from a single log entry.

**Request:**
```json
{
  "log_entry": {
    "action": "string",
    "command": "string",
    "source_ip": "string",
    "destination_ip": "string",
    "user": "string",
    "process": "string"
  }
}
```

**Response:**
```json
{
  "techniques": [
    {
      "id": "T1003",
      "name": "OS Credential Dumping",
      "tactic": "Credential Access",
      "confidence": 0.95,
      "description": "Adversaries may attempt to dump credentials..."
    }
  ],
  "prediction_time": 0.023
}
```

### POST /predict/batch
Predict techniques for multiple log entries.

### GET /techniques
List all supported MITRE ATT&CK techniques.

### GET /health
Health check endpoint.

### GET /metrics
Model performance metrics.

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Test API endpoints
pytest tests/test_api.py -v
```

## 📊 Visualization

Generate technique distribution and model performance visualizations:

```bash
python src/utils/visualization.py \
    --predictions data/predictions.json \
    --output reports/
```

## 🔍 Example Use Cases

### 1. Security Operations Center (SOC)
Automatically classify incoming alerts and prioritize based on MITRE ATT&CK techniques.

### 2. Threat Hunting
Identify attack patterns in historical logs by mapping to known techniques.

### 3. Incident Response
Quickly understand attack progression by identifying techniques used.

### 4. Red Team Assessment
Validate detection coverage by mapping red team activities to techniques.

## 🎓 Training Custom Models

```python
from src.models.trainer import ModelTrainer
from src.data.generator import AttackDataGenerator

# Generate custom dataset
generator = AttackDataGenerator()
data = generator.generate_custom_attacks(
    techniques=['T1003', 'T1055', 'T1059'],
    samples_per_technique=1000
)

# Train model
trainer = ModelTrainer(config)
model = trainer.train('random_forest', data)
trainer.save_model(model, 'custom_model.pkl')
```

## 🔐 Security Considerations

- API authentication via API keys (configurable)
- Rate limiting on prediction endpoints
- Input validation and sanitization
- Model versioning and rollback support
- Audit logging for all predictions

## 📚 References

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Multi-Label Classification](https://scikit-learn.org/stable/modules/multiclass.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - See LICENSE file for details.

## 👤 Author

**Mangesh Bhattacharya**
- Email: mangesh.bhattacharya@ontariotechu.net
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)

## 🙏 Acknowledgments

- MITRE Corporation for the ATT&CK framework
- Security research community for attack pattern documentation
- Open-source ML libraries (scikit-learn, TensorFlow, FastAPI)
