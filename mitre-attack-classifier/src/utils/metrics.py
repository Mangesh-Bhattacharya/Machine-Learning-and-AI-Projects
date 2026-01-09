"""
Multi-Label Metrics Module

Evaluation metrics for multi-label classification.
"""

import numpy as np
from sklearn.metrics import (
    hamming_loss,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    jaccard_score,
    classification_report,
    multilabel_confusion_matrix
)
from typing import Dict, Any
from loguru import logger


def evaluate_multilabel_model(model: Any, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
    """
    Evaluate multi-label classification model.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test labels (multi-label binary matrix)
        
    Returns:
        Dictionary of evaluation metrics
    """
    logger.info("Evaluating multi-label model")
    
    # Get predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        # Hamming Loss: fraction of labels that are incorrectly predicted
        'hamming_loss': hamming_loss(y_test, y_pred),
        
        # Subset Accuracy: exact match ratio (all labels must be correct)
        'subset_accuracy': accuracy_score(y_test, y_pred),
        
        # Micro-averaged metrics (aggregate contributions of all classes)
        'precision_micro': precision_score(y_test, y_pred, average='micro', zero_division=0),
        'recall_micro': recall_score(y_test, y_pred, average='micro', zero_division=0),
        'f1_micro': f1_score(y_test, y_pred, average='micro', zero_division=0),
        
        # Macro-averaged metrics (unweighted mean per class)
        'precision_macro': precision_score(y_test, y_pred, average='macro', zero_division=0),
        'recall_macro': recall_score(y_test, y_pred, average='macro', zero_division=0),
        'f1_macro': f1_score(y_test, y_pred, average='macro', zero_division=0),
        
        # Weighted metrics (weighted by support)
        'precision_weighted': precision_score(y_test, y_pred, average='weighted', zero_division=0),
        'recall_weighted': recall_score(y_test, y_pred, average='weighted', zero_division=0),
        'f1_weighted': f1_score(y_test, y_pred, average='weighted', zero_division=0),
        
        # Jaccard similarity (intersection over union)
        'jaccard_micro': jaccard_score(y_test, y_pred, average='micro', zero_division=0),
        'jaccard_macro': jaccard_score(y_test, y_pred, average='macro', zero_division=0),
    }
    
    # Calculate per-label metrics
    per_label_metrics = calculate_per_label_metrics(y_test, y_pred)
    metrics['per_label'] = per_label_metrics
    
    return metrics


def calculate_per_label_metrics(y_test: np.ndarray, y_pred: np.ndarray) -> Dict:
    """
    Calculate metrics for each label individually.
    
    Args:
        y_test: True labels
        y_pred: Predicted labels
        
    Returns:
        Dictionary of per-label metrics
    """
    n_labels = y_test.shape[1]
    
    per_label = {
        'precision': [],
        'recall': [],
        'f1': [],
        'support': []
    }
    
    for i in range(n_labels):
        # Calculate metrics for this label
        precision = precision_score(y_test[:, i], y_pred[:, i], zero_division=0)
        recall = recall_score(y_test[:, i], y_pred[:, i], zero_division=0)
        f1 = f1_score(y_test[:, i], y_pred[:, i], zero_division=0)
        support = y_test[:, i].sum()
        
        per_label['precision'].append(float(precision))
        per_label['recall'].append(float(recall))
        per_label['f1'].append(float(f1))
        per_label['support'].append(int(support))
    
    return per_label


def print_evaluation_report(metrics: Dict, technique_ids: list = None):
    """
    Print formatted evaluation report.
    
    Args:
        metrics: Dictionary of metrics
        technique_ids: List of technique IDs for per-label reporting
    """
    logger.info("=" * 70)
    logger.info("MULTI-LABEL CLASSIFICATION EVALUATION REPORT")
    logger.info("=" * 70)
    
    # Overall metrics
    logger.info("\nOverall Metrics:")
    logger.info(f"  Hamming Loss:      {metrics['hamming_loss']:.4f}")
    logger.info(f"  Subset Accuracy:   {metrics['subset_accuracy']:.4f}")
    
    logger.info("\nMicro-Averaged Metrics:")
    logger.info(f"  Precision:         {metrics['precision_micro']:.4f}")
    logger.info(f"  Recall:            {metrics['recall_micro']:.4f}")
    logger.info(f"  F1-Score:          {metrics['f1_micro']:.4f}")
    
    logger.info("\nMacro-Averaged Metrics:")
    logger.info(f"  Precision:         {metrics['precision_macro']:.4f}")
    logger.info(f"  Recall:            {metrics['recall_macro']:.4f}")
    logger.info(f"  F1-Score:          {metrics['f1_macro']:.4f}")
    
    logger.info("\nWeighted Metrics:")
    logger.info(f"  Precision:         {metrics['precision_weighted']:.4f}")
    logger.info(f"  Recall:            {metrics['recall_weighted']:.4f}")
    logger.info(f"  F1-Score:          {metrics['f1_weighted']:.4f}")
    
    # Per-label metrics (top 10 by F1-score)
    if 'per_label' in metrics and technique_ids:
        logger.info("\nTop 10 Techniques by F1-Score:")
        logger.info(f"{'Technique':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
        logger.info("-" * 70)
        
        # Sort by F1-score
        f1_scores = metrics['per_label']['f1']
        sorted_indices = np.argsort(f1_scores)[::-1][:10]
        
        for idx in sorted_indices:
            if idx < len(technique_ids):
                tid = technique_ids[idx]
                precision = metrics['per_label']['precision'][idx]
                recall = metrics['per_label']['recall'][idx]
                f1 = metrics['per_label']['f1'][idx]
                support = metrics['per_label']['support'][idx]
                
                logger.info(f"{tid:<12} {precision:<12.4f} {recall:<12.4f} {f1:<12.4f} {support:<10}")
    
    logger.info("=" * 70)


def calculate_label_cardinality(y: np.ndarray) -> float:
    """
    Calculate average number of labels per sample.
    
    Args:
        y: Label matrix
        
    Returns:
        Average label cardinality
    """
    return y.sum(axis=1).mean()


def calculate_label_density(y: np.ndarray) -> float:
    """
    Calculate label density (cardinality / total labels).
    
    Args:
        y: Label matrix
        
    Returns:
        Label density
    """
    cardinality = calculate_label_cardinality(y)
    n_labels = y.shape[1]
    return cardinality / n_labels


def get_confusion_matrices(y_test: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Get confusion matrix for each label.
    
    Args:
        y_test: True labels
        y_pred: Predicted labels
        
    Returns:
        Array of confusion matrices
    """
    return multilabel_confusion_matrix(y_test, y_pred)
