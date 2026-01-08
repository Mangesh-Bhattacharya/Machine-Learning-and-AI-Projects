#!/usr/bin/env python3
"""
Red Team Anomaly Detection Pipeline - Main Entry Point

This script orchestrates the entire pipeline from data ingestion to model training
and anomaly detection.

Usage:
    python main.py --config config/pipeline_config.yaml
    python main.py --mode train --model isolation_forest
    python main.py --mode detect --input data/test/test_logs.json
"""

import argparse
import sys
from pathlib import Path
import yaml
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_ingestion.ingest import DataIngestion
from feature_engineering.engineer_features import FeatureEngineer
from models.train import ModelTrainer
from pipeline.detect import AnomalyDetector
from utils.metrics import evaluate_model


def load_config(config_path: str) -> dict:
    """Load pipeline configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def run_full_pipeline(config: dict):
    """Execute the complete pipeline."""
    logger.info("Starting Red Team Anomaly Detection Pipeline")
    
    # Step 1: Data Ingestion
    logger.info("Step 1: Data Ingestion")
    ingestion = DataIngestion(config['data'])
    raw_data = ingestion.load_logs(config['data']['input_path'])
    clean_data = ingestion.clean_data(raw_data)
    ingestion.save_processed_data(clean_data, config['data']['processed_path'])
    
    # Step 2: Feature Engineering
    logger.info("Step 2: Feature Engineering")
    engineer = FeatureEngineer(config['features'])
    features = engineer.transform(clean_data)
    engineer.save_features(features, config['features']['output_path'])
    
    # Step 3: Model Training
    logger.info("Step 3: Model Training")
    trainer = ModelTrainer(config['models'])
    
    for model_name in config['models']['enabled_models']:
        logger.info(f"Training {model_name}")
        model = trainer.train_model(model_name, features)
        trainer.save_model(model, model_name)
        
        # Evaluate
        metrics = evaluate_model(model, features)
        logger.info(f"{model_name} Metrics: {metrics}")
    
    # Step 4: Detection Pipeline
    logger.info("Step 4: Setting up Detection Pipeline")
    detector = AnomalyDetector(config['detection'])
    detector.load_models(config['models']['model_dir'])
    
    logger.info("Pipeline completed successfully!")
    logger.info(f"Models saved to: {config['models']['model_dir']}")
    logger.info(f"Features saved to: {config['features']['output_path']}")


def run_training_only(config: dict, model_name: str):
    """Run only the training phase."""
    logger.info(f"Training {model_name} model")
    
    # Load features
    engineer = FeatureEngineer(config['features'])
    features = engineer.load_features(config['features']['output_path'])
    
    # Train model
    trainer = ModelTrainer(config['models'])
    model = trainer.train_model(model_name, features)
    trainer.save_model(model, model_name)
    
    # Evaluate
    metrics = evaluate_model(model, features)
    logger.info(f"Model Metrics: {metrics}")
    logger.success(f"Model saved successfully!")


def run_detection_only(config: dict, input_path: str):
    """Run only the detection phase on new data."""
    logger.info("Running anomaly detection on new data")
    
    # Load and process new data
    ingestion = DataIngestion(config['data'])
    raw_data = ingestion.load_logs(input_path)
    clean_data = ingestion.clean_data(raw_data)
    
    # Engineer features
    engineer = FeatureEngineer(config['features'])
    features = engineer.transform(clean_data)
    
    # Detect anomalies
    detector = AnomalyDetector(config['detection'])
    detector.load_models(config['models']['model_dir'])
    
    anomalies = detector.detect(features)
    
    # Generate report
    detector.generate_report(anomalies, output_path="reports/detection_report.html")
    
    logger.success(f"Detected {len(anomalies)} anomalies")
    logger.info("Report saved to: reports/detection_report.html")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Red Team Anomaly Detection Pipeline"
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/pipeline_config.yaml',
        help='Path to pipeline configuration file'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['full', 'train', 'detect'],
        default='full',
        help='Pipeline execution mode'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        choices=['isolation_forest', 'autoencoder', 'one_class_svm', 'lstm'],
        help='Model to train (for train mode)'
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help='Input data path (for detect mode)'
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
    logger.add("logs/pipeline_{time}.log", rotation="500 MB", level=log_level)
    
    # Load configuration
    config = load_config(args.config)
    
    # Execute based on mode
    try:
        if args.mode == 'full':
            run_full_pipeline(config)
        elif args.mode == 'train':
            if not args.model:
                logger.error("--model is required for train mode")
                sys.exit(1)
            run_training_only(config, args.model)
        elif args.mode == 'detect':
            if not args.input:
                logger.error("--input is required for detect mode")
                sys.exit(1)
            run_detection_only(config, args.input)
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
