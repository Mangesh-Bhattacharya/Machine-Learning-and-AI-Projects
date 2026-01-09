#!/usr/bin/env python3
"""
Offensive Tooling Signal Generator - Main Entry Point

Orchestrates tool execution, telemetry collection, and ML model training/inference.

Usage:
    python main.py --mode generate --tool nmap --target 192.168.1.0/24
    python main.py --mode train --dataset data/training/signals.parquet
    python main.py --mode monitor --interface eth0
"""

import argparse
import sys
from pathlib import Path
import yaml
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wrappers import (
    NmapWrapper,
    NucleiWrapper,
    MetasploitWrapper,
    SQLMapWrapper,
    HydraWrapper
)
from telemetry import TelemetryCollector
from features import FeatureExtractor
from ml import DatasetBuilder, ModelTrainer, ToolDetector


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def run_tool_with_telemetry(tool_name: str, config: dict, **kwargs):
    """
    Execute offensive tool with telemetry collection.
    
    Args:
        tool_name: Name of the tool to run
        config: Configuration dictionary
        **kwargs: Tool-specific arguments
    """
    logger.info(f"Running {tool_name} with telemetry collection")
    
    # Initialize tool wrapper
    tool_wrappers = {
        'nmap': NmapWrapper,
        'nuclei': NucleiWrapper,
        'metasploit': MetasploitWrapper,
        'sqlmap': SQLMapWrapper,
        'hydra': HydraWrapper
    }
    
    if tool_name not in tool_wrappers:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    wrapper_class = tool_wrappers[tool_name]
    wrapper = wrapper_class(config=config.get('tools', {}).get(tool_name, {}))
    
    # Initialize telemetry collector
    collector = TelemetryCollector(config=config.get('telemetry', {}))
    
    # Run tool with telemetry
    with collector.capture():
        results = wrapper.execute(**kwargs)
    
    # Extract features
    telemetry = collector.get_telemetry()
    extractor = FeatureExtractor(config=config.get('features', {}))
    features = extractor.extract(telemetry, tool_name=tool_name)
    
    # Save results
    output_dir = Path(config.get('output_dir', 'data/telemetry'))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{tool_name}_{int(time.time())}.json"
    
    import json
    with open(output_file, 'w') as f:
        json.dump({
            'tool': tool_name,
            'results': results,
            'telemetry': telemetry,
            'features': features
        }, f, indent=2)
    
    logger.success(f"Telemetry saved to {output_file}")
    logger.info(f"Scan fingerprint: {features.get('fingerprint', {})}")
    
    return features


def generate_dataset(config: dict, tools: list, samples_per_tool: int):
    """
    Generate training dataset with multiple tools.
    
    Args:
        config: Configuration dictionary
        tools: List of tools to include
        samples_per_tool: Number of samples per tool
    """
    logger.info(f"Generating dataset with {len(tools)} tools, {samples_per_tool} samples each")
    
    builder = DatasetBuilder(config=config)
    
    for tool in tools:
        logger.info(f"Generating samples for {tool}")
        builder.generate_tool_samples(
            tool_name=tool,
            num_samples=samples_per_tool
        )
    
    # Build final dataset
    dataset = builder.build()
    
    # Save dataset
    output_path = config.get('dataset_output', 'data/training/offensive_signals.parquet')
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    dataset.to_parquet(output_path)
    logger.success(f"Dataset saved to {output_path}")
    logger.info(f"Total samples: {len(dataset)}")
    logger.info(f"Features: {dataset.shape[1]}")


def train_detection_model(config: dict, dataset_path: str, model_type: str):
    """
    Train tool detection model.
    
    Args:
        config: Configuration dictionary
        dataset_path: Path to training dataset
        model_type: Type of model to train
    """
    logger.info(f"Training {model_type} model")
    
    # Load dataset
    import pandas as pd
    dataset = pd.read_parquet(dataset_path)
    
    logger.info(f"Loaded {len(dataset)} samples")
    
    # Initialize trainer
    trainer = ModelTrainer(config=config.get('ml', {}))
    
    # Train model
    model = trainer.train(
        dataset=dataset,
        model_type=model_type
    )
    
    # Evaluate
    metrics = trainer.evaluate(model, dataset)
    logger.info(f"Model metrics: {metrics}")
    
    # Save model
    model_path = config.get('model_output', f'models/{model_type}_detector.pkl')
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    
    trainer.save_model(model, model_path)
    logger.success(f"Model saved to {model_path}")


def run_real_time_monitoring(config: dict, interface: str, model_path: str):
    """
    Run real-time tool detection monitoring.
    
    Args:
        config: Configuration dictionary
        interface: Network interface to monitor
        model_path: Path to trained model
    """
    logger.info(f"Starting real-time monitoring on {interface}")
    
    # Load model
    detector = ToolDetector(model_path=model_path, config=config)
    
    # Initialize telemetry collector
    collector = TelemetryCollector(
        config=config.get('telemetry', {}),
        interface=interface
    )
    
    # Start monitoring
    logger.info("Monitoring for offensive tool activity...")
    
    try:
        for telemetry_window in collector.stream():
            # Extract features
            extractor = FeatureExtractor(config=config.get('features', {}))
            features = extractor.extract(telemetry_window)
            
            # Detect tool
            detection = detector.detect(features)
            
            if detection['is_offensive_tool']:
                logger.warning(
                    f"Detected: {detection['tool']} "
                    f"(confidence: {detection['confidence']:.2%})"
                )
                
                # Send to SIEM if configured
                if config.get('siem', {}).get('enabled'):
                    send_to_siem(detection, config)
    
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")


def send_to_siem(detection: dict, config: dict):
    """Send detection to SIEM system."""
    siem_type = config['siem']['type']
    
    if siem_type == 'splunk':
        from integrations import SplunkConnector
        connector = SplunkConnector(config['siem']['splunk'])
        connector.send_event(detection)
    
    elif siem_type == 'elastic':
        from integrations import ElasticConnector
        connector = ElasticConnector(config['siem']['elastic'])
        connector.index_detection(detection)
    
    elif siem_type == 'sentinel':
        from integrations import SentinelConnector
        connector = SentinelConnector(config['siem']['sentinel'])
        connector.send_alert(detection)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Offensive Tooling Signal Generator for EDR/SIEM"
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/tools_config.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['generate', 'dataset', 'train', 'monitor', 'detect'],
        required=True,
        help='Execution mode'
    )
    
    # Tool execution arguments
    parser.add_argument('--tool', type=str, help='Tool to execute')
    parser.add_argument('--target', type=str, help='Target for tool')
    parser.add_argument('--ports', type=str, help='Ports to scan')
    
    # Dataset generation arguments
    parser.add_argument('--tools', type=str, help='Comma-separated list of tools')
    parser.add_argument('--samples', type=int, default=1000, help='Samples per tool')
    
    # Training arguments
    parser.add_argument('--dataset', type=str, help='Path to training dataset')
    parser.add_argument('--model', type=str, default='random_forest', help='Model type')
    
    # Monitoring arguments
    parser.add_argument('--interface', type=str, default='eth0', help='Network interface')
    parser.add_argument('--model-path', type=str, help='Path to trained model')
    
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    logger.add("logs/signal_generator_{time}.log", rotation="500 MB", level=log_level)
    
    # Load configuration
    config = load_config(args.config)
    
    # Execute based on mode
    try:
        if args.mode == 'generate':
            if not args.tool or not args.target:
                logger.error("--tool and --target are required for generate mode")
                sys.exit(1)
            
            run_tool_with_telemetry(
                tool_name=args.tool,
                config=config,
                target=args.target,
                ports=args.ports
            )
        
        elif args.mode == 'dataset':
            if not args.tools:
                logger.error("--tools is required for dataset mode")
                sys.exit(1)
            
            tools = args.tools.split(',')
            generate_dataset(config, tools, args.samples)
        
        elif args.mode == 'train':
            if not args.dataset:
                logger.error("--dataset is required for train mode")
                sys.exit(1)
            
            train_detection_model(config, args.dataset, args.model)
        
        elif args.mode == 'monitor':
            if not args.model_path:
                logger.error("--model-path is required for monitor mode")
                sys.exit(1)
            
            run_real_time_monitoring(config, args.interface, args.model_path)
        
        elif args.mode == 'detect':
            # Single detection mode
            logger.info("Single detection mode not yet implemented")
    
    except Exception as e:
        logger.exception(f"Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import time
    main()
