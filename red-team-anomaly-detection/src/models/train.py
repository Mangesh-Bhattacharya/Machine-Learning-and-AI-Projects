"""
Model Training Module

Handles training of various anomaly detection models.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any
from loguru import logger
import joblib

from .isolation_forest import IsolationForestDetector
from .autoencoder import AutoencoderDetector
from .one_class_svm import OneClassSVMDetector
from .lstm_detector import LSTMDetector


class ModelTrainer:
    """Orchestrates training of anomaly detection models."""
    
    def __init__(self, config: Dict):
        """
        Initialize ModelTrainer.
        
        Args:
            config: Model configuration dictionary
        """
        self.config = config
        self.model_dir = Path(config.get('model_dir', 'models/saved_models'))
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Model registry
        self.models = {
            'isolation_forest': IsolationForestDetector,
            'autoencoder': AutoencoderDetector,
            'one_class_svm': OneClassSVMDetector,
            'lstm': LSTMDetector
        }
    
    def train_model(self, model_name: str, features: pd.DataFrame) -> Any:
        """
        Train a specific model.
        
        Args:
            model_name: Name of the model to train
            features: Feature DataFrame
            
        Returns:
            Trained model instance
        """
        if model_name not in self.models:
            raise ValueError(f"Unknown model: {model_name}")
        
        logger.info(f"Training {model_name} model")
        
        # Get model configuration
        model_config = self.config.get(model_name, {})
        
        # Initialize model
        model_class = self.models[model_name]
        model = model_class(model_config)
        
        # Prepare data
        X = features.select_dtypes(include=[np.number]).values
        
        # Train model
        model.fit(X)
        
        logger.success(f"{model_name} training complete")
        return model
    
    def save_model(self, model: Any, model_name: str):
        """
        Save trained model to disk.
        
        Args:
            model: Trained model instance
            model_name: Name to save model as
        """
        model_path = self.model_dir / f"{model_name}.pkl"
        
        logger.info(f"Saving model to {model_path}")
        joblib.dump(model, model_path)
        logger.success(f"Model saved successfully")
    
    def load_model(self, model_name: str) -> Any:
        """
        Load a trained model from disk.
        
        Args:
            model_name: Name of the model to load
            
        Returns:
            Loaded model instance
        """
        model_path = self.model_dir / f"{model_name}.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        logger.info(f"Loading model from {model_path}")
        model = joblib.load(model_path)
        return model
    
    def train_all_models(self, features: pd.DataFrame) -> Dict[str, Any]:
        """
        Train all enabled models.
        
        Args:
            features: Feature DataFrame
            
        Returns:
            Dictionary of trained models
        """
        enabled_models = self.config.get('enabled_models', [])
        trained_models = {}
        
        for model_name in enabled_models:
            try:
                model = self.train_model(model_name, features)
                self.save_model(model, model_name)
                trained_models[model_name] = model
            except Exception as e:
                logger.error(f"Failed to train {model_name}: {e}")
        
        return trained_models
