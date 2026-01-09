"""
Telemetry Collector

Collects comprehensive telemetry during offensive tool execution.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import time
import threading
from contextlib import contextmanager

from .network_monitor import NetworkMonitor
from .process_monitor import ProcessMonitor


class TelemetryCollector:
    """Main telemetry collection orchestrator."""
    
    def __init__(self, config: Dict = None, interface: str = "eth0"):
        """
        Initialize telemetry collector.
        
        Args:
            config: Telemetry configuration
            interface: Network interface to monitor
        """
        self.config = config or {}
        self.interface = interface
        
        # Initialize monitors
        self.network_monitor = NetworkMonitor(
            interface=interface,
            config=self.config.get('network', {})
        )
        
        self.process_monitor = ProcessMonitor(
            config=self.config.get('process', {})
        )
        
        # Telemetry storage
        self.telemetry_data = {
            'network': {},
            'process': {},
            'system': {},
            'timeline': []
        }
        
        self.is_collecting = False
        self.start_time = None
        self.end_time = None
        
    @contextmanager
    def capture(self):
        """
        Context manager for telemetry capture.
        
        Usage:
            with collector.capture():
                # Run tool
                tool.execute()
        """
        self.start()
        try:
            yield self
        finally:
            self.stop()
    
    def start(self):
        """Start telemetry collection."""
        logger.info("Starting telemetry collection")
        
        self.is_collecting = True
        self.start_time = time.time()
        
        # Start monitors
        self.network_monitor.start()
        self.process_monitor.start()
        
        logger.success("Telemetry collection started")
    
    def stop(self):
        """Stop telemetry collection."""
        logger.info("Stopping telemetry collection")
        
        self.is_collecting = False
        self.end_time = time.time()
        
        # Stop monitors
        self.network_monitor.stop()
        self.process_monitor.stop()
        
        # Collect final data
        self._collect_data()
        
        duration = self.end_time - self.start_time
        logger.success(f"Telemetry collection stopped (duration: {duration:.2f}s)")
    
    def _collect_data(self):
        """Collect data from all monitors."""
        # Network telemetry
        self.telemetry_data['network'] = self.network_monitor.get_data()
        
        # Process telemetry
        self.telemetry_data['process'] = self.process_monitor.get_data()
        
        # System telemetry
        self.telemetry_data['system'] = self._collect_system_data()
        
        # Add metadata
        self.telemetry_data['metadata'] = {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration': self.end_time - self.start_time if self.end_time else 0,
            'interface': self.interface
        }
    
    def _collect_system_data(self) -> Dict[str, Any]:
        """Collect system-level telemetry."""
        import psutil
        
        return {
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'network_io': psutil.net_io_counters()._asdict()
        }
    
    def get_telemetry(self) -> Dict[str, Any]:
        """
        Get collected telemetry data.
        
        Returns:
            Complete telemetry dictionary
        """
        return self.telemetry_data
    
    def stream(self, window_size: int = 60):
        """
        Stream telemetry in real-time windows.
        
        Args:
            window_size: Window size in seconds
            
        Yields:
            Telemetry windows
        """
        self.start()
        
        try:
            while self.is_collecting:
                time.sleep(window_size)
                
                # Get current window data
                window_data = {
                    'network': self.network_monitor.get_window_data(window_size),
                    'process': self.process_monitor.get_window_data(window_size),
                    'system': self._collect_system_data(),
                    'timestamp': time.time()
                }
                
                yield window_data
                
        except KeyboardInterrupt:
            logger.info("Streaming stopped by user")
        finally:
            self.stop()
    
    def save_telemetry(self, output_path: str):
        """
        Save telemetry to file.
        
        Args:
            output_path: Path to save telemetry
        """
        import json
        from pathlib import Path
        
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            json.dump(self.telemetry_data, f, indent=2, default=str)
        
        logger.info(f"Telemetry saved to {output_path}")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get telemetry summary statistics.
        
        Returns:
            Summary dictionary
        """
        network_data = self.telemetry_data.get('network', {})
        process_data = self.telemetry_data.get('process', {})
        
        return {
            'duration': self.telemetry_data.get('metadata', {}).get('duration', 0),
            'network': {
                'total_packets': network_data.get('total_packets', 0),
                'total_bytes': network_data.get('total_bytes', 0),
                'unique_destinations': len(network_data.get('destinations', [])),
                'protocols': list(network_data.get('protocols', {}).keys())
            },
            'process': {
                'peak_cpu': process_data.get('peak_cpu', 0),
                'peak_memory': process_data.get('peak_memory', 0),
                'total_syscalls': process_data.get('total_syscalls', 0),
                'child_processes': len(process_data.get('children', []))
            }
        }
