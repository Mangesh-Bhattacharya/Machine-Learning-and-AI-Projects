"""
Nmap Wrapper

Python wrapper for Nmap network scanner with telemetry collection.
"""

import nmap
from typing import Dict, Any, List, Optional
from loguru import logger
import time

from .base_wrapper import BaseWrapper


class NmapWrapper(BaseWrapper):
    """Wrapper for Nmap network scanner."""
    
    def __init__(self, config: Dict = None, telemetry_enabled: bool = True):
        """Initialize Nmap wrapper."""
        super().__init__(config, telemetry_enabled)
        self.scanner = nmap.PortScanner()
        
    def _validate_installation(self):
        """Validate Nmap installation."""
        try:
            self.scanner.nmap_version()
            logger.info(f"Nmap version: {self.scanner.nmap_version()}")
        except Exception as e:
            logger.error(f"Nmap not found or not accessible: {e}")
            raise
    
    def execute(
        self,
        target: str,
        ports: str = "1-1000",
        scan_type: str = "syn",
        arguments: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute Nmap scan.
        
        Args:
            target: Target IP or network (e.g., "192.168.1.0/24")
            ports: Port range (e.g., "1-1000", "80,443,8080")
            scan_type: Scan type (syn, tcp, udp, ack)
            arguments: Additional Nmap arguments
            
        Returns:
            Scan results dictionary
        """
        logger.info(f"Starting Nmap scan: target={target}, ports={ports}, type={scan_type}")
        
        start_time = time.time()
        
        # Build scan arguments
        scan_args = self._build_scan_args(scan_type, arguments)
        
        try:
            # Execute scan
            self.scanner.scan(
                hosts=target,
                ports=ports,
                arguments=scan_args
            )
            
            # Parse results
            results = self._parse_scan_results()
            
            # Add metadata
            results['metadata'] = {
                'target': target,
                'ports': ports,
                'scan_type': scan_type,
                'arguments': scan_args,
                'duration': time.time() - start_time,
                'timestamp': time.time()
            }
            
            logger.success(f"Nmap scan completed in {results['metadata']['duration']:.2f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"Nmap scan failed: {e}")
            raise
    
    def _build_scan_args(self, scan_type: str, additional_args: Optional[str]) -> str:
        """Build Nmap scan arguments."""
        args = []
        
        # Scan type
        if scan_type == "syn":
            args.append("-sS")
        elif scan_type == "tcp":
            args.append("-sT")
        elif scan_type == "udp":
            args.append("-sU")
        elif scan_type == "ack":
            args.append("-sA")
        
        # Default args from config
        default_args = self.config.get('default_args', [])
        args.extend(default_args)
        
        # Additional arguments
        if additional_args:
            args.append(additional_args)
        
        return ' '.join(args)
    
    def _parse_scan_results(self) -> Dict[str, Any]:
        """Parse Nmap scan results."""
        results = {
            'hosts': [],
            'summary': {
                'total_hosts': 0,
                'hosts_up': 0,
                'hosts_down': 0,
                'total_ports_scanned': 0,
                'open_ports': 0,
                'closed_ports': 0,
                'filtered_ports': 0
            }
        }
        
        for host in self.scanner.all_hosts():
            host_info = {
                'ip': host,
                'hostname': self.scanner[host].hostname(),
                'state': self.scanner[host].state(),
                'protocols': {},
                'os': self._get_os_info(host)
            }
            
            # Parse protocols and ports
            for proto in self.scanner[host].all_protocols():
                ports = self.scanner[host][proto].keys()
                host_info['protocols'][proto] = []
                
                for port in ports:
                    port_info = {
                        'port': port,
                        'state': self.scanner[host][proto][port]['state'],
                        'service': self.scanner[host][proto][port].get('name', ''),
                        'product': self.scanner[host][proto][port].get('product', ''),
                        'version': self.scanner[host][proto][port].get('version', ''),
                        'extrainfo': self.scanner[host][proto][port].get('extrainfo', '')
                    }
                    host_info['protocols'][proto].append(port_info)
                    
                    # Update summary
                    results['summary']['total_ports_scanned'] += 1
                    if port_info['state'] == 'open':
                        results['summary']['open_ports'] += 1
                    elif port_info['state'] == 'closed':
                        results['summary']['closed_ports'] += 1
                    elif port_info['state'] == 'filtered':
                        results['summary']['filtered_ports'] += 1
            
            results['hosts'].append(host_info)
            
            # Update host summary
            results['summary']['total_hosts'] += 1
            if host_info['state'] == 'up':
                results['summary']['hosts_up'] += 1
            else:
                results['summary']['hosts_down'] += 1
        
        return results
    
    def _get_os_info(self, host: str) -> Dict[str, Any]:
        """Extract OS detection information."""
        try:
            if 'osmatch' in self.scanner[host]:
                os_matches = self.scanner[host]['osmatch']
                if os_matches:
                    return {
                        'name': os_matches[0].get('name', ''),
                        'accuracy': os_matches[0].get('accuracy', 0),
                        'type': os_matches[0].get('osclass', [{}])[0].get('type', '')
                    }
        except Exception:
            pass
        
        return {}
    
    def scan_top_ports(self, target: str, top: int = 100) -> Dict[str, Any]:
        """
        Scan top N most common ports.
        
        Args:
            target: Target IP or network
            top: Number of top ports to scan
            
        Returns:
            Scan results
        """
        return self.execute(
            target=target,
            ports=None,
            arguments=f"--top-ports {top}"
        )
    
    def service_version_scan(self, target: str, ports: str = "1-1000") -> Dict[str, Any]:
        """
        Perform service version detection scan.
        
        Args:
            target: Target IP or network
            ports: Port range
            
        Returns:
            Scan results with version information
        """
        return self.execute(
            target=target,
            ports=ports,
            arguments="-sV"
        )
    
    def os_detection_scan(self, target: str) -> Dict[str, Any]:
        """
        Perform OS detection scan.
        
        Args:
            target: Target IP or network
            
        Returns:
            Scan results with OS information
        """
        return self.execute(
            target=target,
            ports="1-1000",
            arguments="-O"
        )
    
    def aggressive_scan(self, target: str) -> Dict[str, Any]:
        """
        Perform aggressive scan (OS, version, script, traceroute).
        
        Args:
            target: Target IP or network
            
        Returns:
            Comprehensive scan results
        """
        return self.execute(
            target=target,
            ports="1-1000",
            arguments="-A"
        )
