#!/usr/bin/env python3
"""
MITRE ATT&CK Attack Classifier - Main Entry Point

This script orchestrates the entire pipeline from data generation to model training
and API deployment for MITRE ATT&CK technique classification.

Usage:
    python main.py --mode train --config config/model_config.yaml
    python main.py --mode predict --input data/test/test_logs.json
    python main.py --mode serve --port 8000
"""

import argparse
import sys
from pathlib import Path
import yaml
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data.generator import AttackDataGenerator
from features.extractor import FeatureExtractor
from models.trainer import ModelTrainer
from api.server import start_server
from utils.metrics import evaluate_multilabel_model


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def run_data_generation(config: dict):
    """Generate synthetic attack data with MITRE ATT&CK labels."""
    logger.info("Generating attack data with MITRE ATT&CK labels")
    
    generator = AttackDataGenerator(config['data'])
    
    # Generate training data
    train_data = generator.generate_dataset(
        num_samples=config['data']['num_samples'],
        techniques_count=config['data']['techniques_count']
    )
    
    # Save data
    output_path = config['data']['output_path']
    generator.save_data(train_data, output_path)
    
    logger.success(f"Generated {len(train_data)} samples")
    logger.info(f"Data saved to {output_path}")


def run_training(config: dict, model_name: str = None):
    """Train MITRE ATT&CK classifier models."""
    logger.info("Starting model training")
    
    # Load data
    logger.info("Loading training data")
    data_path = config['data']['processed_path']
    
    # Extract features
    logger.info("Extracting features")
    extractor = FeatureExtractor(config['features'])
    X_train, y_train, X_test, y_test = extractor.load_and_process(data_path)
    
    # Train models
    trainer = ModelTrainer(config['models'])
    
    if model_name:
        # Train specific model
        logger.info(f"Training {model_name}")
        model = trainer.train_model(model_name, X_train, y_train)
        trainer.save_model(model, model_name)
        
        # Evaluate
        metrics = evaluate_multilabel_model(model, X_test, y_test)
        logger.info(f"Model Metrics: {metrics}")
    else:
        # Train all models
        models = trainer.train_all_models(X_train, y_train)
        
        # Evaluate each model
        for name, model in models.items():
            metrics = evaluate_multilabel_model(model, X_test, y_test)
            logger.info(f"{name} Metrics: {metrics}")
    
    logger.success("Training complete!")


def run_prediction(config: dict, input_path: str):
    """Run predictions on new data."""
    logger.info(f"Running predictions on {input_path}")
    
    # Load model
    trainer = ModelTrainer(config['models'])
    model = trainer.load_model(config['models']['default_model'])
    
    # Load and process input data
    extractor = FeatureExtractor(config['features'])
    X = extractor.transform_logs(input_path)
    
    # Predict
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    # Map to technique IDs
    technique_ids = extractor.get_technique_labels()
    
    # Generate report
    results = []
    for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
        techniques = [
            {
                'id': technique_ids[j],
                'confidence': float(probs[j])
            }
            for j, val in enumerate(pred) if val == 1
        ]
        results.append({
            'sample_id': i,
            'techniques': techniques
        })
    
    # Save results
    output_path = Path(input_path).parent / 'predictions.json'
    import json
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.success(f"Predictions saved to {output_path}")


def run_server(config: dict, host: str, port: int):
    """Start the FastAPI server."""
    logger.info(f"Starting API server on {host}:{port}")
    
    api_config = config.get('api', {})
    api_config['host'] = host
    api_config['port'] = port
    
    start_server(api_config)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MITRE ATT&CK Attack Classifier"
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/model_config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['generate', 'train', 'predict', 'serve'],
        default='train',
        help='Execution mode'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['random_forest', 'neural_network', 'ensemble'],
        help='Model to train (for train mode)'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Input data path (for predict mode)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='API server host (for serve mode)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='API server port (for serve mode)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.add("logs/classifier_{time}.log", rotation="500 MB", level=log_level)
    
    # Load configuration
    config = load_config(args.config)
    
    # Execute based on mode
    try:
        if args.mode == 'generate':
            run_data_generation(config)
        elif args.mode == 'train':
            run_training(config, args.model)
        elif args.mode == 'predict':
            if not args.input:
                logger.error("--input is required for predict mode")
                sys.exit(1)
            run_prediction(config, args.input)
        elif args.mode == 'serve':
            run_server(config, args.host, args.port)
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
