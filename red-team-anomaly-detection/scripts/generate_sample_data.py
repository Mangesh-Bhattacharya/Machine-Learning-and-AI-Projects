"""
Sample Data Generator

Generates synthetic red team simulation logs for testing and development.
"""

import json
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
from loguru import logger


class RedTeamLogGenerator:
    """Generate synthetic red team attack logs."""
    
    def __init__(self):
        self.attack_types = [
            'sql_injection',
            'xss',
            'privilege_escalation',
            'lateral_movement',
            'brute_force',
            'data_exfiltration',
            'command_injection',
            'path_traversal'
        ]
        
        self.actions = [
            'login_attempt',
            'file_access',
            'database_query',
            'command_execution',
            'network_scan',
            'privilege_check',
            'data_transfer',
            'resource_access'
        ]
        
        self.resources = [
            '/admin/dashboard',
            '/api/users',
            '/api/data',
            '/files/sensitive',
            '/database/query',
            '/system/config',
            '/logs/access',
            '/backup/files'
        ]
        
        self.status_codes = [200, 201, 400, 401, 403, 404, 500, 503]
        
    def generate_ip(self) -> str:
        """Generate random IP address."""
        return f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    def generate_normal_log(self, timestamp: datetime, session_id: str, user_id: str) -> Dict:
        """Generate a normal (non-malicious) log entry."""
        return {
            'timestamp': timestamp.isoformat(),
            'session_id': session_id,
            'user_id': user_id,
            'source_ip': self.generate_ip(),
            'action': random.choice(['login_attempt', 'file_access', 'resource_access']),
            'resource': random.choice(self.resources[:4]),  # Less sensitive resources
            'status_code': random.choice([200, 201]),
            'bytes_transferred': random.randint(100, 5000),
            'attack_type': None,
            'is_malicious': False
        }
    
    def generate_malicious_log(self, timestamp: datetime, session_id: str, user_id: str) -> Dict:
        """Generate a malicious log entry."""
        attack_type = random.choice(self.attack_types)
        
        # Customize based on attack type
        if attack_type == 'brute_force':
            action = 'login_attempt'
            status_code = random.choice([401, 403])
            bytes_transferred = random.randint(50, 500)
        elif attack_type == 'data_exfiltration':
            action = 'data_transfer'
            status_code = 200
            bytes_transferred = random.randint(10000000, 50000000)  # Large transfer
        elif attack_type == 'privilege_escalation':
            action = 'privilege_check'
            status_code = random.choice([403, 401])
            bytes_transferred = random.randint(100, 1000)
        else:
            action = random.choice(self.actions)
            status_code = random.choice([400, 401, 403, 500])
            bytes_transferred = random.randint(100, 10000)
        
        return {
            'timestamp': timestamp.isoformat(),
            'session_id': session_id,
            'user_id': user_id,
            'source_ip': self.generate_ip(),
            'action': action,
            'resource': random.choice(self.resources),
            'status_code': status_code,
            'bytes_transferred': bytes_transferred,
            'attack_type': attack_type,
            'is_malicious': True
        }
    
    def generate_attack_session(self, start_time: datetime, session_id: str, user_id: str) -> List[Dict]:
        """Generate a complete attack session with multiple log entries."""
        logs = []
        num_entries = random.randint(5, 20)
        
        for i in range(num_entries):
            timestamp = start_time + timedelta(seconds=i * random.randint(1, 30))
            
            # 70% malicious, 30% normal in attack sessions
            if random.random() < 0.7:
                log = self.generate_malicious_log(timestamp, session_id, user_id)
            else:
                log = self.generate_normal_log(timestamp, session_id, user_id)
            
            logs.append(log)
        
        return logs
    
    def generate_normal_session(self, start_time: datetime, session_id: str, user_id: str) -> List[Dict]:
        """Generate a normal user session."""
        logs = []
        num_entries = random.randint(3, 10)
        
        for i in range(num_entries):
            timestamp = start_time + timedelta(seconds=i * random.randint(5, 60))
            log = self.generate_normal_log(timestamp, session_id, user_id)
            logs.append(log)
        
        return logs
    
    def generate_dataset(self, num_samples: int, malicious_ratio: float = 0.1) -> List[Dict]:
        """
        Generate complete dataset.
        
        Args:
            num_samples: Total number of log entries to generate
            malicious_ratio: Ratio of malicious sessions (0.0 to 1.0)
            
        Returns:
            List of log entries
        """
        logger.info(f"Generating {num_samples} log entries with {malicious_ratio*100}% malicious ratio")
        
        logs = []
        start_time = datetime.now() - timedelta(days=7)
        
        session_count = 0
        while len(logs) < num_samples:
            session_id = f"sess_{session_count:06d}"
            user_id = f"user_{random.randint(1, 100):03d}"
            
            # Determine if this is a malicious session
            is_malicious_session = random.random() < malicious_ratio
            
            # Generate session
            if is_malicious_session:
                session_logs = self.generate_attack_session(start_time, session_id, user_id)
            else:
                session_logs = self.generate_normal_session(start_time, session_id, user_id)
            
            logs.extend(session_logs)
            
            # Move time forward
            start_time += timedelta(minutes=random.randint(1, 30))
            session_count += 1
        
        # Trim to exact number
        logs = logs[:num_samples]
        
        # Shuffle logs
        random.shuffle(logs)
        
        logger.success(f"Generated {len(logs)} log entries from {session_count} sessions")
        
        return logs


def main():
    """Main entry point for data generation script."""
    parser = argparse.ArgumentParser(description="Generate synthetic red team logs")
    
    parser.add_argument(
        '--output',
        type=str,
        default='data/raw/sample_logs.json',
        help='Output file path'
    )
    
    parser.add_argument(
        '--num-samples',
        type=int,
        default=10000,
        help='Number of log entries to generate'
    )
    
    parser.add_argument(
        '--malicious-ratio',
        type=float,
        default=0.1,
        help='Ratio of malicious sessions (0.0 to 1.0)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate data
    generator = RedTeamLogGenerator()
    logs = generator.generate_dataset(args.num_samples, args.malicious_ratio)
    
    # Save to file
    logger.info(f"Saving logs to {output_path}")
    with open(output_path, 'w') as f:
        json.dump(logs, f, indent=2)
    
    logger.success(f"Dataset saved successfully!")
    
    # Print statistics
    malicious_count = sum(1 for log in logs if log['is_malicious'])
    logger.info(f"Statistics:")
    logger.info(f"  Total entries: {len(logs)}")
    logger.info(f"  Malicious: {malicious_count} ({malicious_count/len(logs)*100:.1f}%)")
    logger.info(f"  Normal: {len(logs) - malicious_count} ({(len(logs)-malicious_count)/len(logs)*100:.1f}%)")


if __name__ == "__main__":
    main()
