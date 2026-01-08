"""
Temporal Features Module

Extracts time-based features that may indicate malicious activity.
"""

import pandas as pd
import numpy as np
from typing import Dict
from loguru import logger


class TemporalFeatures:
    """Extract temporal features from log data."""
    
    def __init__(self, config: Dict):
        """
        Initialize TemporalFeatures.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.features = config.get('features', [])
    
    def extract(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract all temporal features.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with temporal features
        """
        features = pd.DataFrame(index=df.index)
        
        if 'timestamp' not in df.columns:
            logger.warning("No timestamp column found, skipping temporal features")
            return features
        
        # Ensure timestamp is datetime
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Hour of day
        if 'hour_of_day' in self.features:
            features['hour_of_day'] = df['timestamp'].dt.hour
            features['hour_sin'] = np.sin(2 * np.pi * features['hour_of_day'] / 24)
            features['hour_cos'] = np.cos(2 * np.pi * features['hour_of_day'] / 24)
        
        # Day of week
        if 'day_of_week' in self.features:
            features['day_of_week'] = df['timestamp'].dt.dayofweek
            features['day_sin'] = np.sin(2 * np.pi * features['day_of_week'] / 7)
            features['day_cos'] = np.cos(2 * np.pi * features['day_of_week'] / 7)
        
        # Is business hours
        if 'is_business_hours' in self.features:
            features['is_business_hours'] = self._is_business_hours(df)
        
        # Time since last action
        if 'time_since_last_action' in self.features:
            features['time_since_last_action'] = self._time_since_last_action(df)
        
        # Action velocity
        if 'action_velocity' in self.features:
            features['action_velocity'] = self._action_velocity(df)
        
        return features
    
    def _is_business_hours(self, df: pd.DataFrame) -> pd.Series:
        """
        Determine if timestamp is during business hours.
        Business hours: Monday-Friday, 9 AM - 5 PM
        """
        hour = df['timestamp'].dt.hour
        day_of_week = df['timestamp'].dt.dayofweek
        
        is_weekday = day_of_week < 5  # Monday = 0, Friday = 4
        is_work_hours = (hour >= 9) & (hour < 17)
        
        return (is_weekday & is_work_hours).astype(int)
    
    def _time_since_last_action(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate time since last action in seconds.
        Grouped by session or user.
        """
        if 'session_id' in df.columns:
            group_col = 'session_id'
        elif 'user_id' in df.columns:
            group_col = 'user_id'
        else:
            # No grouping available, calculate global time diff
            time_diff = df['timestamp'].diff().dt.total_seconds()
            return time_diff.fillna(0)
        
        # Calculate time difference within groups
        time_diff = df.groupby(group_col)['timestamp'].diff().dt.total_seconds()
        return time_diff.fillna(0)
    
    def _action_velocity(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate action velocity (actions per minute).
        Higher velocity may indicate automated attacks.
        """
        if 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        # Count actions per session
        action_count = df.groupby('session_id')['session_id'].transform('count')
        
        # Calculate session duration in minutes
        session_start = df.groupby('session_id')['timestamp'].transform('min')
        session_end = df.groupby('session_id')['timestamp'].transform('max')
        duration_minutes = (session_end - session_start).dt.total_seconds() / 60.0
        duration_minutes = duration_minutes.replace(0, 1)  # Avoid division by zero
        
        velocity = action_count / duration_minutes
        return velocity
    
    def _is_weekend(self, df: pd.DataFrame) -> pd.Series:
        """Check if timestamp is on weekend."""
        day_of_week = df['timestamp'].dt.dayofweek
        return (day_of_week >= 5).astype(int)  # Saturday = 5, Sunday = 6
    
    def _is_night_time(self, df: pd.DataFrame) -> pd.Series:
        """Check if timestamp is during night time (10 PM - 6 AM)."""
        hour = df['timestamp'].dt.hour
        return ((hour >= 22) | (hour < 6)).astype(int)
    
    def _time_of_day_category(self, df: pd.DataFrame) -> pd.Series:
        """
        Categorize time of day into periods.
        0: Night (0-6), 1: Morning (6-12), 2: Afternoon (12-18), 3: Evening (18-24)
        """
        hour = df['timestamp'].dt.hour
        
        categories = pd.cut(
            hour,
            bins=[0, 6, 12, 18, 24],
            labels=[0, 1, 2, 3],
            include_lowest=True
        )
        
        return categories.astype(int)
    
    def _burst_detection(self, df: pd.DataFrame, window_seconds: int = 60) -> pd.Series:
        """
        Detect burst activity (many actions in short time window).
        Returns count of actions in rolling window.
        """
        if 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        # Sort by timestamp
        df_sorted = df.sort_values('timestamp')
        
        # Calculate rolling count within time window
        burst_counts = []
        
        for idx, row in df_sorted.iterrows():
            current_time = row['timestamp']
            session_id = row['session_id']
            
            # Count actions in the same session within window
            window_start = current_time - pd.Timedelta(seconds=window_seconds)
            
            mask = (
                (df_sorted['session_id'] == session_id) &
                (df_sorted['timestamp'] >= window_start) &
                (df_sorted['timestamp'] <= current_time)
            )
            
            count = mask.sum()
            burst_counts.append(count)
        
        return pd.Series(burst_counts, index=df_sorted.index).reindex(df.index)
    
    def _session_time_span(self, df: pd.DataFrame) -> pd.Series:
        """Calculate total time span of session in hours."""
        if 'session_id' not in df.columns:
            return pd.Series(0, index=df.index)
        
        session_start = df.groupby('session_id')['timestamp'].transform('min')
        session_end = df.groupby('session_id')['timestamp'].transform('max')
        
        time_span = (session_end - session_start).dt.total_seconds() / 3600.0
        return time_span
