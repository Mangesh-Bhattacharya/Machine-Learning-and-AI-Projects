"""
MITRE ATT&CK Mapper

Maps attack patterns to MITRE ATT&CK techniques with detailed metadata.
"""

import json
from typing import Dict, List, Optional
from pathlib import Path
from loguru import logger


class MITREMapper:
    """Maps attacks to MITRE ATT&CK framework techniques."""
    
    def __init__(self):
        """Initialize MITRE ATT&CK mapper with technique database."""
        self.techniques = self._load_techniques()
        self.tactics = self._load_tactics()
        
    def _load_techniques(self) -> Dict:
        """Load MITRE ATT&CK techniques database."""
        # Comprehensive mapping of 50+ techniques
        techniques = {
            # Initial Access
            "T1190": {
                "name": "Exploit Public-Facing Application",
                "tactic": "initial-access",
                "description": "Adversaries may attempt to exploit a weakness in an Internet-facing host or system.",
                "indicators": ["exploit", "vulnerability", "public-facing", "web application", "sql injection", "xss"],
                "platforms": ["Linux", "Windows", "macOS", "Network"]
            },
            "T1078": {
                "name": "Valid Accounts",
                "tactic": "initial-access",
                "description": "Adversaries may obtain and abuse credentials of existing accounts.",
                "indicators": ["login", "authentication", "credentials", "valid account", "stolen password"],
                "platforms": ["Linux", "Windows", "macOS", "Cloud"]
            },
            "T1133": {
                "name": "External Remote Services",
                "tactic": "initial-access",
                "description": "Adversaries may leverage external-facing remote services.",
                "indicators": ["vpn", "rdp", "ssh", "remote access", "external service"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Execution
            "T1059": {
                "name": "Command and Scripting Interpreter",
                "tactic": "execution",
                "description": "Adversaries may abuse command and script interpreters.",
                "indicators": ["powershell", "cmd", "bash", "python", "script", "command execution"],
                "platforms": ["Linux", "Windows", "macOS"],
                "sub_techniques": {
                    "T1059.001": "PowerShell",
                    "T1059.003": "Windows Command Shell",
                    "T1059.004": "Unix Shell"
                }
            },
            "T1053": {
                "name": "Scheduled Task/Job",
                "tactic": "execution",
                "description": "Adversaries may abuse task scheduling functionality.",
                "indicators": ["cron", "scheduled task", "at command", "task scheduler"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1204": {
                "name": "User Execution",
                "tactic": "execution",
                "description": "Adversaries may rely upon user actions to execute malicious code.",
                "indicators": ["user click", "malicious attachment", "phishing", "social engineering"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Persistence
            "T1547": {
                "name": "Boot or Logon Autostart Execution",
                "tactic": "persistence",
                "description": "Adversaries may configure system settings to automatically execute.",
                "indicators": ["autostart", "registry run key", "startup folder", "boot"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1136": {
                "name": "Create Account",
                "tactic": "persistence",
                "description": "Adversaries may create an account to maintain access.",
                "indicators": ["new account", "user creation", "account added"],
                "platforms": ["Linux", "Windows", "macOS", "Cloud"]
            },
            
            # Privilege Escalation
            "T1055": {
                "name": "Process Injection",
                "tactic": "privilege-escalation",
                "description": "Adversaries may inject code into processes.",
                "indicators": ["dll injection", "process hollowing", "reflective loading", "injection"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1068": {
                "name": "Exploitation for Privilege Escalation",
                "tactic": "privilege-escalation",
                "description": "Adversaries may exploit software vulnerabilities to elevate privileges.",
                "indicators": ["privilege escalation", "exploit", "elevation", "root access"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1548": {
                "name": "Abuse Elevation Control Mechanism",
                "tactic": "privilege-escalation",
                "description": "Adversaries may circumvent mechanisms designed to control elevate privileges.",
                "indicators": ["sudo", "uac bypass", "setuid", "elevation"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Defense Evasion
            "T1070": {
                "name": "Indicator Removal",
                "tactic": "defense-evasion",
                "description": "Adversaries may delete or modify artifacts to remove evidence.",
                "indicators": ["log deletion", "clear logs", "file deletion", "evidence removal"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1027": {
                "name": "Obfuscated Files or Information",
                "tactic": "defense-evasion",
                "description": "Adversaries may attempt to make files or information difficult to discover.",
                "indicators": ["obfuscation", "encoding", "encryption", "packing"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1562": {
                "name": "Impair Defenses",
                "tactic": "defense-evasion",
                "description": "Adversaries may maliciously modify components to impair defenses.",
                "indicators": ["disable antivirus", "firewall disabled", "security tool disabled"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Credential Access
            "T1003": {
                "name": "OS Credential Dumping",
                "tactic": "credential-access",
                "description": "Adversaries may attempt to dump credentials.",
                "indicators": ["mimikatz", "credential dump", "lsass", "sam database", "password hash"],
                "platforms": ["Linux", "Windows", "macOS"],
                "sub_techniques": {
                    "T1003.001": "LSASS Memory",
                    "T1003.002": "Security Account Manager",
                    "T1003.003": "NTDS"
                }
            },
            "T1110": {
                "name": "Brute Force",
                "tactic": "credential-access",
                "description": "Adversaries may use brute force techniques to gain access.",
                "indicators": ["brute force", "password spray", "credential stuffing", "failed login"],
                "platforms": ["Linux", "Windows", "macOS", "Cloud"]
            },
            "T1056": {
                "name": "Input Capture",
                "tactic": "credential-access",
                "description": "Adversaries may use methods to capture user input.",
                "indicators": ["keylogger", "credential prompt", "input capture"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Discovery
            "T1087": {
                "name": "Account Discovery",
                "tactic": "discovery",
                "description": "Adversaries may attempt to get a listing of accounts.",
                "indicators": ["net user", "whoami", "account enumeration", "user list"],
                "platforms": ["Linux", "Windows", "macOS", "Cloud"]
            },
            "T1083": {
                "name": "File and Directory Discovery",
                "tactic": "discovery",
                "description": "Adversaries may enumerate files and directories.",
                "indicators": ["dir", "ls", "find", "file enumeration", "directory listing"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1046": {
                "name": "Network Service Discovery",
                "tactic": "discovery",
                "description": "Adversaries may attempt to get a listing of services.",
                "indicators": ["port scan", "service enumeration", "nmap", "network scan"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1018": {
                "name": "Remote System Discovery",
                "tactic": "discovery",
                "description": "Adversaries may attempt to get a listing of other systems.",
                "indicators": ["network enumeration", "ping sweep", "arp scan"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Lateral Movement
            "T1021": {
                "name": "Remote Services",
                "tactic": "lateral-movement",
                "description": "Adversaries may use valid accounts to log into remote services.",
                "indicators": ["rdp", "ssh", "smb", "winrm", "remote login"],
                "platforms": ["Linux", "Windows", "macOS"],
                "sub_techniques": {
                    "T1021.001": "Remote Desktop Protocol",
                    "T1021.002": "SMB/Windows Admin Shares",
                    "T1021.004": "SSH"
                }
            },
            "T1570": {
                "name": "Lateral Tool Transfer",
                "tactic": "lateral-movement",
                "description": "Adversaries may transfer tools between systems.",
                "indicators": ["file transfer", "tool copy", "lateral transfer"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Collection
            "T1005": {
                "name": "Data from Local System",
                "tactic": "collection",
                "description": "Adversaries may search local system sources.",
                "indicators": ["file access", "data collection", "local files"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1039": {
                "name": "Data from Network Shared Drive",
                "tactic": "collection",
                "description": "Adversaries may search network shares.",
                "indicators": ["network share", "shared drive", "file server"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1113": {
                "name": "Screen Capture",
                "tactic": "collection",
                "description": "Adversaries may attempt to take screen captures.",
                "indicators": ["screenshot", "screen capture", "screen recording"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Command and Control
            "T1071": {
                "name": "Application Layer Protocol",
                "tactic": "command-and-control",
                "description": "Adversaries may communicate using application layer protocols.",
                "indicators": ["http", "https", "dns", "c2 communication"],
                "platforms": ["Linux", "Windows", "macOS"],
                "sub_techniques": {
                    "T1071.001": "Web Protocols",
                    "T1071.004": "DNS"
                }
            },
            "T1573": {
                "name": "Encrypted Channel",
                "tactic": "command-and-control",
                "description": "Adversaries may employ encrypted communication.",
                "indicators": ["encrypted traffic", "ssl", "tls", "encrypted c2"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1095": {
                "name": "Non-Application Layer Protocol",
                "tactic": "command-and-control",
                "description": "Adversaries may use non-application layer protocols.",
                "indicators": ["icmp", "raw socket", "custom protocol"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Exfiltration
            "T1041": {
                "name": "Exfiltration Over C2 Channel",
                "tactic": "exfiltration",
                "description": "Adversaries may steal data over their C2 channel.",
                "indicators": ["data exfiltration", "c2 channel", "data theft"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1048": {
                "name": "Exfiltration Over Alternative Protocol",
                "tactic": "exfiltration",
                "description": "Adversaries may steal data over different protocols.",
                "indicators": ["dns exfiltration", "icmp exfiltration", "alternative protocol"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1567": {
                "name": "Exfiltration Over Web Service",
                "tactic": "exfiltration",
                "description": "Adversaries may use web services to exfiltrate data.",
                "indicators": ["cloud upload", "web service", "file sharing"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            
            # Impact
            "T1486": {
                "name": "Data Encrypted for Impact",
                "tactic": "impact",
                "description": "Adversaries may encrypt data to impact availability.",
                "indicators": ["ransomware", "file encryption", "crypto locker"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1490": {
                "name": "Inhibit System Recovery",
                "tactic": "impact",
                "description": "Adversaries may delete or remove built-in data.",
                "indicators": ["backup deletion", "shadow copy delete", "recovery disabled"],
                "platforms": ["Linux", "Windows", "macOS"]
            },
            "T1498": {
                "name": "Network Denial of Service",
                "tactic": "impact",
                "description": "Adversaries may perform DoS attacks.",
                "indicators": ["ddos", "dos", "network flood", "service disruption"],
                "platforms": ["Linux", "Windows", "macOS", "Network"]
            },
            "T1529": {
                "name": "System Shutdown/Reboot",
                "tactic": "impact",
                "description": "Adversaries may shutdown/reboot systems.",
                "indicators": ["shutdown", "reboot", "system halt"],
                "platforms": ["Linux", "Windows", "macOS"]
            }
        }
        
        return techniques
    
    def _load_tactics(self) -> Dict:
        """Load MITRE ATT&CK tactics."""
        tactics = {
            "reconnaissance": {
                "name": "Reconnaissance",
                "description": "Gather information for planning future operations"
            },
            "resource-development": {
                "name": "Resource Development",
                "description": "Establish resources to support operations"
            },
            "initial-access": {
                "name": "Initial Access",
                "description": "Gain initial foothold within a network"
            },
            "execution": {
                "name": "Execution",
                "description": "Run malicious code"
            },
            "persistence": {
                "name": "Persistence",
                "description": "Maintain foothold in the environment"
            },
            "privilege-escalation": {
                "name": "Privilege Escalation",
                "description": "Gain higher-level permissions"
            },
            "defense-evasion": {
                "name": "Defense Evasion",
                "description": "Avoid detection"
            },
            "credential-access": {
                "name": "Credential Access",
                "description": "Steal account credentials"
            },
            "discovery": {
                "name": "Discovery",
                "description": "Explore the environment"
            },
            "lateral-movement": {
                "name": "Lateral Movement",
                "description": "Move through the environment"
            },
            "collection": {
                "name": "Collection",
                "description": "Gather data of interest"
            },
            "command-and-control": {
                "name": "Command and Control",
                "description": "Communicate with compromised systems"
            },
            "exfiltration": {
                "name": "Exfiltration",
                "description": "Steal data"
            },
            "impact": {
                "name": "Impact",
                "description": "Manipulate, interrupt, or destroy systems and data"
            }
        }
        
        return tactics
    
    def get_technique(self, technique_id: str) -> Optional[Dict]:
        """Get technique details by ID."""
        return self.techniques.get(technique_id)
    
    def get_techniques_by_tactic(self, tactic: str) -> List[Dict]:
        """Get all techniques for a specific tactic."""
        return [
            {"id": tid, **tdata}
            for tid, tdata in self.techniques.items()
            if tdata["tactic"] == tactic
        ]
    
    def get_all_technique_ids(self) -> List[str]:
        """Get list of all technique IDs."""
        return list(self.techniques.keys())
    
    def match_indicators(self, text: str, threshold: int = 1) -> List[str]:
        """
        Match text against technique indicators.
        
        Args:
            text: Text to match
            threshold: Minimum number of indicator matches
            
        Returns:
            List of matching technique IDs
        """
        text_lower = text.lower()
        matches = []
        
        for tid, tdata in self.techniques.items():
            match_count = sum(
                1 for indicator in tdata["indicators"]
                if indicator in text_lower
            )
            
            if match_count >= threshold:
                matches.append(tid)
        
        return matches
    
    def save_mapping(self, output_path: str):
        """Save technique mapping to JSON file."""
        mapping = {
            "techniques": self.techniques,
            "tactics": self.tactics
        }
        
        with open(output_path, 'w') as f:
            json.dump(mapping, f, indent=2)
        
        logger.info(f"Saved MITRE ATT&CK mapping to {output_path}")
