# Cybersecurity Projects Portfolio

A comprehensive collection of advanced cybersecurity projects covering offensive security, defensive operations, threat intelligence, network reconnaissance, and security automation. These projects demonstrate practical skills in penetration testing, security analysis, and defensive security operations.

## 🎯 Project Categories

### Offensive Security & Red Team
### Defensive Security & Blue Team  
### Threat Intelligence & Analysis
### Network Security & Reconnaissance
### Security Automation & Tools

---

## 🔴 Offensive Security & Red Team

### 1. StealthScan - Advanced Red Team Network Reconnaissance Tool
**Repository**: [StealthScan](https://github.com/Mangesh-Bhattacharya/StealthScan)

Advanced network reconnaissance tool with Streamlit UI for red team operations.

**Key Features:**
- Multi-threaded port scanning
- Service version detection
- OS fingerprinting
- Vulnerability assessment
- Interactive Streamlit dashboard
- Export results (JSON, CSV, PDF)

**Technologies:** Python, Nmap, Streamlit, Threading

**Use Cases:**
- Penetration testing
- Network security assessments
- Red team exercises
- Security audits

---

### 2. Web Reconnaissance Toolkit
**Repository**: [web-recon-toolkit](https://github.com/Mangesh-Bhattacharya/web-recon-toolkit)

Python-based orchestration of Nmap, ffuf, and Nuclei for automated security scanning.

**Key Features:**
- Automated Nmap scanning
- Directory/file fuzzing with ffuf
- Vulnerability scanning with Nuclei
- CSV/JSON reporting
- Modular architecture

**Technologies:** Python, Nmap, ffuf, Nuclei

**Workflow:**
```
Target → Nmap Scan → ffuf Fuzzing → Nuclei Vuln Scan → Report Generation
```

---

### 3. Web Vulnerability Scanner
**Repository**: [web-vuln-scan](https://github.com/Mangesh-Bhattacharya/web-vuln-scan)

Lightweight Python tool for identifying common web application vulnerabilities.

**Detects:**
- SQL Injection (SQLi)
- Cross-Site Scripting (XSS)
- Directory Traversal
- Sensitive File Exposure

**Technologies:** Python, Requests, BeautifulSoup

**Target Audience:** Developers, Security Researchers, Bug Bounty Hunters

---

### 4. Keylogger (Educational)
**Repository**: [Keylogger](https://github.com/Mangesh-Bhattacharya/Keylogger)

Educational keylogger demonstrating keystroke recording functionality.

**Features:**
- Keystroke capture
- File logging
- Basic stealth techniques

**Technologies:** Python, pynput

**⚠️ Educational Purpose Only**: For learning about security threats and defensive measures.

---

## 🔵 Defensive Security & Blue Team

### 5. Ransomware Detection System
**Repository**: [Ransomware-Detection-System](https://github.com/Mangesh-Bhattacharya/Ransomware-Detection-System)

Real-time ransomware detection system monitoring file activities and processes.

**Key Features:**
- Real-time file activity monitoring
- Process behavior analysis
- Suspicious pattern detection
- Automated alerts
- Protective actions
- Quarantine capabilities

**Technologies:** Python, Watchdog, psutil

**Detection Methods:**
- File extension monitoring
- Rapid file modification detection
- Suspicious process identification
- Entropy analysis

**Stars:** ⭐⭐ (2 stars)

---

### 6. Log Anomaly Detector
**Repository**: [Log-Anomaly-Detector](https://github.com/Mangesh-Bhattacharya/Log-Anomaly-Detector)

Lightweight anomaly detection for logs using n-gram language models.

**Key Features:**
- 100% Bash + awk + coreutils
- No Python dependencies
- No network calls
- Unigram + bigram analysis
- Baseline learning
- Anomaly scoring

**Technologies:** Bash, awk, coreutils

**Perfect For:**
- Embedded systems
- Resource-constrained environments
- Air-gapped networks
- Quick log analysis

---

### 7. Wazuh Automated Installer
**Repository**: [Wazuh-Automated-Installer](https://github.com/Mangesh-Bhattacharya/Wazuh-Automated-Installer)

Automated installation and configuration of Wazuh SIEM/XDR platform.

**Features:**
- One-command installation
- Automated configuration
- Multi-node deployment support
- Security hardening

**Technologies:** Bash, Wazuh, Elasticsearch

**Components:**
- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard

---

## 🔍 Threat Intelligence & Analysis

### 8. Threat Intelligence Data Analysis Platform
**Repository**: [threat-intelligence-data-analysis](https://github.com/Mangesh-Bhattacharya/threat-intelligence-data-analysis)

Advanced threat intelligence platform with AI-powered anomaly detection.

**Key Features:**
- Real-time threat monitoring
- AI-powered anomaly detection
- Interactive Streamlit dashboard
- Threat correlation
- IOC enrichment
- Automated reporting

**Technologies:** Python, Streamlit, scikit-learn, Pandas

**Data Sources:**
- MISP feeds
- STIX/TAXII
- Custom threat feeds
- Open-source intelligence

---

### 9. Threat Intelligence Automated Research and Analysis AI Tool
**Repository**: [Threat-Intelligence-Automated-Research-and-Analysis-AI-Tool](https://github.com/Mangesh-Bhattacharya/Threat-Intelligence-Automated-Research-and-Analysis-AI-Tool)

Streamlit tool for automated threat-intel research on IoCs.

**Capabilities:**
- IP address analysis
- Domain reputation checking
- File hash lookup
- VirusTotal integration
- ThreatFox enrichment
- Batch analysis
- Downloadable reports

**Technologies:** Python, Streamlit, VirusTotal API, ThreatFox API

**Supported IOCs:**
- IP addresses
- Domains
- File hashes (MD5, SHA1, SHA256)

---

### 10. CANARIE AWS Cloud Threat Intelligence Project
**Repository**: [canarie-aws-cloud-threat-intelligence-project](https://github.com/Mangesh-Bhattacharya/canarie-aws-cloud-threat-intelligence-project)

ELK Stack-powered threat intelligence for AWS environments.

**Features:**
- Log management
- Threat analysis
- Visualization
- AWS integration
- Real-time monitoring

**Technologies:** ELK Stack, AWS, Docker

**Components:**
- Elasticsearch
- Logstash
- Kibana
- Beats

---

## 🌐 Network Security & Reconnaissance

### 11. Cisco Network Topology Simulator
**Repository**: [cisco-network-topology-simulator](https://github.com/Mangesh-Bhattacharya/cisco-network-topology-simulator)

AI-powered Cisco network topology generator and simulator.

**Key Features:**
- AI-powered topology generation
- Security auditing
- Cloud integration
- Real-time analytics
- Streamlit dashboard
- Network simulation
- Configuration validation

**Technologies:** Python, Streamlit, NetworkX, Cisco APIs

**Use Cases:**
- Network design
- Security auditing
- Training and education
- Disaster recovery planning

---

## 🤖 Security Automation & Tools

### 12. Healthcare IT Support Automation
**Repository**: [healthcare-it-support-automation](https://github.com/Mangesh-Bhattacharya/healthcare-it-support-automation)

Automated incident detection and ticket management for healthcare IT.

**Key Features:**
- Automated incident detection
- Log analysis
- Ticket management
- RIS/PACS monitoring
- Windows server monitoring
- Oracle database monitoring

**Technologies:** Python, PowerShell, SQL

**Healthcare Systems:**
- RIS (Radiology Information System)
- PACS (Picture Archiving and Communication System)
- Windows servers
- Oracle databases

---

### 13. Compliant Data Collector
**Repository**: [compliant-data-collector](https://github.com/Mangesh-Bhattacharya/compliant-data-collector)

Ethical web & API data collection toolkit.

**Key Features:**
- Respects robots.txt
- Terms of Service compliance
- Rate limiting
- Clean data output (CSV/Excel)
- Configurable pipeline
- Test coverage

**Technologies:** Python, Scrapy, Playwright, requests

**Ethics First:**
- Legal compliance
- Ethical scraping
- Reliability
- Data validation

---

## 📚 Learning Resources

### 14. TryHackMe Roadmap
**Repository**: [TryHackMe-Roadmap](https://github.com/Mangesh-Bhattacharya/TryHackMe-Roadmap)

Comprehensive roadmap for TryHackMe learning paths.

**Content:**
- 370+ free rooms
- Beginner to advanced paths
- Tool tutorials
- Hands-on challenges
- Skill-building resources

**Stars:** ⭐⭐⭐⭐ (4 stars)

**Topics Covered:**
- Web exploitation
- Network security
- Cryptography
- Privilege escalation
- Active Directory
- Malware analysis

---

## 🎓 Skills Demonstrated

### Technical Skills
- **Programming**: Python, Bash, PowerShell, SQL
- **Security Tools**: Nmap, Metasploit, Burp Suite, Wireshark
- **Frameworks**: Streamlit, Flask, Django
- **Cloud**: AWS, Azure
- **SIEM**: Wazuh, ELK Stack, Splunk
- **Automation**: Ansible, Docker, CI/CD

### Security Domains
- Penetration Testing
- Vulnerability Assessment
- Threat Intelligence
- Incident Response
- Security Monitoring
- Network Security
- Application Security
- Cloud Security

### Methodologies
- MITRE ATT&CK Framework
- OWASP Top 10
- NIST Cybersecurity Framework
- Kill Chain Analysis
- Threat Modeling

---

## 📊 Project Statistics

| Category | Projects | Stars |
|----------|----------|-------|
| Offensive Security | 4 | 0 |
| Defensive Security | 3 | 2 |
| Threat Intelligence | 3 | 0 |
| Network Security | 1 | 0 |
| Automation | 2 | 0 |
| Learning Resources | 1 | 4 |
| **Total** | **14** | **6** |

---

## 👤 Author

**Mangesh Bhattacharya**
- Email: mangeshb20@gmail.com
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)
- Portfolio: [Mangesh-Bhattacharya.github.io](https://mangesh-bhattacharya.github.io)

---

⭐ **Star the repositories you find useful!**

🔒 **Stay secure, stay ethical!**
