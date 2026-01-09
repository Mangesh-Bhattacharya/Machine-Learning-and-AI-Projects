"""
Link Tracker

Tracks link clicks in phishing emails.
"""

from typing import Dict, Any, Optional
from loguru import logger
import time
from datetime import datetime
import hashlib


class LinkTracker:
    """Tracks link clicks in phishing simulations."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize link tracker.
        
        Args:
            config: Tracking configuration
        """
        self.config = config or {}
        self.clicks = {}
        
    def generate_tracking_token(
        self,
        campaign_id: str,
        user_email: str
    ) -> str:
        """
        Generate unique tracking token.
        
        Args:
            campaign_id: Campaign ID
            user_email: User email
            
        Returns:
            Tracking token
        """
        data = f"{campaign_id}:{user_email}:{time.time()}"
        token = hashlib.sha256(data.encode()).hexdigest()[:32]
        
        return token
    
    def track_click(
        self,
        token: str,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Track a link click.
        
        Args:
            token: Tracking token
            request_data: Request metadata (IP, user agent, etc.)
            
        Returns:
            Click data
        """
        click_data = {
            'token': token,
            'timestamp': datetime.now().isoformat(),
            'ip_address': request_data.get('ip_address'),
            'user_agent': request_data.get('user_agent'),
            'referer': request_data.get('referer'),
            'device_type': self._detect_device_type(request_data.get('user_agent', '')),
            'browser': self._detect_browser(request_data.get('user_agent', ''))
        }
        
        # Store click
        if token not in self.clicks:
            self.clicks[token] = []
        
        self.clicks[token].append(click_data)
        
        logger.info(f"Click tracked: {token}")
        
        return click_data
    
    def track_open(
        self,
        token: str,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Track email open via tracking pixel.
        
        Args:
            token: Tracking token
            request_data: Request metadata
            
        Returns:
            Open data
        """
        open_data = {
            'token': token,
            'timestamp': datetime.now().isoformat(),
            'ip_address': request_data.get('ip_address'),
            'user_agent': request_data.get('user_agent'),
            'device_type': self._detect_device_type(request_data.get('user_agent', ''))
        }
        
        logger.info(f"Email opened: {token}")
        
        return open_data
    
    def track_submission(
        self,
        token: str,
        form_data: Dict[str, Any],
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Track form submission.
        
        Args:
            token: Tracking token
            form_data: Submitted form data
            request_data: Request metadata
            
        Returns:
            Submission data
        """
        submission_data = {
            'token': token,
            'timestamp': datetime.now().isoformat(),
            'ip_address': request_data.get('ip_address'),
            'user_agent': request_data.get('user_agent'),
            'form_fields': list(form_data.keys()),
            'has_credentials': 'password' in form_data or 'username' in form_data
        }
        
        logger.warning(f"Form submitted: {token}")
        
        return submission_data
    
    def get_click_stats(self, token: str) -> Dict[str, Any]:
        """
        Get click statistics for a token.
        
        Args:
            token: Tracking token
            
        Returns:
            Click statistics
        """
        clicks = self.clicks.get(token, [])
        
        if not clicks:
            return {
                'total_clicks': 0,
                'unique_ips': 0,
                'devices': {},
                'browsers': {}
            }
        
        # Calculate statistics
        unique_ips = len(set(c['ip_address'] for c in clicks if c.get('ip_address')))
        
        devices = {}
        browsers = {}
        
        for click in clicks:
            device = click.get('device_type', 'unknown')
            devices[device] = devices.get(device, 0) + 1
            
            browser = click.get('browser', 'unknown')
            browsers[browser] = browsers.get(browser, 0) + 1
        
        return {
            'total_clicks': len(clicks),
            'unique_ips': unique_ips,
            'first_click': clicks[0]['timestamp'],
            'last_click': clicks[-1]['timestamp'],
            'devices': devices,
            'browsers': browsers
        }
    
    def _detect_device_type(self, user_agent: str) -> str:
        """Detect device type from user agent."""
        user_agent_lower = user_agent.lower()
        
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            return 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'tablet'
        else:
            return 'desktop'
    
    def _detect_browser(self, user_agent: str) -> str:
        """Detect browser from user agent."""
        user_agent_lower = user_agent.lower()
        
        if 'chrome' in user_agent_lower:
            return 'chrome'
        elif 'firefox' in user_agent_lower:
            return 'firefox'
        elif 'safari' in user_agent_lower:
            return 'safari'
        elif 'edge' in user_agent_lower:
            return 'edge'
        else:
            return 'other'
