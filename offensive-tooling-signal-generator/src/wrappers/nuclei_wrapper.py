"""
Nuclei Wrapper

Python wrapper for Nuclei vulnerability scanner with telemetry collection.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import time
import json

from .base_wrapper import BaseWrapper


class NucleiWrapper(BaseWrapper):
    """Wrapper for Nuclei vulnerability scanner."""
    
    def __init__(self, config: Dict = None, telemetry_enabled: bool = True):
        """Initialize Nuclei wrapper."""
        super().__init__(config, telemetry_enabled)
        
    def _validate_installation(self):
        """Validate Nuclei installation."""
        try:
            binary = self.config.get('binary_path', 'nuclei')
            result = self._run_command([binary, '-version'], timeout=5)
            logger.info(f"Nuclei installed: {result.stdout.strip()}")
        except Exception as e:
            logger.error(f"Nuclei not found or not accessible: {e}")
            raise
    
    def execute(
        self,
        target: str,
        templates: Optional[List[str]] = None,
        severity: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute Nuclei scan.
        
        Args:
            target: Target URL or file with URLs
            templates: List of template paths or IDs
            severity: Severity levels to scan (info, low, medium, high, critical)
            tags: Template tags to use
            
        Returns:
            Scan results dictionary
        """
        logger.info(f"Starting Nuclei scan: target={target}")
        
        start_time = time.time()
        
        # Build command
        command = self._build_command(target, templates, severity, tags)
        
        try:
            # Execute scan
            result = self._run_command(command)
            
            # Parse results
            results = self._parse_results(result.stdout)
            
            # Add metadata
            results['metadata'] = {
                'target': target,
                'templates': templates,
                'severity': severity,
                'tags': tags,
                'duration': time.time() - start_time,
                'timestamp': time.time()
            }
            
            logger.success(
                f"Nuclei scan completed: {results['summary']['total_findings']} findings "
                f"in {results['metadata']['duration']:.2f}s"
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Nuclei scan failed: {e}")
            raise
    
    def _build_command(
        self,
        target: str,
        templates: Optional[List[str]],
        severity: Optional[List[str]],
        tags: Optional[List[str]]
    ) -> List[str]:
        """Build Nuclei command."""
        binary = self.config.get('binary_path', 'nuclei')
        command = [binary]
        
        # Target
        command.extend(['-u', target])
        
        # Templates
        if templates:
            for template in templates:
                command.extend(['-t', template])
        else:
            # Use default templates directory
            templates_dir = self.config.get('templates_dir')
            if templates_dir:
                command.extend(['-t', templates_dir])
        
        # Severity
        if severity:
            command.extend(['-severity', ','.join(severity)])
        
        # Tags
        if tags:
            command.extend(['-tags', ','.join(tags)])
        
        # Default args
        default_args = self.config.get('default_args', ['-silent', '-json'])
        command.extend(default_args)
        
        return command
    
    def _parse_results(self, output: str) -> Dict[str, Any]:
        """Parse Nuclei JSON output."""
        results = {
            'findings': [],
            'summary': {
                'total_findings': 0,
                'by_severity': {
                    'info': 0,
                    'low': 0,
                    'medium': 0,
                    'high': 0,
                    'critical': 0
                },
                'by_type': {}
            }
        }
        
        # Parse JSON lines
        for line in output.strip().split('\n'):
            if not line:
                continue
            
            try:
                finding = json.loads(line)
                
                # Extract relevant information
                parsed_finding = {
                    'template_id': finding.get('template-id', ''),
                    'name': finding.get('info', {}).get('name', ''),
                    'severity': finding.get('info', {}).get('severity', 'info'),
                    'type': finding.get('type', ''),
                    'host': finding.get('host', ''),
                    'matched_at': finding.get('matched-at', ''),
                    'extracted_results': finding.get('extracted-results', []),
                    'curl_command': finding.get('curl-command', ''),
                    'matcher_name': finding.get('matcher-name', ''),
                    'timestamp': finding.get('timestamp', '')
                }
                
                results['findings'].append(parsed_finding)
                
                # Update summary
                results['summary']['total_findings'] += 1
                
                severity = parsed_finding['severity'].lower()
                if severity in results['summary']['by_severity']:
                    results['summary']['by_severity'][severity] += 1
                
                finding_type = parsed_finding['type']
                results['summary']['by_type'][finding_type] = \
                    results['summary']['by_type'].get(finding_type, 0) + 1
                
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON line: {line[:100]}")
                continue
        
        return results
    
    def scan_with_custom_templates(
        self,
        target: str,
        template_paths: List[str]
    ) -> Dict[str, Any]:
        """
        Scan with custom template files.
        
        Args:
            target: Target URL
            template_paths: List of custom template file paths
            
        Returns:
            Scan results
        """
        return self.execute(target=target, templates=template_paths)
    
    def scan_by_severity(
        self,
        target: str,
        severity: List[str]
    ) -> Dict[str, Any]:
        """
        Scan with specific severity levels.
        
        Args:
            target: Target URL
            severity: List of severity levels
            
        Returns:
            Scan results
        """
        return self.execute(target=target, severity=severity)
    
    def scan_by_tags(
        self,
        target: str,
        tags: List[str]
    ) -> Dict[str, Any]:
        """
        Scan with specific template tags.
        
        Args:
            target: Target URL
            tags: List of template tags
            
        Returns:
            Scan results
        """
        return self.execute(target=target, tags=tags)
    
    def update_templates(self) -> bool:
        """
        Update Nuclei templates.
        
        Returns:
            True if successful
        """
        logger.info("Updating Nuclei templates")
        
        try:
            binary = self.config.get('binary_path', 'nuclei')
            result = self._run_command([binary, '-update-templates'])
            
            logger.success("Templates updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update templates: {e}")
            return False
