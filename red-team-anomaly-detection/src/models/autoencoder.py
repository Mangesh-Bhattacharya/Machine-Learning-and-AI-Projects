"""
Autoencoder Anomaly Detector

Implements anomaly detection using deep learning autoencoder.
"""

import numpy as np
from typing import Dict
from loguru import logger

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
except ImportError:
    logger.warning("TensorFlow not available, autoencoder will not work")


class AutoencoderDetector:
    """Autoencoder based anomaly detector."""
    
    def __init__(self, config: Dict):
        """
        Initialize Autoencoder detector.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.encoding_dim = config.get('encoding_dim', 32)
        self.hidden_layers = config.get('hidden_layers', [64, 32, 16])
        self.activation = config.get('activation', 'relu')
        self.epochs = config.get('epochs', 50)
        self.batch_size = config.get('batch_size', 32)
        self.learning_rate = config.get('learning_rate', 0.001)
        self.threshold = config.get('reconstruction_threshold', 0.95)
        
        self.model = None
        self.reconstruction_errors = None
        
    def _build_model(self, input_dim: int):
        """Build autoencoder architecture."""
        # Encoder
        encoder_input = layers.Input(shape=(input_dim,))
        x = encoder_input
        
        for units in self.hidden_layers:
            x = layers.Dense(units, activation=self.activation)(x)
            x = layers.BatchNormalization()(x)
            x = layers.Dropout(0.2)(x)
        
        # Bottleneck
        encoded = layers.Dense(self.encoding_dim, activation=self.activation, name='encoding')(x)
        
        # Decoder
        x = encoded
        for units in reversed(self.hidden_layers):
            x = layers.Dense(units, activation=self.activation)(x)
            x = layers.BatchNormalization()(x)
            x = layers.Dropout(0.2)(x)
        
        # Output
        decoder_output = layers.Dense(input_dim, activation='sigmoid')(x)
        
        # Autoencoder model
        autoencoder = keras.Model(encoder_input, decoder_output, name='autoencoder')
        
        # Compile
        optimizer = keras.optimizers.Adam(learning_rate=self.learning_rate)
        autoencoder.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        return autoencoder
    
    def fit(self, X: np.ndarray):
        """
        Train the autoencoder.
        
        Args:
            X: Training data
        """
        logger.info(f"Training Autoencoder on {X.shape[0]} samples")
        
        # Build model
        self.model = self._build_model(X.shape[1])
        
        # Train
        history = self.model.fit(
            X, X,
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
        
        # Calculate reconstruction errors on training data
        reconstructions = self.model.predict(X, verbose=0)
        self.reconstruction_errors = np.mean(np.square(X - reconstructions), axis=1)
        
        # Set threshold at specified percentile
        self.threshold_value = np.percentile(self.reconstruction_errors, self.threshold * 100)
        
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
        predictions = np.where(scores > self.threshold_value, -1, 1)
        return predictions
    
    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """
        Compute reconstruction errors.
        
        Args:
            X: Data to score
            
        Returns:
            Array of reconstruction errors
        """
        reconstructions = self.model.predict(X, verbose=0)
        errors = np.mean(np.square(X - reconstructions), axis=1)
        return errors
    
    def get_encoder(self):
        """Get the encoder part of the autoencoder."""
        encoder = keras.Model(
            self.model.input,
            self.model.get_layer('encoding').output
        )
        return encoder
