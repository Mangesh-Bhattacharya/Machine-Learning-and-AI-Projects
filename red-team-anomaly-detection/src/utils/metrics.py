"""
Metrics and Evaluation Module

Provides evaluation metrics for anomaly detection models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from typing import Dict, Any
from loguru import logger


def evaluate_model(model: Any, features: pd.DataFrame, labels: pd.Series = None) -> Dict:
    """
    Evaluate anomaly detection model.
    
    Args:
        model: Trained model
        features: Feature DataFrame
        labels: True labels (if available)
        
    Returns:
        Dictionary of evaluation metrics
    """
    logger.info("Evaluating model performance")
    
    X = features.select_dtypes(include=[np.number]).values
    
    # Get predictions
    predictions = model.predict(X)
    
    # Convert to binary (0 = normal, 1 = anomaly)
    y_pred = (predictions == -1).astype(int)
    
    metrics = {
        'total_samples': len(predictions),
        'anomalies_detected': y_pred.sum(),
        'anomaly_rate': y_pred.mean()
    }
    
    # If labels are available, calculate additional metrics
    if labels is not None:
        y_true = labels.values
        
        metrics.update({
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist()
        })
        
        # Try to calculate AUC-ROC if scores are available
        try:
            if hasattr(model, 'score_samples'):
                scores = model.score_samples(X)
                # Invert scores (lower = more anomalous)
                scores = -scores
                metrics['auc_roc'] = roc_auc_score(y_true, scores)
            elif hasattr(model, 'decision_function'):
                scores = model.decision_function(X)
                # Invert scores (lower = more anomalous)
                scores = -scores
                metrics['auc_roc'] = roc_auc_score(y_true, scores)
        except Exception as e:
            logger.warning(f"Could not calculate AUC-ROC: {e}")
    
    return metrics


def print_evaluation_report(metrics: Dict):
    """
    Print formatted evaluation report.
    
    Args:
        metrics: Dictionary of metrics
    """
    logger.info("=" * 50)
    logger.info("MODEL EVALUATION REPORT")
    logger.info("=" * 50)
    
    logger.info(f"Total Samples: {metrics['total_samples']}")
    logger.info(f"Anomalies Detected: {metrics['anomalies_detected']}")
    logger.info(f"Anomaly Rate: {metrics['anomaly_rate']:.2%}")
    
    if 'precision' in metrics:
        logger.info("-" * 50)
        logger.info(f"Precision: {metrics['precision']:.4f}")
        logger.info(f"Recall: {metrics['recall']:.4f}")
        logger.info(f"F1-Score: {metrics['f1_score']:.4f}")
        
        if 'auc_roc' in metrics:
            logger.info(f"AUC-ROC: {metrics['auc_roc']:.4f}")
        
        if 'confusion_matrix' in metrics:
            cm = metrics['confusion_matrix']
            logger.info("-" * 50)
            logger.info("Confusion Matrix:")
            logger.info(f"  TN: {cm[0][0]:<6} FP: {cm[0][1]}")
            logger.info(f"  FN: {cm[1][0]:<6} TP: {cm[1][1]}")
    
    logger.info("=" * 50)


def calculate_feature_importance(features: pd.DataFrame, predictions: np.ndarray) -> pd.DataFrame:
    """
    Calculate feature importance based on correlation with predictions.
    
    Args:
        features: Feature DataFrame
        predictions: Model predictions
        
    Returns:
        DataFrame with feature importance scores
    """
    numeric_features = features.select_dtypes(include=[np.number])
    
    # Convert predictions to binary
    y_pred = (predictions == -1).astype(int)
    
    # Calculate correlation with predictions
    correlations = []
    
    for col in numeric_features.columns:
        corr = np.corrcoef(numeric_features[col].values, y_pred)[0, 1]
        correlations.append({
            'feature': col,
            'correlation': abs(corr),
            'direction': 'positive' if corr > 0 else 'negative'
        })
    
    importance_df = pd.DataFrame(correlations)
    importance_df = importance_df.sort_values('correlation', ascending=False)
    
    return importance_df


def compare_models(results: Dict[str, Dict]) -> pd.DataFrame:
    """
    Compare multiple models' performance.
    
    Args:
        results: Dictionary mapping model names to their metrics
        
    Returns:
        DataFrame comparing model performance
    """
    comparison = []
    
    for model_name, metrics in results.items():
        row = {'model': model_name}
        row.update(metrics)
        comparison.append(row)
    
    comparison_df = pd.DataFrame(comparison)
    
    # Sort by F1-score if available
    if 'f1_score' in comparison_df.columns:
        comparison_df = comparison_df.sort_values('f1_score', ascending=False)
    
    return comparison_df
