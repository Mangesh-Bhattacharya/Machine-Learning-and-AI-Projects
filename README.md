# Machine Learning and AI Projects

A comprehensive collection of advanced machine learning and AI projects focusing on security, anomaly detection, and intelligent threat analysis. This repository showcases the intersection of AI/ML and cybersecurity through production-ready implementations.

## 📚 Quick Navigation

### 📖 Consolidated Documentation
- **[🔒 Cybersecurity Projects](./CYBERSECURITY-PROJECTS.md)** - 14 security projects across offensive, defensive, and threat intelligence
- **[🤖 AI Projects](./AI-PROJECTS.md)** - 11 AI/ML projects covering automation, NLP, and intelligent systems
- **[🛡️ AI-Security Projects](./AI-SECURITY-PROJECTS.md)** - 5 cutting-edge projects at the intersection of AI and Security

---

## 🎯 Projects in This Repository

### 1. Red Team Attack Telemetry → Anomaly Detection Pipeline

An end-to-end machine learning pipeline that analyzes red team simulation logs to detect malicious activities including web app attacks, lateral movement, and privilege escalation attempts.

**[View Project →](./red-team-anomaly-detection/)**

**Key Features:**
- Multi-model anomaly detection (Isolation Forest, Autoencoder, One-Class SVM, LSTM)
- Behavioral, network, and temporal feature engineering
- Real-time detection pipeline with ensemble predictions
- Comprehensive evaluation metrics and reporting

**Technologies:** Python, scikit-learn, TensorFlow, Pandas

---

### 2. MITRE ATT&CK-Mapped Attack Classifier

A production-ready multi-label classification system that maps security logs and alerts to MITRE ATT&CK techniques with a REST API for real-time predictions.

**[View Project →](./mitre-attack-classifier/)**

**Key Features:**
- 50+ MITRE ATT&CK technique classification
- Multi-label Random Forest and Neural Network models
- FastAPI REST endpoint for model serving
- Batch prediction support with confidence scores
- Comprehensive technique mapping and explanation

**Technologies:** Python, scikit-learn, FastAPI, TensorFlow, MITRE ATT&CK

---

### 3. Offensive Tooling Signal Generator for EDR/SIEM

A comprehensive framework that wraps popular offensive security tools (Nmap, Nuclei, Metasploit, etc.) to generate ML-ready telemetry signals for training EDR/SIEM detection models.

**[View Project →](./offensive-tooling-signal-generator/)**

**Key Features:**
- Wraps 10+ offensive security tools with Python interfaces
- Captures detailed telemetry during tool execution
- Generates ML-ready feature vectors (128-dimensional scan fingerprints)
- Real-time signal streaming to SIEM systems
- Multi-language support (Python, Go, Rust)

**Technologies:** Python, Go, Rust, Scapy, Elasticsearch

---

### 4. Phishing Simulation Analytics with ML

A comprehensive phishing simulation and analytics platform that runs realistic phishing campaigns, collects user behavior data, and uses machine learning to predict click/compromise likelihood.

**[View Project →](./phishing-simulation-analytics/)**

**Key Features:**
- Realistic phishing campaign execution with customizable templates
- User behavior tracking (opens, clicks, data submission)
- ML models predicting compromise likelihood (87% accuracy)
- Real-time analytics dashboard (React + TypeScript)
- REST API for programmatic access

**Technologies:** Python, FastAPI, React, TypeScript, scikit-learn, XGBoost

---

### 5. Red-Blue-ML Lab (Purple Team Notebook)

A comprehensive purple team laboratory that bridges offensive security (red team), defensive operations (blue team), and machine learning. Execute scripted attack scenarios, collect telemetry in ELK/OpenSearch, and train ML detection models with automated CI/CD pipelines.

**[View Project →](./red-blue-ml-lab/)**

**Key Features:**
- Scripted red team scenarios in multiple languages (Python, Go, Rust, PowerShell)
- Centralized log collection with ELK/OpenSearch stack
- Jupyter notebooks for purple team analysis
- Automated ML model training and deployment
- CI/CD integration for continuous improvement

**Technologies:** Python, Go, Rust, ELK Stack, Docker, Jupyter, MLflow

---

## 🚀 Getting Started

Each project contains its own README with detailed setup instructions, dependencies, and usage examples.

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Mangesh-Bhattacharya/Machine-Learning-and-AI-Projects.git
cd Machine-Learning-and-AI-Projects

# Navigate to a specific project
cd red-team-anomaly-detection
# or
cd mitre-attack-classifier
# or
cd offensive-tooling-signal-generator
# or
cd phishing-simulation-analytics
# or
cd red-blue-ml-lab

# Follow project-specific README for setup
```

## 📋 Requirements

- Python 3.8+
- Docker & Docker Compose (for some projects)
- See individual project requirements for specific dependencies

## 🎓 Learning Resources

These projects demonstrate:
- **Anomaly Detection**: Unsupervised learning for security threat detection
- **Multi-Label Classification**: Predicting multiple labels per sample
- **Feature Engineering**: Extracting meaningful features from security logs
- **Deep Learning**: Neural networks for complex pattern recognition
- **API Development**: Production-ready model serving with FastAPI
- **Security ML**: Applying ML to cybersecurity problems
- **Purple Team Operations**: Bridging offensive and defensive security with ML

## 📊 Project Comparison

| Feature | Red Team Anomaly | MITRE Classifier | Offensive Tooling | Phishing Analytics | Red-Blue-ML Lab |
|---------|-----------------|------------------|-------------------|-------------------|-----------------|
| **Type** | Anomaly Detection | Multi-Label | Feature Generation | Risk Prediction | Purple Team |
| **Input** | Security logs | Attack logs | Tool telemetry | User behavior | Attack scenarios |
| **Output** | Anomaly score | ATT&CK techniques | Feature vectors | Risk score | Detection models |
| **Models** | IF, AE, SVM, LSTM | RF, Neural Net | Tool detectors | RF, XGBoost | Ensemble |
| **API** | Detection pipeline | FastAPI REST | SIEM integration | FastAPI REST | Detection API |
| **Dashboard** | ✓ | ✓ | ✓ | ✓ (React) | ✓ (Kibana) |

## 🔬 Research & Development

These projects are based on:
- MITRE ATT&CK Framework
- Latest anomaly detection research
- Multi-label classification techniques
- Security operations best practices
- Purple team methodologies
- Real-world threat intelligence

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

MIT License - see individual projects for specific licensing information.

## 📧 Contact

**Mangesh Bhattacharya**
- Email: mangeshb20@gmail.com
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)
- Portfolio: [Mangesh-Bhattacharya.github.io](https://mangesh-bhattacharya.github.io)

## 🙏 Acknowledgments

- MITRE Corporation for the ATT&CK framework
- Elastic Security Team
- Security research community
- Open-source ML libraries (scikit-learn, TensorFlow, FastAPI)
- Red team and blue team practitioners
- Purple team community

## 📈 Future Projects

Coming soon:
- Threat Intelligence Graph Neural Networks
- Automated Incident Response with RL
- Malware Classification with CNNs
- Network Traffic Analysis with Transformers
- Zero-Trust Architecture with ML
- Federated Learning for Privacy-Preserving Security

---

## 📊 Repository Statistics

- **Total Projects**: 5 (AI-Security focused)
- **Additional Projects**: 25+ across Cybersecurity and AI domains
- **Languages**: Python, Go, Rust, TypeScript, Bash, PowerShell
- **ML Models**: 20+ trained models
- **Average Accuracy**: 91%+
- **Production-Ready APIs**: 4

---

⭐ **Star this repository if you find it helpful!**

🔒 **Securing the future with AI!**

🤖 **Where AI meets Cybersecurity!**
