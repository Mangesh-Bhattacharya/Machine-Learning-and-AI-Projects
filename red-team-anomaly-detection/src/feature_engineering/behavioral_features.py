"""
Behavioral Features Module

Extracts user and session behavioral patterns that may indicate malicious activity.
"""

import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger


class BehavioralFeatures:
    """Extract behavioral features from log data."""
    
    def __init__(self, config: Dict):
        """
        Initialize BehavioralFeatures.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.window_size = config.get('window_size', '1h')
        self.features = config.get('features', [])
    
    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract all behavioral features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with behavioral features
        """
        features = pd.DataFrame(index=df.index)
        
        # Failed login count
        if 'failed_login_count' in self.features:
            features['failed_login_count'] = self._failed_login_count(df)
        
        # Privilege escalation attempts
        if 'privilege_escalation_attempts' in self.features:
            features['privilege_escalation_attempts'] = self._privilege_escalation_attempts(df)
        
        # Unique resources accessed
        if 'unique_resources_accessed' in self.features:
            features['unique_resources_accessed'] = self._unique_resources_accessed(df)
        
        # Session duration
        if 'session_duration' in self.features:
            features['session_duration'] = self._session_duration(df)
        
        # Action frequency
        if 'action_frequency' in self.features:
            features['action_frequency'] = self._action_frequency(df)
        
        return features
    
    def _failed_login_count(self, df: pd.DataFrame) -> pd.Series:
        """Count failed login attempts per session."""
        if 'action' not in df.columns or 'status_code' not in df.columns:
            return pd.Series(0, index=df.index)
        
        failed_logins = (
            (df['action'].str.contains('login', case=False, na=False)) &
            (df['status_code'].isin([401, 403]))
        )
        
        if 'session_id' in df.columns:
            counts = df.groupby('session_id')['session_id'].transform('count')
            failed_counts = df[failed_logins].groupby('session_id')['session_id'].transform('count')
            return failed_counts.reindex(df.index, fill_value=0)
        
        return failed_logins.astype(int)
    
    def _privilege_escalation_attempts(self, df: pd.DataFrame) -> pd.Series:
        """Detect privilege escalation attempts."""
        if 'action' not in df.columns:
            return pd.Series(0, index=df.index)
        
        escalation_keywords = ['sudo', 'admin', 'root', 'privilege', 'escalate', 'elevate']
        
        escalation_attempts = df['action'].str.contains(
            '|'.join(escalation_keywords),
            case=False,
            na=False
        )
        
        if 'session_id' in df.columns:
            counts = df[escalation_attempts].groupby(df['session_id'])['session_id'].transform('count')
            return counts.reindex(df.index, fill_value=0)
        
        return escalation_attempts.astype(int)
    
    def _unique_resources_accessed(self, df: pd.DataFrame) -> pd.Series:
        """Count unique resources accessed per session."""
        if 'resource' not in df.columns or 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        unique_counts = df.groupby('session_id')['resource'].transform('nunique')
        return unique_counts
    
    def _session_duration(self, df: pd.DataFrame) -> pd.Series:
        """Calculate session duration in seconds."""
        if 'timestamp' not in df.columns or 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        # Ensure timestamp is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate duration per session
        session_start = df.groupby('session_id')['timestamp'].transform('min')
        session_end = df.groupby('session_id')['timestamp'].transform('max')
        
        duration = (session_end - session_start).dt.total_seconds()
        return duration
    
    def _action_frequency(self, df: pd.DataFrame) -> pd.Series:
        """Calculate action frequency (actions per minute)."""
        if 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        # Count actions per session
        action_count = df.groupby('session_id')['session_id'].transform('count')
        
        # Get session duration in minutes
        duration = self._session_duration(df) / 60.0
        duration = duration.replace(0, 1)  # Avoid division by zero
        
        frequency = action_count / duration
        return frequency
    
    def _suspicious_action_ratio(self, df: pd.DataFrame) -> pd.Series:
        """Calculate ratio of suspicious actions to total actions."""
        if 'action' not in df.columns or 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        suspicious_keywords = [
            'delete', 'drop', 'truncate', 'exec', 'script',
            'inject', 'exploit', 'payload', 'shell'
        ]
        
        suspicious = df['action'].str.contains(
            '|'.join(suspicious_keywords),
            case=False,
            na=False
        )
        
        total_actions = df.groupby('session_id')['session_id'].transform('count')
        suspicious_actions = df[suspicious].groupby(df['session_id'])['session_id'].transform('count')
        suspicious_actions = suspicious_actions.reindex(df.index, fill_value=0)
        
        ratio = suspicious_actions / total_actions
        return ratio
    
    def _error_rate(self, df: pd.DataFrame) -> pd.Series:
        """Calculate error rate per session."""
        if 'status_code' not in df.columns or 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        errors = df['status_code'] >= 400
        
        total_requests = df.groupby('session_id')['session_id'].transform('count')
        error_requests = df[errors].groupby(df['session_id'])['session_id'].transform('count')
        error_requests = error_requests.reindex(df.index, fill_value=0)
        
        error_rate = error_requests / total_requests
        return error_rate
