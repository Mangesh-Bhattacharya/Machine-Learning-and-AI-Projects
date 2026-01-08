"""
Detection Pipeline Module

Real-time anomaly detection using trained models.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger
import joblib


class AnomalyDetector:
    """Real-time anomaly detection pipeline."""
    
    def __init__(self, config: Dict):
        """
        Initialize AnomalyDetector.
        
        Args:
            config: Detection configuration
        """
        self.config = config
        self.models = {}
        self.thresholds = config.get('thresholds', {})
        self.ensemble_config = config.get('ensemble', {})
        
    def load_models(self, model_dir: str):
        """
        Load trained models from directory.
        
        Args:
            model_dir: Directory containing saved models
        """
        logger.info(f"Loading models from {model_dir}")
        
        model_path = Path(model_dir)
        
        for model_file in model_path.glob('*.pkl'):
            model_name = model_file.stem
            logger.info(f"Loading {model_name}")
            
            try:
                model = joblib.load(model_file)
                self.models[model_name] = model
            except Exception as e:
                logger.error(f"Failed to load {model_name}: {e}")
        
        logger.success(f"Loaded {len(self.models)} models")
    
    def detect(self, features: pd.DataFrame) -> pd.DataFrame:
        """
        Detect anomalies in features.
        
        Args:
            features: Feature DataFrame
            
        Returns:
            DataFrame with anomaly predictions and scores
        """
        logger.info(f"Running anomaly detection on {len(features)} samples")
        
        X = features.select_dtypes(include=[np.number]).values
        
        results = pd.DataFrame(index=features.index)
        
        # Get predictions from each model
        for model_name, model in self.models.items():
            logger.info(f"Running {model_name}")
            
            try:
                # Get predictions
                predictions = model.predict(X)
                results[f'{model_name}_prediction'] = predictions
                
                # Get scores
                if hasattr(model, 'score_samples'):
                    scores = model.score_samples(X)
                    results[f'{model_name}_score'] = scores
                elif hasattr(model, 'decision_function'):
                    scores = model.decision_function(X)
                    results[f'{model_name}_score'] = scores
                
            except Exception as e:
                logger.error(f"Error running {model_name}: {e}")
        
        # Ensemble predictions
        if self.ensemble_config.get('enabled', True):
            results['ensemble_prediction'] = self._ensemble_predict(results)
            results['ensemble_score'] = self._ensemble_score(results)
        
        # Flag anomalies
        results['is_anomaly'] = results['ensemble_prediction'] == -1
        
        anomaly_count = results['is_anomaly'].sum()
        logger.info(f"Detected {anomaly_count} anomalies ({anomaly_count/len(results)*100:.2f}%)")
        
        return results
    
    def _ensemble_predict(self, results: pd.DataFrame) -> np.ndarray:
        """
        Combine predictions from multiple models.
        
        Args:
            results: DataFrame with individual model predictions
            
        Returns:
            Array of ensemble predictions
        """
        method = self.ensemble_config.get('method', 'voting')
        
        # Get prediction columns
        pred_cols = [col for col in results.columns if col.endswith('_prediction')]
        
        if not pred_cols:
            return np.ones(len(results))
        
        if method == 'voting':
            # Majority voting
            votes = results[pred_cols].mode(axis=1)[0]
            return votes.values
        
        elif method == 'weighted':
            # Weighted voting
            weights = self.ensemble_config.get('weights', {})
            
            weighted_sum = np.zeros(len(results))
            total_weight = 0
            
            for col in pred_cols:
                model_name = col.replace('_prediction', '')
                weight = weights.get(model_name, 1.0)
                weighted_sum += results[col].values * weight
                total_weight += weight
            
            # Average and threshold
            avg = weighted_sum / total_weight
            return np.where(avg < 0, -1, 1)
        
        else:
            # Default to voting
            votes = results[pred_cols].mode(axis=1)[0]
            return votes.values
    
    def _ensemble_score(self, results: pd.DataFrame) -> np.ndarray:
        """
        Combine scores from multiple models.
        
        Args:
            results: DataFrame with individual model scores
            
        Returns:
            Array of ensemble scores
        """
        # Get score columns
        score_cols = [col for col in results.columns if col.endswith('_score')]
        
        if not score_cols:
            return np.zeros(len(results))
        
        # Normalize scores to [0, 1]
        normalized_scores = pd.DataFrame()
        
        for col in score_cols:
            scores = results[col].values
            min_score = scores.min()
            max_score = scores.max()
            
            if max_score > min_score:
                normalized = (scores - min_score) / (max_score - min_score)
            else:
                normalized = np.zeros_like(scores)
            
            normalized_scores[col] = normalized
        
        # Average normalized scores
        ensemble_score = normalized_scores.mean(axis=1).values
        
        return ensemble_score
    
    def generate_report(self, anomalies: pd.DataFrame, output_path: str = "reports/detection_report.html"):
        """
        Generate HTML report of detected anomalies.
        
        Args:
            anomalies: DataFrame with anomaly detection results
            output_path: Path to save report
        """
        logger.info(f"Generating detection report")
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Calculate statistics
        total_samples = len(anomalies)
        anomaly_count = anomalies['is_anomaly'].sum()
        anomaly_rate = anomaly_count / total_samples * 100
        
        # Generate HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Anomaly Detection Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .stats {{ background: #f0f0f0; padding: 15px; border-radius: 5px; }}
                .anomaly {{ color: red; font-weight: bold; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
            </style>
        </head>
        <body>
            <h1>Red Team Anomaly Detection Report</h1>
            
            <div class="stats">
                <h2>Summary Statistics</h2>
                <p>Total Samples: {total_samples}</p>
                <p class="anomaly">Anomalies Detected: {anomaly_count} ({anomaly_rate:.2f}%)</p>
                <p>Normal Samples: {total_samples - anomaly_count} ({100 - anomaly_rate:.2f}%)</p>
            </div>
            
            <h2>Top Anomalies</h2>
            <table>
                <tr>
                    <th>Index</th>
                    <th>Ensemble Score</th>
                    <th>Models Agreement</th>
                </tr>
        """
        
        # Add top anomalies
        top_anomalies = anomalies[anomalies['is_anomaly']].nlargest(20, 'ensemble_score')
        
        for idx, row in top_anomalies.iterrows():
            pred_cols = [col for col in anomalies.columns if col.endswith('_prediction')]
            agreement = sum(row[col] == -1 for col in pred_cols)
            
            html += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{row['ensemble_score']:.4f}</td>
                    <td>{agreement}/{len(pred_cols)}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        
        # Save report
        with open(output_file, 'w') as f:
            f.write(html)
        
        logger.success(f"Report saved to {output_path}")
