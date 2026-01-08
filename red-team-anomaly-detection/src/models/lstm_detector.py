"""
LSTM Anomaly Detector

Implements sequence-based anomaly detection using LSTM networks.
"""

import numpy as np
from typing import Dict
from loguru import logger

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
except ImportError:
    logger.warning("TensorFlow not available, LSTM detector will not work")


class LSTMDetector:
    """LSTM based sequence anomaly detector."""
    
    def __init__(self, config: Dict):
        """
        Initialize LSTM detector.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.sequence_length = config.get('sequence_length', 10)
        self.lstm_units = config.get('lstm_units', [64, 32])
        self.dropout = config.get('dropout', 0.2)
        self.epochs = config.get('epochs', 30)
        self.batch_size = config.get('batch_size', 32)
        self.learning_rate = config.get('learning_rate', 0.001)
        
        self.model = None
        self.threshold_value = None
        
    def _create_sequences(self, X: np.ndarray):
        """Create sequences from data."""
        sequences = []
        targets = []
        
        for i in range(len(X) - self.sequence_length):
            sequences.append(X[i:i + self.sequence_length])
            targets.append(X[i + self.sequence_length])
        
        return np.array(sequences), np.array(targets)
    
    def _build_model(self, input_shape: tuple, output_dim: int):
        """Build LSTM architecture."""
        model = keras.Sequential(name='lstm_detector')
        
        # LSTM layers
        for i, units in enumerate(self.lstm_units):
            return_sequences = i < len(self.lstm_units) - 1
            model.add(layers.LSTM(
                units,
                return_sequences=return_sequences,
                dropout=self.dropout,
                input_shape=input_shape if i == 0 else None
            ))
        
        # Output layer
        model.add(layers.Dense(output_dim))
        
        # Compile
        optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        return model
    
    def fit(self, X: np.ndarray):
        """
        Train the LSTM model.
        
        Args:
            X: Training data
        """
        logger.info(f"Training LSTM on {X.shape[0]} samples")
        
        # Create sequences
        X_seq, y_seq = self._create_sequences(X)
        
        logger.info(f"Created {len(X_seq)} sequences of length {self.sequence_length}")
        
        # Build model
        self.model = self._build_model(
            input_shape=(self.sequence_length, X.shape[1]),
            output_dim=X.shape[1]
        )
        
        # Train
        history = self.model.fit(
            X_seq, y_seq,
            epochs=self.epochs,
            batch_size=self.batch_size,
            validation_split=0.2,
            verbose=0,
            callbacks=[
                keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=5,
                    restore_best_weights=True
                )
            ]
        )
        
        # Calculate prediction errors on training data
        predictions = self.model.predict(X_seq, verbose=0)
        errors = np.mean(np.square(y_seq - predictions), axis=1)
        
        # Set threshold at 95th percentile
        self.threshold_value = np.percentile(errors, 95)
        
        logger.info(f"Training complete. Threshold: {self.threshold_value:.4f}")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies.
        
        Args:
            X: Data to predict on
            
        Returns:
            Array of predictions (-1 for anomaly, 1 for normal)
        """
        scores = self.score_samples(X)
        
        # Pad predictions to match input length
        predictions = np.ones(len(X))
        predictions[self.sequence_length:] = np.where(
            scores > self.threshold_value, -1, 1
        )
        
        return predictions
    
    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """
        Compute prediction errors.
        
        Args:
            X: Data to score
            
        Returns:
            Array of prediction errors
        """
        X_seq, y_seq = self._create_sequences(X)
        
        if len(X_seq) == 0:
            return np.zeros(len(X))
        
        predictions = self.model.predict(X_seq, verbose=0)
        errors = np.mean(np.square(y_seq - predictions), axis=1)
        
        return errors
