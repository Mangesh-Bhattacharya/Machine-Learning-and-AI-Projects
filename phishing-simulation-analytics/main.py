#!/usr/bin/env python3
"""
Phishing Simulation Analytics - Main Entry Point

Orchestrates phishing campaigns, tracking, ML training, and API serving.

Usage:
    python main.py --mode campaign --template office365_login --targets users.csv
    python main.py --mode train --data data/training/user_behavior.parquet
    python main.py --mode serve --port 8000
"""

import argparse
import sys
from pathlib import Path
import yaml
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from campaigns import CampaignManager
from email import EmailSender
from ml import ModelTrainer, RiskPredictor
from api import start_server


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def run_campaign(config: dict, args):
    """
    Run a phishing simulation campaign.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
    """
    logger.info(f"Starting campaign: {args.name}")
    
    # Initialize campaign manager
    manager = CampaignManager(config=config['campaigns'])
    
    # Load targets
    targets = []
    if args.targets:
        import pandas as pd
        df = pd.read_csv(args.targets)
        targets = df['email'].tolist()
    
    # Create campaign
    campaign = manager.create_campaign(
        name=args.name,
        template=args.template,
        targets=targets,
        schedule=args.schedule
    )
    
    logger.info(f"Campaign created: {campaign.id}")
    logger.info(f"Targets: {len(targets)}")
    
    # Send emails if not scheduled
    if not args.schedule:
        sender = EmailSender(config=config['email'])
        results = sender.send_campaign(campaign)
        
        logger.success(f"Campaign sent: {results['sent']}/{results['total']} emails")
    else:
        logger.info(f"Campaign scheduled for: {args.schedule}")
    
    return campaign


def train_model(config: dict, args):
    """
    Train ML model for risk prediction.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
    """
    logger.info("Training risk prediction model")
    
    # Load training data
    import pandas as pd
    data = pd.read_parquet(args.data)
    
    logger.info(f"Loaded {len(data)} training samples")
    
    # Initialize trainer
    trainer = ModelTrainer(config=config['ml'])
    
    # Train model
    model = trainer.train(
        data=data,
        model_type=args.model,
        target_column='clicked'
    )
    
    # Evaluate
    metrics = trainer.evaluate(model, data)
    
    logger.info("Model Performance:")
    logger.info(f"  Accuracy:  {metrics['accuracy']:.3f}")
    logger.info(f"  Precision: {metrics['precision']:.3f}")
    logger.info(f"  Recall:    {metrics['recall']:.3f}")
    logger.info(f"  F1-Score:  {metrics['f1_score']:.3f}")
    logger.info(f"  AUC-ROC:   {metrics['auc_roc']:.3f}")
    
    # Save model
    model_path = config['ml']['model_dir'] / f"{args.model}_risk_predictor.pkl"
    trainer.save_model(model, model_path)
    
    logger.success(f"Model saved to {model_path}")


def evaluate_model(config: dict, args):
    """
    Evaluate trained model.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
    """
    logger.info("Evaluating model")
    
    # Load model
    predictor = RiskPredictor(model_path=args.model)
    
    # Load test data
    import pandas as pd
    test_data = pd.read_parquet(args.test_data)
    
    # Evaluate
    metrics = predictor.evaluate(test_data)
    
    logger.info("Evaluation Results:")
    for metric, value in metrics.items():
        logger.info(f"  {metric}: {value:.3f}")


def get_user_risk(config: dict, args):
    """
    Get risk score for a user.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
    """
    logger.info(f"Getting risk score for {args.email}")
    
    # Load model
    predictor = RiskPredictor(
        model_path=config['ml']['model_path'],
        config=config['ml']
    )
    
    # Get risk score
    risk_score = predictor.predict_user_risk(args.email)
    
    logger.info(f"Risk Score: {risk_score:.1f}/100")
    logger.info(f"Risk Level: {predictor.get_risk_level(risk_score)}")


def view_results(config: dict, args):
    """
    View campaign results.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
    """
    logger.info(f"Viewing results for campaign: {args.campaign_id}")
    
    manager = CampaignManager(config=config['campaigns'])
    results = manager.get_campaign_results(args.campaign_id)
    
    logger.info("Campaign Results:")
    logger.info(f"  Emails Sent:    {results['total_sent']}")
    logger.info(f"  Opened:         {results['opened']} ({results['open_rate']:.1%})")
    logger.info(f"  Clicked:        {results['clicked']} ({results['click_rate']:.1%})")
    logger.info(f"  Submitted:      {results['submitted']} ({results['submit_rate']:.1%})")
    logger.info(f"  Avg Time to Click: {results['avg_time_to_click']:.1f}s")


def serve_api(config: dict, args):
    """
    Start API server.
    
    Args:
        config: Configuration dictionary
        args: Command line arguments
    """
    logger.info(f"Starting API server on {args.host}:{args.port}")
    
    api_config = config.get('api', {})
    api_config['host'] = args.host
    api_config['port'] = args.port
    
    start_server(api_config)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Phishing Simulation Analytics with ML"
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['campaign', 'train', 'evaluate', 'risk', 'results', 'serve'],
        required=True,
        help='Execution mode'
    )
    
    # Campaign arguments
    parser.add_argument('--name', type=str, help='Campaign name')
    parser.add_argument('--template', type=str, help='Email template')
    parser.add_argument('--targets', type=str, help='Target users CSV file')
    parser.add_argument('--schedule', type=str, help='Schedule time (ISO format)')
    
    # Training arguments
    parser.add_argument('--data', type=str, help='Training data path')
    parser.add_argument('--model', type=str, default='random_forest', help='Model type')
    parser.add_argument('--test-data', type=str, help='Test data path')
    
    # Risk scoring arguments
    parser.add_argument('--email', type=str, help='User email')
    
    # Results arguments
    parser.add_argument('--campaign-id', type=str, help='Campaign ID')
    
    # Server arguments
    parser.add_argument('--host', type=str, default='0.0.0.0', help='API host')
    parser.add_argument('--port', type=int, default=8000, help='API port')
    
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.add("logs/phishing_{time}.log", rotation="500 MB", level=log_level)
    
    # Load configuration
    config = load_config(args.config)
    
    # Execute based on mode
    try:
        if args.mode == 'campaign':
            if not args.name or not args.template:
                logger.error("--name and --template are required for campaign mode")
                sys.exit(1)
            run_campaign(config, args)
        
        elif args.mode == 'train':
            if not args.data:
                logger.error("--data is required for train mode")
                sys.exit(1)
            train_model(config, args)
        
        elif args.mode == 'evaluate':
            if not args.model or not args.test_data:
                logger.error("--model and --test-data are required for evaluate mode")
                sys.exit(1)
            evaluate_model(config, args)
        
        elif args.mode == 'risk':
            if not args.email:
                logger.error("--email is required for risk mode")
                sys.exit(1)
            get_user_risk(config, args)
        
        elif args.mode == 'results':
            if not args.campaign_id:
                logger.error("--campaign-id is required for results mode")
                sys.exit(1)
            view_results(config, args)
        
        elif args.mode == 'serve':
            serve_api(config, args)
    
    except Exception as e:
        logger.exception(f"Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
