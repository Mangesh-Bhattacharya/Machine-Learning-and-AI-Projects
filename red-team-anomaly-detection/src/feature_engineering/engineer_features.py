"""
Feature Engineering Module

Transforms raw log data into features suitable for anomaly detection.
Includes behavioral, network, and temporal feature extraction.
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from loguru import logger
from pathlib import Path

from .behavioral_features import BehavioralFeatures
from .network_features import NetworkFeatures
from .temporal_features import TemporalFeatures


class FeatureEngineer:
    """Main feature engineering class that orchestrates all feature extraction."""
    
    def __init__(self, config: Dict):
        """
        Initialize FeatureEngineer with configuration.
        
        Args:
            config: Dictionary containing feature engineering configuration
        """
        self.config = config
        
        # Initialize feature extractors
        self.behavioral = BehavioralFeatures(config.get('behavioral', {}))
        self.network = NetworkFeatures(config.get('network', {}))
        self.temporal = TemporalFeatures(config.get('temporal', {}))
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform raw data into features.
        
        Args:
            df: Raw log DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("Starting feature engineering")
        
        features_list = []
        
        # Extract behavioral features
        if self.config.get('behavioral', {}).get('enabled', True):
            logger.info("Extracting behavioral features")
            behavioral_features = self.behavioral.extract(df)
            features_list.append(behavioral_features)
        
        # Extract network features
        if self.config.get('network', {}).get('enabled', True):
            logger.info("Extracting network features")
            network_features = self.network.extract(df)
            features_list.append(network_features)
        
        # Extract temporal features
        if self.config.get('temporal', {}).get('enabled', True):
            logger.info("Extracting temporal features")
            temporal_features = self.temporal.extract(df)
            features_list.append(temporal_features)
        
        # Combine all features
        if features_list:
            features = pd.concat(features_list, axis=1)
        else:
            features = df.copy()
        
        # Add aggregations if configured
        if 'aggregations' in self.config:
            features = self._add_aggregations(features, df)
        
        # Handle missing values
        features = self._handle_missing_features(features)
        
        # Normalize features
        features = self._normalize_features(features)
        
        logger.info(f"Feature engineering complete: {features.shape[1]} features created")
        return features
    
    def _add_aggregations(self, features: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
        """Add statistical aggregations."""
        logger.info("Adding statistical aggregations")
        
        aggregations = self.config['aggregations']
        
        # Group by session and compute aggregations
        if 'session_id' in df.columns:
            for agg in aggregations:
                numeric_cols = features.select_dtypes(include=[np.number]).columns
                
                if agg == 'mean':
                    agg_features = features.groupby(df['session_id'])[numeric_cols].mean()
                    agg_features.columns = [f"{col}_session_mean" for col in agg_features.columns]
                elif agg == 'std':
                    agg_features = features.groupby(df['session_id'])[numeric_cols].std()
                    agg_features.columns = [f"{col}_session_std" for col in agg_features.columns]
                elif agg == 'min':
                    agg_features = features.groupby(df['session_id'])[numeric_cols].min()
                    agg_features.columns = [f"{col}_session_min" for col in agg_features.columns]
                elif agg == 'max':
                    agg_features = features.groupby(df['session_id'])[numeric_cols].max()
                    agg_features.columns = [f"{col}_session_max" for col in agg_features.columns]
                elif agg == 'median':
                    agg_features = features.groupby(df['session_id'])[numeric_cols].median()
                    agg_features.columns = [f"{col}_session_median" for col in agg_features.columns]
                
                # Merge back to original features
                features = features.join(agg_features, on=df['session_id'])
        
        return features
    
    def _handle_missing_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in features."""
        # Fill NaN with 0 for numeric columns
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        features[numeric_cols] = features[numeric_cols].fillna(0)
        
        # Fill inf values
        features.replace([np.inf, -np.inf], 0, inplace=True)
        
        return features
    
    def _normalize_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Normalize numeric features to [0, 1] range."""
        logger.info("Normalizing features")
        
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            min_val = features[col].min()
            max_val = features[col].max()
            
            if max_val > min_val:
                features[col] = (features[col] - min_val) / (max_val - min_val)
            else:
                features[col] = 0
        
        return features
    
    def save_features(self, features: pd.DataFrame, output_path: str):
        """
        Save engineered features to file.
        
        Args:
            features: Feature DataFrame
            output_path: Path to save file
        """
        logger.info(f"Saving features to {output_path}")
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if path.suffix == '.parquet':
            features.to_parquet(path, index=False)
        elif path.suffix == '.csv':
            features.to_csv(path, index=False)
        else:
            raise ValueError(f"Unsupported output format: {path.suffix}")
        
        logger.success(f"Saved {features.shape[0]} samples with {features.shape[1]} features")
    
    def load_features(self, input_path: str) -> pd.DataFrame:
        """
        Load previously saved features.
        
        Args:
            input_path: Path to feature file
            
        Returns:
            Feature DataFrame
        """
        logger.info(f"Loading features from {input_path}")
        
        path = Path(input_path)
        
        if path.suffix == '.parquet':
            features = pd.read_parquet(path)
        elif path.suffix == '.csv':
            features = pd.read_csv(path)
        else:
            raise ValueError(f"Unsupported input format: {path.suffix}")
        
        logger.info(f"Loaded {features.shape[0]} samples with {features.shape[1]} features")
        return features
    
    def get_feature_importance(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate feature importance based on variance.
        
        Args:
            features: Feature DataFrame
            
        Returns:
            DataFrame with feature importance scores
        """
        numeric_cols = features.select_dtypes(include=[np.number]).columns
        
        importance = pd.DataFrame({
            'feature': numeric_cols,
            'variance': [features[col].var() for col in numeric_cols],
            'mean': [features[col].mean() for col in numeric_cols],
            'std': [features[col].std() for col in numeric_cols]
        })
        
        importance = importance.sort_values('variance', ascending=False)
        return importance
