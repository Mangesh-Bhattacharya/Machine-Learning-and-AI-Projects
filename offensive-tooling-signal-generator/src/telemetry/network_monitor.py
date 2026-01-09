"""
Network Monitor

Captures and analyzes network traffic during tool execution.
"""

from typing import Dict, Any, List
from loguru import logger
import threading
import time
from collections import defaultdict

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    logger.warning("Scapy not available, network monitoring will be limited")
    SCAPY_AVAILABLE = False


class NetworkMonitor:
    """Monitor network traffic during tool execution."""
    
    def __init__(self, interface: str = "eth0", config: Dict = None):
        """
        Initialize network monitor.
        
        Args:
            interface: Network interface to monitor
            config: Network monitoring configuration
        """
        self.interface = interface
        self.config = config or {}
        
        self.packets = []
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Statistics
        self.stats = {
            'total_packets': 0,
            'total_bytes': 0,
            'protocols': defaultdict(int),
            'destinations': set(),
            'ports': defaultdict(int),
            'packet_sizes': [],
            'timestamps': [],
            'syn_packets': 0,
            'failed_connections': 0
        }
        
    def start(self):
        """Start network monitoring."""
        if not SCAPY_AVAILABLE:
            logger.warning("Scapy not available, skipping network monitoring")
            return
        
        logger.info(f"Starting network monitoring on {self.interface}")
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._capture_packets)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def stop(self):
        """Stop network monitoring."""
        logger.info("Stopping network monitoring")
        self.is_monitoring = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _capture_packets(self):
        """Capture network packets."""
        try:
            capture_filter = self.config.get('capture_filter', 'tcp or udp or icmp')
            packet_limit = self.config.get('packet_limit', 10000)
            
            sniff(
                iface=self.interface,
                filter=capture_filter,
                prn=self._process_packet,
                store=False,
                stop_filter=lambda x: not self.is_monitoring,
                count=packet_limit
            )
            
        except Exception as e:
            logger.error(f"Packet capture failed: {e}")
    
    def _process_packet(self, packet):
        """Process captured packet."""
        try:
            timestamp = time.time()
            
            # Extract packet information
            packet_info = {
                'timestamp': timestamp,
                'size': len(packet)
            }
            
            # IP layer
            if IP in packet:
                packet_info['src_ip'] = packet[IP].src
                packet_info['dst_ip'] = packet[IP].dst
                packet_info['protocol'] = packet[IP].proto
                packet_info['ttl'] = packet[IP].ttl
                
                self.stats['destinations'].add(packet[IP].dst)
            
            # TCP layer
            if TCP in packet:
                packet_info['src_port'] = packet[TCP].sport
                packet_info['dst_port'] = packet[TCP].dport
                packet_info['flags'] = packet[TCP].flags
                packet_info['window'] = packet[TCP].window
                
                self.stats['protocols']['TCP'] += 1
                self.stats['ports'][packet[TCP].dport] += 1
                
                # Check for SYN packets
                if packet[TCP].flags & 0x02:  # SYN flag
                    self.stats['syn_packets'] += 1
                
                # Check for RST packets (failed connections)
                if packet[TCP].flags & 0x04:  # RST flag
                    self.stats['failed_connections'] += 1
            
            # UDP layer
            elif UDP in packet:
                packet_info['src_port'] = packet[UDP].sport
                packet_info['dst_port'] = packet[UDP].dport
                
                self.stats['protocols']['UDP'] += 1
                self.stats['ports'][packet[UDP].dport] += 1
            
            # ICMP layer
            elif ICMP in packet:
                packet_info['icmp_type'] = packet[ICMP].type
                packet_info['icmp_code'] = packet[ICMP].code
                
                self.stats['protocols']['ICMP'] += 1
            
            # Update statistics
            self.stats['total_packets'] += 1
            self.stats['total_bytes'] += len(packet)
            self.stats['packet_sizes'].append(len(packet))
            self.stats['timestamps'].append(timestamp)
            
            # Store packet (limited)
            if len(self.packets) < 1000:
                self.packets.append(packet_info)
            
        except Exception as e:
            logger.debug(f"Error processing packet: {e}")
    
    def get_data(self) -> Dict[str, Any]:
        """
        Get collected network data.
        
        Returns:
            Network telemetry dictionary
        """
        return {
            'total_packets': self.stats['total_packets'],
            'total_bytes': self.stats['total_bytes'],
            'protocols': dict(self.stats['protocols']),
            'destinations': list(self.stats['destinations']),
            'top_ports': self._get_top_ports(10),
            'packet_rate': self._calculate_packet_rate(),
            'packet_size_stats': self._calculate_packet_size_stats(),
            'syn_ratio': self._calculate_syn_ratio(),
            'failed_connection_ratio': self._calculate_failed_connection_ratio(),
            'inter_packet_delay': self._calculate_inter_packet_delay(),
            'packets': self.packets[:100]  # Return sample
        }
    
    def get_window_data(self, window_size: int) -> Dict[str, Any]:
        """Get data for a specific time window."""
        current_time = time.time()
        window_start = current_time - window_size
        
        # Filter packets in window
        window_packets = [
            p for p in self.packets
            if p.get('timestamp', 0) >= window_start
        ]
        
        return {
            'window_size': window_size,
            'packet_count': len(window_packets),
            'packets': window_packets
        }
    
    def _get_top_ports(self, n: int) -> List[tuple]:
        """Get top N most accessed ports."""
        sorted_ports = sorted(
            self.stats['ports'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_ports[:n]
    
    def _calculate_packet_rate(self) -> float:
        """Calculate packets per second."""
        if len(self.stats['timestamps']) < 2:
            return 0.0
        
        duration = self.stats['timestamps'][-1] - self.stats['timestamps'][0]
        if duration > 0:
            return self.stats['total_packets'] / duration
        return 0.0
    
    def _calculate_packet_size_stats(self) -> Dict[str, float]:
        """Calculate packet size statistics."""
        if not self.stats['packet_sizes']:
            return {'mean': 0, 'std': 0, 'min': 0, 'max': 0}
        
        import numpy as np
        sizes = np.array(self.stats['packet_sizes'])
        
        return {
            'mean': float(np.mean(sizes)),
            'std': float(np.std(sizes)),
            'min': float(np.min(sizes)),
            'max': float(np.max(sizes))
        }
    
    def _calculate_syn_ratio(self) -> float:
        """Calculate ratio of SYN packets."""
        if self.stats['total_packets'] == 0:
            return 0.0
        return self.stats['syn_packets'] / self.stats['total_packets']
    
    def _calculate_failed_connection_ratio(self) -> float:
        """Calculate ratio of failed connections."""
        if self.stats['total_packets'] == 0:
            return 0.0
        return self.stats['failed_connections'] / self.stats['total_packets']
    
    def _calculate_inter_packet_delay(self) -> Dict[str, float]:
        """Calculate inter-packet delay statistics."""
        if len(self.stats['timestamps']) < 2:
            return {'mean': 0, 'std': 0}
        
        import numpy as np
        timestamps = np.array(self.stats['timestamps'])
        delays = np.diff(timestamps)
        
        return {
            'mean': float(np.mean(delays)),
            'std': float(np.std(delays))
        }
