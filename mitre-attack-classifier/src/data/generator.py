"""
Attack Data Generator

Generates synthetic attack logs labeled with MITRE ATT&CK techniques.
"""

import json
import random
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from loguru import logger
from pathlib import Path

from .mitre_mapper import MITREMapper


class AttackDataGenerator:
    """Generate synthetic attack data with MITRE ATT&CK labels."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize generator.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.mitre = MITREMapper()
        
        # Attack patterns for each technique
        self.attack_patterns = self._define_attack_patterns()
        
    def _define_attack_patterns(self) -> Dict:
        """Define attack patterns for generating realistic logs."""
        patterns = {
            "T1190": {
                "actions": ["exploit_attempt", "vulnerability_scan", "web_attack"],
                "commands": ["sqlmap", "nikto", "burpsuite", "' OR 1=1--", "<script>alert(1)</script>"],
                "processes": ["apache2", "nginx", "iis"],
                "ports": [80, 443, 8080, 8443]
            },
            "T1078": {
                "actions": ["login_attempt", "authentication", "account_access"],
                "commands": ["net use", "ssh", "rdp"],
                "users": ["admin", "administrator", "root", "service_account"],
                "ports": [22, 3389, 445]
            },
            "T1059": {
                "actions": ["command_execution", "script_execution", "shell_activity"],
                "commands": [
                    "powershell.exe -enc", "cmd.exe /c", "bash -c",
                    "Invoke-Mimikatz", "IEX (New-Object Net.WebClient)",
                    "python -c", "perl -e"
                ],
                "processes": ["powershell.exe", "cmd.exe", "bash", "python.exe"],
                "ports": []
            },
            "T1053": {
                "actions": ["scheduled_task", "cron_job", "task_creation"],
                "commands": ["schtasks /create", "at ", "crontab -e", "New-ScheduledTask"],
                "processes": ["taskeng.exe", "svchost.exe", "cron"],
                "ports": []
            },
            "T1055": {
                "actions": ["process_injection", "dll_injection", "code_injection"],
                "commands": ["CreateRemoteThread", "WriteProcessMemory", "reflective_dll"],
                "processes": ["explorer.exe", "svchost.exe", "lsass.exe"],
                "ports": []
            },
            "T1003": {
                "actions": ["credential_dump", "memory_access", "password_extraction"],
                "commands": [
                    "mimikatz", "sekurlsa::logonpasswords", "procdump -ma lsass.exe",
                    "reg save HKLM\\SAM", "ntdsutil"
                ],
                "processes": ["lsass.exe", "mimikatz.exe", "procdump.exe"],
                "ports": []
            },
            "T1110": {
                "actions": ["brute_force", "password_spray", "credential_stuffing"],
                "commands": ["hydra", "medusa", "ncrack", "password_list.txt"],
                "users": ["admin", "user", "test", "guest"],
                "ports": [22, 3389, 445, 21, 23]
            },
            "T1087": {
                "actions": ["account_discovery", "user_enumeration", "group_enumeration"],
                "commands": ["net user", "net group", "whoami", "id", "getent passwd"],
                "processes": ["net.exe", "whoami.exe"],
                "ports": [389, 636, 445]
            },
            "T1083": {
                "actions": ["file_discovery", "directory_listing", "file_search"],
                "commands": ["dir /s", "ls -la", "find / -name", "tree", "Get-ChildItem -Recurse"],
                "processes": ["cmd.exe", "powershell.exe", "explorer.exe"],
                "ports": []
            },
            "T1046": {
                "actions": ["port_scan", "service_scan", "network_scan"],
                "commands": ["nmap", "masscan", "netstat", "ss", "Test-NetConnection"],
                "processes": ["nmap", "masscan"],
                "ports": list(range(1, 65536, 1000))
            },
            "T1021": {
                "actions": ["lateral_movement", "remote_login", "remote_execution"],
                "commands": ["psexec", "wmic", "ssh", "rdp", "winrm"],
                "processes": ["psexec.exe", "wmic.exe", "ssh.exe"],
                "ports": [22, 3389, 445, 5985, 5986]
            },
            "T1071": {
                "actions": ["c2_communication", "http_request", "dns_query"],
                "commands": ["curl", "wget", "Invoke-WebRequest", "nslookup"],
                "processes": ["chrome.exe", "firefox.exe", "curl.exe"],
                "ports": [80, 443, 53, 8080]
            },
            "T1041": {
                "actions": ["data_exfiltration", "file_transfer", "data_upload"],
                "commands": ["scp", "ftp", "curl -X POST", "Invoke-RestMethod"],
                "processes": ["scp", "ftp", "curl"],
                "ports": [21, 22, 80, 443]
            },
            "T1486": {
                "actions": ["file_encryption", "ransomware", "crypto_locker"],
                "commands": ["encrypt.exe", "cipher", "openssl enc", ".encrypted"],
                "processes": ["ransomware.exe", "locker.exe"],
                "ports": []
            },
            "T1070": {
                "actions": ["log_deletion", "evidence_removal", "artifact_deletion"],
                "commands": [
                    "wevtutil cl", "rm -rf /var/log", "Clear-EventLog",
                    "del /f /q", "shred"
                ],
                "processes": ["wevtutil.exe", "cmd.exe"],
                "ports": []
            }
        }
        
        return patterns
    
    def generate_log_entry(self, technique_ids: List[str]) -> Dict:
        """
        Generate a single log entry with specified techniques.
        
        Args:
            technique_ids: List of MITRE ATT&CK technique IDs
            
        Returns:
            Log entry dictionary
        """
        # Select primary technique
        primary_technique = random.choice(technique_ids)
        pattern = self.attack_patterns.get(primary_technique, {})
        
        # Generate log fields
        log = {
            "timestamp": (datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )).isoformat(),
            "source_ip": self._generate_ip(),
            "destination_ip": self._generate_ip(),
            "action": random.choice(pattern.get("actions", ["unknown_action"])),
            "command": random.choice(pattern.get("commands", [""])),
            "process": random.choice(pattern.get("processes", ["unknown.exe"])),
            "user": random.choice(pattern.get("users", ["user"])) if "users" in pattern else f"user_{random.randint(1, 100)}",
            "port": random.choice(pattern.get("ports", [0])) if pattern.get("ports") else 0,
            "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS", "SMB", "SSH"]),
            "bytes_transferred": random.randint(100, 10000000),
            "connection_count": random.randint(1, 100),
            "failed_attempts": random.randint(0, 50),
            "status_code": random.choice([200, 401, 403, 404, 500]),
            "severity": random.choice(["low", "medium", "high", "critical"]),
            "techniques": technique_ids
        }
        
        return log
    
    def _generate_ip(self) -> str:
        """Generate random IP address."""
        return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    
    def generate_dataset(
        self,
        num_samples: int,
        techniques_count: int = 50
    ) -> List[Dict]:
        """
        Generate complete dataset.
        
        Args:
            num_samples: Number of samples to generate
            techniques_count: Number of techniques to include
            
        Returns:
            List of log entries
        """
        logger.info(f"Generating {num_samples} attack logs with {techniques_count} techniques")
        
        # Get available techniques
        all_techniques = list(self.attack_patterns.keys())
        selected_techniques = all_techniques[:min(techniques_count, len(all_techniques))]
        
        logger.info(f"Using {len(selected_techniques)} MITRE ATT&CK techniques")
        
        dataset = []
        
        for i in range(num_samples):
            # Randomly select 1-5 techniques per log
            num_techniques = random.randint(1, min(5, len(selected_techniques)))
            techniques = random.sample(selected_techniques, num_techniques)
            
            # Generate log entry
            log = self.generate_log_entry(techniques)
            dataset.append(log)
            
            if (i + 1) % 10000 == 0:
                logger.info(f"Generated {i + 1}/{num_samples} samples")
        
        logger.success(f"Generated {len(dataset)} attack logs")
        
        # Print statistics
        self._print_statistics(dataset)
        
        return dataset
    
    def _print_statistics(self, dataset: List[Dict]):
        """Print dataset statistics."""
        technique_counts = {}
        
        for log in dataset:
            for technique in log["techniques"]:
                technique_counts[technique] = technique_counts.get(technique, 0) + 1
        
        logger.info("Dataset Statistics:")
        logger.info(f"  Total samples: {len(dataset)}")
        logger.info(f"  Unique techniques: {len(technique_counts)}")
        logger.info(f"  Avg techniques per sample: {sum(len(log['techniques']) for log in dataset) / len(dataset):.2f}")
        
        # Top 10 techniques
        top_techniques = sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        logger.info("  Top 10 techniques:")
        for tid, count in top_techniques:
            technique = self.mitre.get_technique(tid)
            logger.info(f"    {tid} ({technique['name']}): {count}")
    
    def save_data(self, dataset: List[Dict], output_path: str):
        """
        Save dataset to file.
        
        Args:
            dataset: List of log entries
            output_path: Path to save file
        """
        logger.info(f"Saving dataset to {output_path}")
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        logger.success(f"Saved {len(dataset)} samples to {output_path}")
