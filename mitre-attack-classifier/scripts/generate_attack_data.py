#!/usr/bin/env python3
"""
Generate Attack Data Script

Generates synthetic attack logs labeled with MITRE ATT&CK techniques.

Usage:
    python scripts/generate_attack_data.py --output data/raw/attack_logs.json --num-samples 50000
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data.generator import AttackDataGenerator
from data.mitre_mapper import MITREMapper
from loguru import logger


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic attack data with MITRE ATT&CK labels"
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='data/raw/attack_logs.json',
        help='Output file path'
    )
    
    parser.add_argument(
        '--num-samples',
        type=int,
        default=50000,
        help='Number of samples to generate'
    )
    
    parser.add_argument(
        '--techniques',
        type=int,
        default=50,
        help='Number of MITRE ATT&CK techniques to include'
    )
    
    parser.add_argument(
        '--save-mapping',
        action='store_true',
        help='Save MITRE ATT&CK mapping to JSON'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    try:
        # Initialize generator
        config = {
            'num_samples': args.num_samples,
            'techniques_count': args.techniques
        }
        
        generator = AttackDataGenerator(config)
        
        # Generate dataset
        dataset = generator.generate_dataset(
            num_samples=args.num_samples,
            techniques_count=args.techniques
        )
        
        # Save dataset
        generator.save_data(dataset, args.output)
        
        # Optionally save MITRE mapping
        if args.save_mapping:
            mapping_path = Path(args.output).parent / 'mitre_attack_mapping.json'
            generator.mitre.save_mapping(str(mapping_path))
        
        logger.success("Data generation complete!")
        
    except Exception as e:
        logger.exception(f"Data generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
