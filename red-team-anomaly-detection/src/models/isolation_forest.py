"""
Isolation Forest Anomaly Detector

Implements anomaly detection using Isolation Forest algorithm.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict
from loguru import logger


class IsolationForestDetector:
    """Isolation Forest based anomaly detector."""
    
    def __init__(self, config: Dict):
        """
        Initialize Isolation Forest detector.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model = IsolationForest(
            n_estimators=config.get('n_estimators', 100),
            max_samples=config.get('max_samples', 'auto'),
            contamination=config.get('contamination', 0.1),
            random_state=config.get('random_state', 42),
            n_jobs=-1
        )
        
    def fit(self, X: np.ndarray):
        """
        Train the Isolation Forest model.
        
        Args:
            X: Training data
        """
        logger.info(f"Training Isolation Forest on {X.shape[0]} samples")
        self.model.fit(X)
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies.
        
        Args:
            X: Data to predict on
            
        Returns:
            Array of predictions (-1 for anomaly, 1 for normal)
        """
        return self.model.predict(X)
    
    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """
        Compute anomaly scores.
        
        Args:
            X: Data to score
            
        Returns:
            Array of anomaly scores (lower = more anomalous)
        """
        return self.model.score_samples(X)
    
    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """
        Compute decision function.
        
        Args:
            X: Data to evaluate
            
        Returns:
            Array of decision scores
        """
        return self.model.decision_function(X)
