"""
Template Engine

Manages email templates for phishing simulations.
"""

from typing import Dict, Any, Optional
from loguru import logger
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import json


class TemplateEngine:
    """Manages phishing email templates."""
    
    def __init__(self, templates_dir: str = "config/templates"):
        """
        Initialize template engine.
        
        Args:
            templates_dir: Directory containing templates
        """
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=True
        )
        
        # Load template metadata
        self.templates = self._load_template_metadata()
        
    def _load_template_metadata(self) -> Dict[str, Dict]:
        """Load template metadata."""
        metadata_file = self.templates_dir / "templates.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        
        # Default templates
        return {
            "office365_login": {
                "name": "Office 365 Login",
                "description": "Fake Office 365 login page",
                "category": "credential_harvesting",
                "difficulty": "medium",
                "subject": "Your Office 365 password will expire today",
                "from_name": "Microsoft Account Team"
            },
            "password_reset": {
                "name": "Password Reset",
                "description": "Urgent password reset request",
                "category": "credential_harvesting",
                "difficulty": "easy",
                "subject": "Reset your password immediately",
                "from_name": "IT Support"
            },
            "invoice_attachment": {
                "name": "Invoice Attachment",
                "description": "Fake invoice with malicious attachment",
                "category": "malware_delivery",
                "difficulty": "medium",
                "subject": "Invoice #{{invoice_number}} - Payment Required",
                "from_name": "Accounts Payable"
            },
            "ceo_fraud": {
                "name": "CEO Fraud",
                "description": "Urgent request from CEO",
                "category": "social_engineering",
                "difficulty": "hard",
                "subject": "URGENT: Wire Transfer Needed",
                "from_name": "{{ceo_name}}"
            },
            "hr_policy": {
                "name": "HR Policy Update",
                "description": "New HR policy requiring action",
                "category": "social_engineering",
                "difficulty": "easy",
                "subject": "Important: New Company Policy - Action Required",
                "from_name": "Human Resources"
            }
        }
    
    def template_exists(self, template_id: str) -> bool:
        """
        Check if template exists.
        
        Args:
            template_id: Template identifier
            
        Returns:
            True if template exists
        """
        return template_id in self.templates
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """
        Get template metadata.
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template metadata or None
        """
        return self.templates.get(template_id)
    
    def list_templates(self, category: Optional[str] = None) -> Dict[str, Dict]:
        """
        List available templates.
        
        Args:
            category: Optional category filter
            
        Returns:
            Dictionary of templates
        """
        if category:
            return {
                tid: tmpl for tid, tmpl in self.templates.items()
                if tmpl.get('category') == category
            }
        
        return self.templates
    
    def render_email(
        self,
        template_id: str,
        user_data: Dict[str, Any],
        tracking_token: str
    ) -> Dict[str, str]:
        """
        Render email from template.
        
        Args:
            template_id: Template identifier
            user_data: User data for personalization
            tracking_token: Tracking token for links
            
        Returns:
            Dictionary with subject, html_body, text_body
        """
        if not self.template_exists(template_id):
            raise ValueError(f"Template not found: {template_id}")
        
        template_meta = self.templates[template_id]
        
        # Prepare template variables
        variables = {
            **user_data,
            'tracking_token': tracking_token,
            'tracking_pixel_url': f"https://track.company.com/pixel/{tracking_token}.png",
            'phishing_link': f"https://secure.company.com/verify/{tracking_token}"
        }
        
        # Render subject
        subject_template = Template(template_meta['subject'])
        subject = subject_template.render(**variables)
        
        # Render HTML body
        try:
            html_template = self.env.get_template(f"{template_id}.html")
            html_body = html_template.render(**variables)
        except Exception as e:
            logger.warning(f"HTML template not found for {template_id}: {e}")
            html_body = self._generate_default_html(template_id, variables)
        
        # Render text body
        try:
            text_template = self.env.get_template(f"{template_id}.txt")
            text_body = text_template.render(**variables)
        except Exception:
            text_body = self._html_to_text(html_body)
        
        return {
            'subject': subject,
            'html_body': html_body,
            'text_body': text_body,
            'from_name': template_meta.get('from_name', 'IT Support')
        }
    
    def _generate_default_html(
        self,
        template_id: str,
        variables: Dict[str, Any]
    ) -> str:
        """Generate default HTML template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Security Alert</title>
        </head>
        <body>
            <p>Dear {variables.get('first_name', 'User')},</p>
            
            <p>This is a phishing simulation test.</p>
            
            <p><a href="{variables['phishing_link']}">Click here to verify your account</a></p>
            
            <p>Best regards,<br>IT Security Team</p>
            
            <img src="{variables['tracking_pixel_url']}" width="1" height="1" alt="" />
        </body>
        </html>
        """
    
    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text."""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text()
    
    def create_template(
        self,
        template_id: str,
        name: str,
        category: str,
        subject: str,
        html_content: str,
        **metadata
    ) -> bool:
        """
        Create a new template.
        
        Args:
            template_id: Template identifier
            name: Template name
            category: Template category
            subject: Email subject
            html_content: HTML content
            **metadata: Additional metadata
            
        Returns:
            True if created successfully
        """
        # Save HTML template
        template_file = self.templates_dir / f"{template_id}.html"
        with open(template_file, 'w') as f:
            f.write(html_content)
        
        # Update metadata
        self.templates[template_id] = {
            'name': name,
            'category': category,
            'subject': subject,
            **metadata
        }
        
        # Save metadata
        metadata_file = self.templates_dir / "templates.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
        
        logger.info(f"Template created: {template_id}")
        
        return True
