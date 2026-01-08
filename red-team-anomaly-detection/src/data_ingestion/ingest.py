"""
Data Ingestion Module

Handles loading, parsing, and cleaning of red team simulation logs.
Supports multiple log formats and performs initial data validation.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime


class DataIngestion:
    """Handles ingestion and preprocessing of red team logs."""
    
    def __init__(self, config: Dict):
        """
        Initialize DataIngestion with configuration.
        
        Args:
            config: Dictionary containing data configuration
        """
        self.config = config
        self.required_fields = config.get('required_fields', [])
        self.timestamp_field = config.get('timestamp_field', 'timestamp')
        
    def load_logs(self, input_path: str) -> pd.DataFrame:
        """
        Load logs from file.
        
        Args:
            input_path: Path to log file
            
        Returns:
            DataFrame containing raw log data
        """
        logger.info(f"Loading logs from {input_path}")
        
        path = Path(input_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {input_path}")
        
        # Determine file format and load
        if path.suffix == '.json':
            df = self._load_json(path)
        elif path.suffix == '.csv':
            df = pd.read_csv(path)
        elif path.suffix in ['.parquet', '.pq']:
            df = pd.read_parquet(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        logger.info(f"Loaded {len(df)} log entries")
        return df
    
    def _load_json(self, path: Path) -> pd.DataFrame:
        """Load JSON log file."""
        with open(path, 'r') as f:
            # Try to load as JSON array first
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame([data])
            except json.JSONDecodeError:
                # If that fails, try line-delimited JSON
                f.seek(0)
                data = [json.loads(line) for line in f]
                return pd.DataFrame(data)
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate log data.
        
        Args:
            df: Raw log DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data")
        
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Check for required fields
        missing_fields = set(self.required_fields) - set(df.columns)
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
        
        # Parse timestamps
        if self.timestamp_field in df.columns:
            df[self.timestamp_field] = pd.to_datetime(df[self.timestamp_field])
            df = df.sort_values(self.timestamp_field)
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        if len(df) < initial_count:
            logger.info(f"Removed {initial_count - len(df)} duplicate entries")
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Validate data types
        df = self._validate_data_types(df)
        
        # Remove invalid entries
        df = self._remove_invalid_entries(df)
        
        logger.info(f"Cleaned data: {len(df)} entries remaining")
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset."""
        # Log missing value statistics
        missing_stats = df.isnull().sum()
        if missing_stats.any():
            logger.info(f"Missing values:\n{missing_stats[missing_stats > 0]}")
        
        # Fill numeric columns with median
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode or 'unknown'
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col].fillna(mode_val[0], inplace=True)
                else:
                    df[col].fillna('unknown', inplace=True)
        
        return df
    
    def _validate_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and convert data types."""
        # Convert IP addresses to string
        if 'source_ip' in df.columns:
            df['source_ip'] = df['source_ip'].astype(str)
        
        # Convert status codes to int
        if 'status_code' in df.columns:
            df['status_code'] = pd.to_numeric(df['status_code'], errors='coerce')
        
        # Convert bytes to numeric
        if 'bytes_transferred' in df.columns:
            df['bytes_transferred'] = pd.to_numeric(df['bytes_transferred'], errors='coerce')
        
        # Convert boolean flags
        if 'is_malicious' in df.columns:
            df['is_malicious'] = df['is_malicious'].astype(bool)
        
        return df
    
    def _remove_invalid_entries(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove entries with invalid data."""
        initial_count = len(df)
        
        # Remove entries with invalid timestamps
        if self.timestamp_field in df.columns:
            df = df[df[self.timestamp_field].notna()]
        
        # Remove entries with negative bytes
        if 'bytes_transferred' in df.columns:
            df = df[df['bytes_transferred'] >= 0]
        
        # Remove entries with invalid status codes
        if 'status_code' in df.columns:
            df = df[(df['status_code'] >= 100) & (df['status_code'] < 600)]
        
        removed = initial_count - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} invalid entries")
        
        return df
    
    def save_processed_data(self, df: pd.DataFrame, output_path: str):
        """
        Save processed data to file.
        
        Args:
            df: Processed DataFrame
            output_path: Path to save file
        """
        logger.info(f"Saving processed data to {output_path}")
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save based on file extension
        if path.suffix == '.parquet':
            df.to_parquet(path, index=False)
        elif path.suffix == '.csv':
            df.to_csv(path, index=False)
        elif path.suffix == '.json':
            df.to_json(path, orient='records', lines=True)
        else:
            raise ValueError(f"Unsupported output format: {path.suffix}")
        
        logger.success(f"Saved {len(df)} entries to {output_path}")
    
    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for the dataset.
        
        Args:
            df: DataFrame to summarize
            
        Returns:
            Dictionary containing summary statistics
        """
        summary = {
            'total_entries': len(df),
            'columns': list(df.columns),
            'date_range': {
                'start': df[self.timestamp_field].min().isoformat() if self.timestamp_field in df.columns else None,
                'end': df[self.timestamp_field].max().isoformat() if self.timestamp_field in df.columns else None
            },
            'unique_sessions': df['session_id'].nunique() if 'session_id' in df.columns else None,
            'unique_users': df['user_id'].nunique() if 'user_id' in df.columns else None,
            'malicious_entries': df['is_malicious'].sum() if 'is_malicious' in df.columns else None,
            'attack_types': df['attack_type'].value_counts().to_dict() if 'attack_type' in df.columns else None
        }
        
        return summary
