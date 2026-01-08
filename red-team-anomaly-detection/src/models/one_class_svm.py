"""
One-Class SVM Anomaly Detector

Implements anomaly detection using One-Class SVM.
"""

import numpy as np
from sklearn.svm import OneClassSVM
from typing import Dict
from loguru import logger


class OneClassSVMDetector:
    """One-Class SVM based anomaly detector."""
    
    def __init__(self, config: Dict):
        """
        Initialize One-Class SVM detector.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.model = OneClassSVM(
            kernel=config.get('kernel', 'rbf'),
            gamma=config.get('gamma', 'auto'),
            nu=config.get('nu', 0.1)
        )
        
    def fit(self, X: np.ndarray):
        """
        Train the One-Class SVM model.
        
        Args:
            X: Training data
        """
        logger.info(f"Training One-Class SVM on {X.shape[0]} samples")
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
            Array of anomaly scores
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
