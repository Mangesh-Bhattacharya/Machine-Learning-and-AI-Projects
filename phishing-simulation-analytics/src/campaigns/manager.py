"""
Campaign Manager

Manages phishing simulation campaigns including creation, scheduling, and tracking.
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import uuid
from datetime import datetime
from pathlib import Path
import json

from .template_engine import TemplateEngine
from .scheduler import CampaignScheduler


class Campaign:
    """Represents a phishing simulation campaign."""
    
    def __init__(
        self,
        name: str,
        template: str,
        targets: List[str],
        schedule: Optional[str] = None,
        campaign_id: Optional[str] = None
    ):
        """
        Initialize campaign.
        
        Args:
            name: Campaign name
            template: Template identifier
            targets: List of target email addresses
            schedule: Optional schedule time (ISO format)
            campaign_id: Optional campaign ID
        """
        self.id = campaign_id or str(uuid.uuid4())
        self.name = name
        self.template = template
        self.targets = targets
        self.schedule = schedule
        self.created_at = datetime.now()
        self.status = "scheduled" if schedule else "draft"
        
        # Tracking data
        self.sent_count = 0
        self.opened_count = 0
        self.clicked_count = 0
        self.submitted_count = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert campaign to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'template': self.template,
            'targets': self.targets,
            'schedule': self.schedule,
            'created_at': self.created_at.isoformat(),
            'status': self.status,
            'stats': {
                'sent': self.sent_count,
                'opened': self.opened_count,
                'clicked': self.clicked_count,
                'submitted': self.submitted_count
            }
        }


class CampaignManager:
    """Manages phishing simulation campaigns."""
    
    def __init__(self, config: Dict = None):
        """
        Initialize campaign manager.
        
        Args:
            config: Campaign configuration
        """
        self.config = config or {}
        self.campaigns = {}
        
        # Initialize components
        self.template_engine = TemplateEngine(
            templates_dir=self.config.get('templates_dir', 'config/templates')
        )
        
        self.scheduler = CampaignScheduler(
            config=self.config.get('scheduler', {})
        )
        
        # Load existing campaigns
        self._load_campaigns()
        
    def create_campaign(
        self,
        name: str,
        template: str,
        targets: List[str],
        schedule: Optional[str] = None,
        **kwargs
    ) -> Campaign:
        """
        Create a new campaign.
        
        Args:
            name: Campaign name
            template: Template identifier
            targets: List of target email addresses
            schedule: Optional schedule time
            **kwargs: Additional campaign parameters
            
        Returns:
            Created campaign
        """
        logger.info(f"Creating campaign: {name}")
        
        # Validate template
        if not self.template_engine.template_exists(template):
            raise ValueError(f"Template not found: {template}")
        
        # Validate targets
        if not targets:
            raise ValueError("No targets specified")
        
        # Create campaign
        campaign = Campaign(
            name=name,
            template=template,
            targets=targets,
            schedule=schedule
        )
        
        # Store campaign
        self.campaigns[campaign.id] = campaign
        self._save_campaign(campaign)
        
        # Schedule if needed
        if schedule:
            self.scheduler.schedule_campaign(campaign)
        
        logger.success(f"Campaign created: {campaign.id}")
        
        return campaign
    
    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        """
        Get campaign by ID.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Campaign or None
        """
        return self.campaigns.get(campaign_id)
    
    def list_campaigns(
        self,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Campaign]:
        """
        List campaigns.
        
        Args:
            status: Filter by status
            limit: Maximum number of campaigns
            
        Returns:
            List of campaigns
        """
        campaigns = list(self.campaigns.values())
        
        # Filter by status
        if status:
            campaigns = [c for c in campaigns if c.status == status]
        
        # Sort by created date (newest first)
        campaigns.sort(key=lambda c: c.created_at, reverse=True)
        
        return campaigns[:limit]
    
    def update_campaign(
        self,
        campaign_id: str,
        **updates
    ) -> Campaign:
        """
        Update campaign.
        
        Args:
            campaign_id: Campaign ID
            **updates: Fields to update
            
        Returns:
            Updated campaign
        """
        campaign = self.get_campaign(campaign_id)
        
        if not campaign:
            raise ValueError(f"Campaign not found: {campaign_id}")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        
        # Save changes
        self._save_campaign(campaign)
        
        logger.info(f"Campaign updated: {campaign_id}")
        
        return campaign
    
    def delete_campaign(self, campaign_id: str) -> bool:
        """
        Delete campaign.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            True if deleted
        """
        if campaign_id in self.campaigns:
            del self.campaigns[campaign_id]
            
            # Delete from storage
            campaign_file = self._get_campaign_file(campaign_id)
            if campaign_file.exists():
                campaign_file.unlink()
            
            logger.info(f"Campaign deleted: {campaign_id}")
            return True
        
        return False
    
    def get_campaign_results(self, campaign_id: str) -> Dict[str, Any]:
        """
        Get campaign results and statistics.
        
        Args:
            campaign_id: Campaign ID
            
        Returns:
            Results dictionary
        """
        campaign = self.get_campaign(campaign_id)
        
        if not campaign:
            raise ValueError(f"Campaign not found: {campaign_id}")
        
        # Calculate rates
        total_sent = campaign.sent_count
        
        if total_sent == 0:
            return {
                'campaign_id': campaign_id,
                'campaign_name': campaign.name,
                'total_sent': 0,
                'opened': 0,
                'clicked': 0,
                'submitted': 0,
                'open_rate': 0.0,
                'click_rate': 0.0,
                'submit_rate': 0.0
            }
        
        results = {
            'campaign_id': campaign_id,
            'campaign_name': campaign.name,
            'template': campaign.template,
            'created_at': campaign.created_at.isoformat(),
            'status': campaign.status,
            'total_sent': total_sent,
            'opened': campaign.opened_count,
            'clicked': campaign.clicked_count,
            'submitted': campaign.submitted_count,
            'open_rate': campaign.opened_count / total_sent,
            'click_rate': campaign.clicked_count / total_sent,
            'submit_rate': campaign.submitted_count / total_sent,
            'avg_time_to_click': self._calculate_avg_time_to_click(campaign_id)
        }
        
        return results
    
    def _calculate_avg_time_to_click(self, campaign_id: str) -> float:
        """Calculate average time to click for campaign."""
        # This would query the tracking database
        # Placeholder implementation
        return 0.0
    
    def _load_campaigns(self):
        """Load campaigns from storage."""
        campaigns_dir = Path('data/campaigns')
        
        if not campaigns_dir.exists():
            return
        
        for campaign_file in campaigns_dir.glob('*.json'):
            try:
                with open(campaign_file, 'r') as f:
                    data = json.load(f)
                
                campaign = Campaign(
                    name=data['name'],
                    template=data['template'],
                    targets=data['targets'],
                    schedule=data.get('schedule'),
                    campaign_id=data['id']
                )
                
                campaign.status = data.get('status', 'draft')
                campaign.sent_count = data.get('stats', {}).get('sent', 0)
                campaign.opened_count = data.get('stats', {}).get('opened', 0)
                campaign.clicked_count = data.get('stats', {}).get('clicked', 0)
                campaign.submitted_count = data.get('stats', {}).get('submitted', 0)
                
                self.campaigns[campaign.id] = campaign
                
            except Exception as e:
                logger.error(f"Failed to load campaign {campaign_file}: {e}")
    
    def _save_campaign(self, campaign: Campaign):
        """Save campaign to storage."""
        campaigns_dir = Path('data/campaigns')
        campaigns_dir.mkdir(parents=True, exist_ok=True)
        
        campaign_file = campaigns_dir / f"{campaign.id}.json"
        
        with open(campaign_file, 'w') as f:
            json.dump(campaign.to_dict(), f, indent=2)
    
    def _get_campaign_file(self, campaign_id: str) -> Path:
        """Get campaign file path."""
        return Path('data/campaigns') / f"{campaign_id}.json"
