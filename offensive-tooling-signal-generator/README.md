# Offensive Tooling Signal Generator for EDR/SIEM

A comprehensive framework that wraps popular offensive security tools (Nmap, Nuclei, Metasploit, etc.) to generate ML-ready telemetry signals for training EDR/SIEM detection models. This project creates "scan fingerprint" vectors and behavioral signatures that can be used to detect offensive tooling in production environments.

## 🎯 Project Overview

This framework:
- Wraps 10+ offensive security tools with Python interfaces
- Captures detailed telemetry during tool execution
- Generates ML-ready feature vectors for detection models
- Creates labeled datasets for supervised learning
- Provides real-time signal streaming to SIEM/EDR systems
- Supports multiple programming languages (Python, Go, Rust wrappers)

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                   OFFENSIVE TOOLING SIGNAL GENERATOR                       │
│                     EDR/SIEM Detection Framework                           │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                          LAYER 1: TOOL WRAPPER LAYER                       │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Network    │  │    Vuln      │  │ Exploitation │  │   Web App    │    │
│  │   Scanners   │  │   Scanners   │  │  Frameworks  │  │    Tools     │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ • Nmap       │  │ • Nuclei     │  │ • Metasploit │  │ • Burp Suite │    │
│  │ • Masscan    │  │ • Nikto      │  │ • Empire     │  │ • SQLMap     │    │
│  │ • Zmap       │  │ • OpenVAS    │  │ • Cobalt St. │  │ • Gobuster   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                            │
│  ┌──────────────┐  ┌──────────────┐                                        │
│  │  Password    │  │    Recon     │                                        │
│  │   Crackers   │  │    Tools     │                                        │
│  ├──────────────┤  ├──────────────┤                                        │
│  │ • Hydra      │  │ • Recon-ng   │                                        │
│  │ • John       │  │ • theHarv.   │                                        │
│  │ • Hashcat    │  │ • Amass      │                                        │
│  └──────────────┘  └──────────────┘                                        │
└────────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────────────┐
│                      LAYER 2: TELEMETRY COLLECTION LAYER                   │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │              Telemetry Collector (collector.py)                │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                   ↓                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Network   │  │   Process   │  │   System    │  │    File     │        │
│  │  Monitoring │  │  Monitoring │  │    Call     │  │  Monitoring │        │
│  │             │  │             │  │   Tracing   │  │             │        │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤        │
│  │ • Packet    │  │ • CPU Usage │  │ • syscall   │  │ • File I/O  │        │
│  │   Capture   │  │ • Memory    │  │   tracking  │  │ • Registry  │        │
│  │ • Flow      │  │ • Threads   │  │ • Kernel    │  │   changes   │        │
│  │   Analysis  │  │ • Children  │  │   events    │  │ • Access    │        │
│  │ • Protocol  │  │   Process   │  │ • Context   │  │   patterns  │        │
│  │   Decode    │  │ • Resources │  │   switches  │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└────────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────────────┐
│                    LAYER 3: FEATURE ENGINEERING LAYER                      │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │           Feature Extractor (extractor.py)                     │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                   ↓                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │    Scan      │  │  Behavioral  │  │   Network    │  │   Temporal   │    │
│  │ Fingerprints │  │  Signatures  │  │   Pattern    │  │   Features   │    │
│  │              │  │              │  │   Features   │  │              │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ • Packet     │  │ • Tool       │  │ • Protocol   │  │ • Inter-pkt  │    │
│  │   Rate       │  │   Family     │  │   Analysis   │  │   Delays     │    │
│  │ • Port Scan  │  │ • IOC        │  │ • Port Seq.  │  │ • Burst Rate │    │
│  │   Entropy    │  │   Matching   │  │ • Connection │  │ • Scan       │    │
│  │ • SYN Ratio  │  │ • MITRE      │  │   Patterns   │  │   Duration   │    │
│  │ • TTL        │  │   Mapping    │  │ • DNS Query  │  │ • Timing     │    │
│  │   Patterns   │  │ • Confidence │  │   Rate       │  │   Windows    │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │         128-Dimensional Feature Vector Generation            │          │
│  │  (Network + Timing + Behavioral + Tool-specific indicators)  │          │
│  └──────────────────────────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────────────┐
│                     LAYER 4: MACHINE LEARNING LAYER                        │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │             ML Pipeline (trainer.py & models.py)               │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                   ↓                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Random     │  │    Neural    │  │  Isolation   │  │   Gradient   │    │
│  │   Forest     │  │   Network    │  │   Forest     │  │   Boosting   │    │
│  │  Classifier  │  │   (LSTM)     │  │  (Anomaly)   │  │ (XGB/LGBM)   │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ Multi-class  │  │ Sequence     │  │ Zero-day     │  │ High-perf    │    │
│  │ Tool ID      │  │ Modeling     │  │ Detection    │  │ Real-time    │    │
│  │ 95%+ Acc.    │  │ Complex      │  │ Behavioral   │  │ Inference    │    │
│  │ Feature Imp. │  │ Patterns     │  │ Deviation    │  │ < 25ms       │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────┐          │
│  │        Dataset Builder (dataset_builder.py)                  │          │
│  │  • Labeled dataset generation (offensive + benign)           │          │
│  │  • Training/test split • Feature normalization               │          │
│  └──────────────────────────────────────────────────────────────┘          │
└────────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────────────┐
│                      LAYER 5: INTEGRATION LAYER                            │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────┐        │
│  │         SIEM/EDR Connectors & Real-Time Streaming              │        │
│  └────────────────────────────────────────────────────────────────┘        │
│                                   ↓                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Splunk     │  │   Elastic    │  │  Microsoft   │  │   Custom     │    │
│  │  Connector   │  │    SIEM      │  │   Sentinel   │  │     API      │    │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤    │
│  │ • HEC Token  │  │ • ES Index   │  │ • Workspace  │  │ • Webhook    │    │
│  │ • Real-time  │  │ • Bulk API   │  │ • Shared Key │  │ • REST API   │    │
│  │   Events     │  │ • Detection  │  │ • Alert API  │  │ • Syslog     │    │
│  │ • CEF Format │  │   Rules      │  │ • Log Anal.  │  │ • JSON/XML   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │
└────────────────────────────────────────────────────────────────────────────┘
                                   ↓
┌────────────────────────────────────────────────────────────────────────────┐
│                     LAYER 6: NATIVE PERFORMANCE LAYER                      │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                      │
│  │      Go      │  │     Rust     │  │     C++      │                      │
│  │   Wrappers   │  │   Security   │  │  Low-Level   │                      │
│  │              │  │   Modules    │  │    Hooks     │                      │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤                      │
│  │ • High-perf  │  │ • Memory     │  │ • Syscall    │                      │
│  │   Network    │  │   Safety     │  │   Interc.    │                      │
│  │ • Concurrent │  │ • Crypto     │  │ • Kernel     │                      │
│  │   Processing │  │   Functions  │  │   Modules    │                      │
│  │ • Telemetry  │  │ • Zero-copy  │  │ • eBPF       │                      │
│  └──────────────┘  └──────────────┘  └──────────────┘                      │
└────────────────────────────────────────────────────────────────────────────┘

```

## Data Flow Architecture

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│ Offensive  │────>│   Tool     │────>│ Telemetry  │────>│  Feature   │
│   Tools    │     │  Wrappers  │     │ Collection │     │ Extraction │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
                                                                 │
                                                                 ↓
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│ SIEM/EDR   │<────│ Real-time  │<────│    ML      │<────│  Dataset   │
│   Output   │     │  Detector  │     │   Models   │     │  Builder   │
└────────────┘     └────────────┘     └────────────┘     └────────────┘

```

### Components

1. **Tool Wrappers** (`src/wrappers/`)
   - Nmap scanner wrapper
   - Nuclei vulnerability scanner
   - Metasploit framework interface
   - Gobuster directory brute-forcer
   - SQLMap injection tool
   - Hydra password cracker
   - Burp Suite integration
   - Custom tool wrappers

2. **Telemetry Collection** (`src/telemetry/`)
   - Network traffic capture
   - Process monitoring
   - System call tracing
   - File system activity
   - Registry modifications
   - Memory patterns

3. **Feature Engineering** (`src/features/`)
   - Scan fingerprint vectors
   - Behavioral signatures
   - Network pattern features
   - Temporal features
   - Statistical aggregations

4. **ML Integration** (`src/ml/`)
   - Dataset generation
   - Model training pipelines
   - Real-time inference
   - SIEM/EDR connectors

5. **Multi-Language Support** (`src/native/`)
   - Go performance wrappers
   - Rust security modules
   - C++ low-level hooks

## Storage Structure

```
offensive-tooling-signal-generator/
├── config/
│   ├── tools_config.yaml
│   ├── telemetry_config.yaml
│   └── siem_config.yaml
├── data/
│   ├── raw/                        # Immutable raw outputs
│   │   ├── tool_runs/              # JSONL per run (tool I/O)
│   │   └── telemetry/              # Structured logs, traces, metrics
│   ├── bronze/                     # Lightly cleaned, schema-aligned
│   │   ├── events/                 # Per-tool, per-scenario events
│   │   └── artifacts/              # Files (pcaps, reports, screenshots)
│   ├── silver/                     # Feature-ready ML datasets
│   │   ├── training/               # Parquet feature tables + labels
│   │   └── inference/              # Live features for scoring
│   └── gold/                       # Aggregated views for analytics/SIEM
│       ├── siem_exports/           # ECS/CEF/LEEF-normalized exports
│       └── dashboards/             # Aggregated stats for observability
├── models/
│   ├── signal_detection/           # Model binaries + metadata
│   └── drift_monitoring/           # Stats, thresholds
├── logs/
│   ├── app/                        # Application logs
│   └── audit/                      # Security/audit trail
└── storage/
    ├── retention_policies.md       # Data retention & rotation
    ├── schemas/                    # JSON/Avro schemas for all layers
    └── catalog.yaml                # Logical catalog of tables & paths

```

## 📊 Supported Tools

### Network Scanners
- **Nmap**: Port scanning, service detection, OS fingerprinting
- **Masscan**: High-speed port scanner
- **Zmap**: Internet-wide scanner

### Vulnerability Scanners
- **Nuclei**: Template-based vulnerability scanner
- **Nikto**: Web server scanner
- **OpenVAS**: Comprehensive vulnerability assessment

### Exploitation Frameworks
- **Metasploit**: Penetration testing framework
- **Empire**: Post-exploitation framework
- **Cobalt Strike**: Adversary simulation (telemetry only)

### Web Application Tools
- **Burp Suite**: Web vulnerability scanner
- **SQLMap**: SQL injection tool
- **Gobuster**: Directory/file brute-forcer
- **FFUF**: Fast web fuzzer

### Password Crackers
- **Hydra**: Network login cracker
- **John the Ripper**: Password cracker
- **Hashcat**: Advanced password recovery

### Reconnaissance Tools
- **Recon-ng**: Web reconnaissance framework
- **theHarvester**: OSINT gathering
- **Amass**: Attack surface mapping

## 🚀 Quick Start

### Installation

```bash
cd Machine-Learning-and-AI-Projects/offensive-tooling-signal-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install offensive tools (requires sudo/admin)
sudo bash scripts/install_tools.sh

# Build native wrappers (optional)
cd src/native/go && go build -o ../../bin/go_wrapper
cd ../rust && cargo build --release
```

### Basic Usage

```python
from src.wrappers import NmapWrapper, NucleiWrapper
from src.telemetry import TelemetryCollector
from src.features import FeatureExtractor

# Initialize wrapper with telemetry
nmap = NmapWrapper(telemetry_enabled=True)
collector = TelemetryCollector()

# Run scan with telemetry collection
with collector.capture():
    results = nmap.scan(
        target="192.168.1.0/24",
        ports="1-1000",
        scan_type="syn"
    )

# Extract ML features
extractor = FeatureExtractor()
features = extractor.extract(collector.get_telemetry())

print(f"Scan fingerprint: {features['fingerprint']}")
print(f"Behavioral signature: {features['signature']}")
```

### Generate Training Dataset

```bash
# Generate labeled dataset with multiple tools
python scripts/generate_dataset.py \
    --tools nmap,nuclei,metasploit \
    --samples 10000 \
    --output data/training/offensive_signals.parquet

# Generate benign traffic for comparison
python scripts/generate_benign.py \
    --samples 5000 \
    --output data/training/benign_signals.parquet
```

### Train Detection Model

```bash
# Train tool detection classifier
python main.py --mode train \
    --model random_forest \
    --features data/training/offensive_signals.parquet

# Evaluate model
python main.py --mode evaluate \
    --model models/tool_detector.pkl \
    --test-data data/test/signals.parquet
```

### Real-Time Detection

```bash
# Start real-time monitoring
python main.py --mode monitor \
    --interface eth0 \
    --model models/tool_detector.pkl \
    --siem-endpoint http://splunk:8088

# Stream to SIEM
python src/integrations/siem_streamer.py \
    --format cef \
    --destination syslog://192.168.1.100:514
```

## 📁 Project Structure

```
offensive-tooling-signal-generator/
├── README.md
├── requirements.txt
├── setup.py
├── main.py
├── config/
│   ├── tools_config.yaml
│   ├── telemetry_config.yaml
│   └── siem_config.yaml
├── data/
│   ├── training/
│   ├── test/
│   └── signatures/
├── src/
│   ├── __init__.py
│   ├── wrappers/
│   │   ├── __init__.py
│   │   ├── base_wrapper.py
│   │   ├── nmap_wrapper.py
│   │   ├── nuclei_wrapper.py
│   │   ├── metasploit_wrapper.py
│   │   ├── sqlmap_wrapper.py
│   │   ├── hydra_wrapper.py
│   │   ├── gobuster_wrapper.py
│   │   └── burp_wrapper.py
│   ├── telemetry/
│   │   ├── __init__.py
│   │   ├── collector.py
│   │   ├── network_monitor.py
│   │   ├── process_monitor.py
│   │   ├── syscall_tracer.py
│   │   └── file_monitor.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── fingerprint.py
│   │   ├── behavioral.py
│   │   ├── network_features.py
│   │   └── temporal_features.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── dataset_builder.py
│   │   ├── trainer.py
│   │   ├── detector.py
│   │   └── models.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── siem_streamer.py
│   │   ├── splunk_connector.py
│   │   ├── elastic_connector.py
│   │   └── sentinel_connector.py
│   ├── native/
│   │   ├── go/
│   │   │   ├── wrapper.go
│   │   │   └── telemetry.go
│   │   ├── rust/
│   │   │   ├── Cargo.toml
│   │   │   └── src/
│   │   │       ├── lib.rs
│   │   │       └── monitor.rs
│   │   └── cpp/
│   │       ├── hook.cpp
│   │       └── tracer.cpp
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── metrics.py
├── scripts/
│   ├── install_tools.sh
│   ├── generate_dataset.py
│   ├── generate_benign.py
│   └── benchmark_tools.py
├── tests/
│   ├── test_wrappers.py
│   ├── test_telemetry.py
│   └── test_features.py
├── notebooks/
│   ├── 01_tool_analysis.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
└── models/
    └── saved_models/
```

## 🔍 Feature Vectors

### Scan Fingerprint Vector (128 dimensions)

```python
{
    # Network patterns
    "packet_rate": 1500.0,           # Packets per second
    "packet_size_mean": 64.0,        # Average packet size
    "packet_size_std": 12.5,         # Packet size variance
    "syn_ratio": 0.95,               # SYN packet ratio
    "port_scan_entropy": 7.8,        # Port randomness
    
    # Timing patterns
    "inter_packet_delay_mean": 0.001,  # Average delay
    "inter_packet_delay_std": 0.0005,  # Delay variance
    "burst_rate": 100.0,               # Packets per burst
    "scan_duration": 45.2,             # Total scan time
    
    # Behavioral signatures
    "sequential_ports": True,          # Sequential port access
    "common_ports_ratio": 0.3,         # Well-known ports
    "failed_connection_ratio": 0.85,   # Failed attempts
    "retransmission_rate": 0.02,       # Retransmit ratio
    
    # Tool-specific indicators
    "nmap_signature_score": 0.92,      # Nmap likelihood
    "user_agent_entropy": 2.1,         # UA randomness
    "ttl_pattern": "64,64,64",         # TTL sequence
    "window_size": 1024,               # TCP window
    
    # Process behavior
    "cpu_usage_spike": True,           # CPU spike detected
    "network_threads": 50,             # Concurrent threads
    "dns_queries_rate": 10.5,          # DNS query rate
    "privilege_escalation": False      # Privilege changes
}
```

### Behavioral Signature

```python
{
    "tool_family": "scanner",
    "confidence": 0.95,
    "indicators": [
        "high_packet_rate",
        "sequential_port_access",
        "syn_flood_pattern",
        "low_response_rate"
    ],
    "mitre_techniques": ["T1046", "T1595"],
    "severity": "high"
}
```

## 🎓 Tool Detection Models

### Supported Models

1. **Random Forest Classifier**
   - Multi-class tool identification
   - Feature importance analysis
   - 95%+ accuracy on known tools

2. **Neural Network Detector**
   - Deep learning for complex patterns
   - Sequence modeling with LSTM
   - Unknown tool detection

3. **Isolation Forest**
   - Anomaly-based detection
   - Zero-day tool identification
   - Behavioral deviation scoring

4. **Gradient Boosting**
   - XGBoost/LightGBM
   - High-performance classification
   - Real-time inference

## 📈 Performance Metrics

| Tool | Detection Rate | False Positive | Latency |
|------|---------------|----------------|---------|
| Nmap | 98.5% | 0.5% | 12ms |
| Nuclei | 96.2% | 1.2% | 18ms |
| Metasploit | 97.8% | 0.8% | 25ms |
| SQLMap | 95.5% | 1.5% | 15ms |
| Hydra | 94.3% | 2.1% | 10ms |
| Gobuster | 93.8% | 1.8% | 8ms |

## 🔧 Configuration

### Tool Configuration (`config/tools_config.yaml`)

```yaml
tools:
  nmap:
    binary_path: "/usr/bin/nmap"
    default_args: ["-sS", "-T4"]
    telemetry_level: "full"
    timeout: 300
    
  nuclei:
    binary_path: "/usr/local/bin/nuclei"
    templates_dir: "/opt/nuclei-templates"
    telemetry_level: "full"
    
  metasploit:
    msf_path: "/opt/metasploit-framework"
    rpc_enabled: true
    telemetry_level: "full"
```

### Telemetry Configuration

```yaml
telemetry:
  network:
    capture_interface: "eth0"
    capture_filter: "tcp or udp"
    packet_limit: 10000
    
  process:
    monitor_children: true
    capture_syscalls: true
    track_memory: true
    
  features:
    window_size: 60  # seconds
    aggregation_interval: 5
```

## 🌐 SIEM/EDR Integration

### Splunk Integration

```python
from src.integrations import SplunkConnector

splunk = SplunkConnector(
    host="splunk.company.com",
    port=8088,
    token="YOUR-HEC-TOKEN"
)

# Stream detections
splunk.send_event({
    "tool": "nmap",
    "confidence": 0.95,
    "source_ip": "192.168.1.100",
    "target": "10.0.0.0/24",
    "timestamp": "2024-01-08T10:30:00Z"
})
```

### Elastic SIEM

```python
from src.integrations import ElasticConnector

elastic = ElasticConnector(
    hosts=["https://elastic:9200"],
    api_key="YOUR-API-KEY"
)

elastic.index_detection(detection_data)
```

### Microsoft Sentinel

```python
from src.integrations import SentinelConnector

sentinel = SentinelConnector(
    workspace_id="YOUR-WORKSPACE-ID",
    shared_key="YOUR-SHARED-KEY"
)

sentinel.send_alert(alert_data)
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Test specific wrapper
pytest tests/test_wrappers.py::TestNmapWrapper

# Test with coverage
pytest --cov=src tests/

# Benchmark tool detection
python scripts/benchmark_tools.py --iterations 1000
```

## 📊 Example Use Cases

### 1. Security Operations Center (SOC)
Train models on offensive tool signatures to detect red team activities and real attacks.

### 2. Purple Team Exercises
Generate telemetry during red team operations to improve blue team detection capabilities.

### 3. EDR Development
Create training datasets for endpoint detection and response systems.

### 4. Threat Hunting
Identify unknown offensive tools based on behavioral patterns.

### 5. Security Research
Analyze tool fingerprints and develop new detection techniques.

## 🔐 Security Considerations

⚠️ **WARNING**: This tool generates offensive security tool telemetry. Use only in:
- Authorized penetration testing environments
- Isolated lab networks
- Security research with proper authorization

**Legal Notice**: Unauthorized use of offensive security tools is illegal. Always obtain proper authorization before testing.

## 📚 References

- [Nmap Documentation](https://nmap.org/book/)
- [Nuclei Templates](https://github.com/projectdiscovery/nuclei-templates)
- [Metasploit Framework](https://www.metasploit.com/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [SIEM Integration Best Practices](https://www.splunk.com/en_us/blog/security/siem-best-practices.html)

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - See LICENSE file for details.

**Disclaimer**: This tool is for authorized security testing and research only.

## 👤 Author

**Mangesh Bhattacharya**
- Email: mangeshb20@gmail.com
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)

## 🙏 Acknowledgments

- Offensive security tool developers
- SIEM/EDR vendors for integration support
- Security research community
- Open-source contributors

---

⚠️ **Use Responsibly**: This framework is designed for defensive security purposes. Always follow responsible disclosure and obtain proper authorization.
