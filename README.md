# Machine Learning and AI Projects

A comprehensive collection of advanced machine learning and AI projects focusing on security, anomaly detection, and intelligent threat analysis.

## 🎯 Projects

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

# Follow project-specific README for setup
```

## 📋 Requirements

- Python 3.8+
- See individual project requirements for specific dependencies

## 🎓 Learning Resources

These projects demonstrate:
- **Anomaly Detection**: Unsupervised learning for security threat detection
- **Multi-Label Classification**: Predicting multiple labels per sample
- **Feature Engineering**: Extracting meaningful features from security logs
- **Deep Learning**: Neural networks for complex pattern recognition
- **API Development**: Production-ready model serving with FastAPI
- **Security ML**: Applying ML to cybersecurity problems

## 📊 Project Comparison

| Feature | Red Team Anomaly Detection | MITRE ATT&CK Classifier |
|---------|---------------------------|------------------------|
| **Problem Type** | Anomaly Detection | Multi-Label Classification |
| **Input** | Security logs | Attack logs/alerts |
| **Output** | Anomaly score | MITRE ATT&CK techniques |
| **Models** | IF, Autoencoder, SVM, LSTM | Random Forest, Neural Net |
| **API** | Detection pipeline | FastAPI REST endpoint |
| **Use Case** | Real-time threat detection | Attack technique mapping |

## 🔬 Research & Development

These projects are based on:
- MITRE ATT&CK Framework
- Latest anomaly detection research
- Multi-label classification techniques
- Security operations best practices

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

## 🙏 Acknowledgments

- MITRE Corporation for the ATT&CK framework
- Security research community
- Open-source ML libraries (scikit-learn, TensorFlow, FastAPI)
- Red team and blue team practitioners

## 📈 Future Projects

Coming soon:
- Threat Intelligence Graph Neural Networks
- Automated Incident Response with RL
- Malware Classification with CNNs
- Network Traffic Analysis with Transformers

---

⭐ Star this repository if you find it helpful!
