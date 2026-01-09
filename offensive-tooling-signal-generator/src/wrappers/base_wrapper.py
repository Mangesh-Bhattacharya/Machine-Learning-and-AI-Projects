"""
Base Wrapper Class

Abstract base class for all offensive tool wrappers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger
import subprocess
import json
from pathlib import Path


class BaseWrapper(ABC):
    """Abstract base class for tool wrappers."""
    
    def __init__(self, config: Dict = None, telemetry_enabled: bool = True):
        """
        Initialize base wrapper.
        
        Args:
            config: Tool-specific configuration
            telemetry_enabled: Whether to collect telemetry
        """
        self.config = config or {}
        self.telemetry_enabled = telemetry_enabled
        self.tool_name = self.__class__.__name__.replace('Wrapper', '').lower()
        
        # Validate tool installation
        self._validate_installation()
        
    @abstractmethod
    def _validate_installation(self):
        """Validate that the tool is installed and accessible."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.
        
        Returns:
            Dictionary containing execution results
        """
        pass
    
    def _run_command(
        self,
        command: list,
        timeout: Optional[int] = None,
        capture_output: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Run a command and return the result.
        
        Args:
            command: Command and arguments as list
            timeout: Timeout in seconds
            capture_output: Whether to capture stdout/stderr
            
        Returns:
            CompletedProcess object
        """
        logger.debug(f"Running command: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout or self.config.get('timeout', 300),
                check=False
            )
            
            return result
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(command)}")
            raise
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise
    
    def _parse_output(self, output: str, format: str = 'text') -> Any:
        """
        Parse tool output.
        
        Args:
            output: Raw output string
            format: Output format (text, json, xml)
            
        Returns:
            Parsed output
        """
        if format == 'json':
            try:
                return json.loads(output)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON output")
                return {'raw': output}
        
        elif format == 'xml':
            try:
                import xml.etree.ElementTree as ET
                return ET.fromstring(output)
            except Exception:
                logger.warning("Failed to parse XML output")
                return {'raw': output}
        
        return output
    
    def get_tool_signature(self) -> Dict[str, Any]:
        """
        Get tool-specific signature characteristics.
        
        Returns:
            Dictionary of signature features
        """
        return {
            'tool_name': self.tool_name,
            'version': self._get_version(),
            'binary_path': self.config.get('binary_path', ''),
            'default_args': self.config.get('default_args', [])
        }
    
    def _get_version(self) -> str:
        """Get tool version."""
        try:
            binary = self.config.get('binary_path', self.tool_name)
            result = subprocess.run(
                [binary, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip().split('\n')[0]
        except Exception:
            return 'unknown'
    
    def _save_results(self, results: Dict, output_path: Optional[str] = None):
        """Save execution results to file."""
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Results saved to {output_path}")
