"""
Network Features Module

Extracts network-related features that may indicate malicious activity.
"""

import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger


class NetworkFeatures:
    """Extract network features from log data."""
    
    def __init__(self, config: Dict):
        """
        Initialize NetworkFeatures.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.features = config.get('features', [])
    
    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract all network features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with network features
        """
        features = pd.DataFrame(index=df.index)
        
        # Bytes transferred
        if 'bytes_transferred' in self.features:
            features['bytes_transferred'] = self._bytes_transferred(df)
            features['bytes_transferred_log'] = np.log1p(features['bytes_transferred'])
        
        # Connection count
        if 'connection_count' in self.features:
            features['connection_count'] = self._connection_count(df)
        
        # Unique destinations
        if 'unique_destinations' in self.features:
            features['unique_destinations'] = self._unique_destinations(df)
        
        # Port scan indicators
        if 'port_scan_indicators' in self.features:
            features['port_scan_score'] = self._port_scan_indicators(df)
        
        # Lateral movement score
        if 'lateral_movement_score' in self.features:
            features['lateral_movement_score'] = self._lateral_movement_score(df)
        
        return features
    
    def _bytes_transferred(self, df: pd.DataFrame) -> pd.Series:
        """Extract bytes transferred feature."""
        if 'bytes_transferred' in df.columns:
            return df['bytes_transferred'].fillna(0)
        return pd.Series(0, index=df.index)
    
    def _connection_count(self, df: pd.DataFrame) -> pd.Series:
        """Count connections per session."""
        if 'session_id' not in df.columns:
            return pd.Series(1, index=df.index)
        
        counts = df.groupby('session_id')['session_id'].transform('count')
        return counts
    
    def _unique_destinations(self, df: pd.DataFrame) -> pd.Series:
        """Count unique destination IPs or resources per session."""
        if 'session_id' not in df.columns:
            return pd.Series(1, index=df.index)
        
        # Try to use destination_ip if available, otherwise use resource
        if 'destination_ip' in df.columns:
            unique_counts = df.groupby('session_id')['destination_ip'].transform('nunique')
        elif 'resource' in df.columns:
            unique_counts = df.groupby('session_id')['resource'].transform('nunique')
        else:
            unique_counts = pd.Series(1, index=df.index)
        
        return unique_counts
    
    def _port_scan_indicators(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate port scan indicator score.
        High score indicates potential port scanning activity.
        """
        score = pd.Series(0.0, index=df.index)
        
        if 'session_id' not in df.columns:
            return score
        
        # Indicator 1: High number of unique destinations
        if 'destination_ip' in df.columns:
            unique_dests = df.groupby('session_id')['destination_ip'].transform('nunique')
            score += (unique_dests > 10).astype(float) * 0.3
        
        # Indicator 2: High connection rate
        if 'timestamp' in df.columns:
            session_duration = self._get_session_duration(df)
            connection_count = self._connection_count(df)
            connection_rate = connection_count / (session_duration / 60.0 + 1)  # per minute
            score += (connection_rate > 20).astype(float) * 0.3
        
        # Indicator 3: Many failed connections
        if 'status_code' in df.columns:
            failed = df['status_code'].isin([403, 404, 500, 503])
            failed_count = df[failed].groupby(df['session_id'])['session_id'].transform('count')
            failed_count = failed_count.reindex(df.index, fill_value=0)
            score += (failed_count > 5).astype(float) * 0.4
        
        return score
    
    def _lateral_movement_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate lateral movement indicator score.
        High score indicates potential lateral movement.
        """
        score = pd.Series(0.0, index=df.index)
        
        if 'session_id' not in df.columns:
            return score
        
        # Indicator 1: Access to multiple internal resources
        if 'resource' in df.columns:
            unique_resources = df.groupby('session_id')['resource'].transform('nunique')
            score += (unique_resources > 5).astype(float) * 0.3
        
        # Indicator 2: Privilege escalation attempts
        if 'action' in df.columns:
            escalation_keywords = ['sudo', 'admin', 'root', 'privilege']
            escalation = df['action'].str.contains(
                '|'.join(escalation_keywords),
                case=False,
                na=False
            )
            escalation_count = df[escalation].groupby(df['session_id'])['session_id'].transform('count')
            escalation_count = escalation_count.reindex(df.index, fill_value=0)
            score += (escalation_count > 0).astype(float) * 0.4
        
        # Indicator 3: Access from multiple source IPs
        if 'source_ip' in df.columns and 'user_id' in df.columns:
            unique_ips = df.groupby('user_id')['source_ip'].transform('nunique')
            score += (unique_ips > 2).astype(float) * 0.3
        
        return score
    
    def _get_session_duration(self, df: pd.DataFrame) -> pd.Series:
        """Helper to calculate session duration in seconds."""
        if 'timestamp' not in df.columns or 'session_id' not in df.columns:
            return pd.Series(1, index=df.index)
        
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        session_start = df.groupby('session_id')['timestamp'].transform('min')
        session_end = df.groupby('session_id')['timestamp'].transform('max')
        
        duration = (session_end - session_start).dt.total_seconds()
        return duration.replace(0, 1)  # Avoid division by zero
    
    def _data_exfiltration_score(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate data exfiltration indicator score.
        High score indicates potential data exfiltration.
        """
        score = pd.Series(0.0, index=df.index)
        
        if 'bytes_transferred' not in df.columns or 'session_id' not in df.columns:
            return score
        
        # Calculate total bytes per session
        total_bytes = df.groupby('session_id')['bytes_transferred'].transform('sum')
        
        # High data transfer volume
        score += (total_bytes > 10_000_000).astype(float) * 0.5  # > 10MB
        
        # Unusual transfer patterns (high variance)
        bytes_std = df.groupby('session_id')['bytes_transferred'].transform('std')
        bytes_mean = df.groupby('session_id')['bytes_transferred'].transform('mean')
        cv = bytes_std / (bytes_mean + 1)  # Coefficient of variation
        score += (cv > 2).astype(float) * 0.3
        
        # Off-hours transfer
        if 'timestamp' in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            hour = df['timestamp'].dt.hour
            off_hours = (hour < 6) | (hour > 22)
            score += off_hours.astype(float) * 0.2
        
        return score
