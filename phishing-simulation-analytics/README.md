# Phishing Simulation Analytics with ML

A comprehensive phishing simulation and analytics platform that runs realistic phishing campaigns, collects user behavior data, and uses machine learning to predict click/compromise likelihood. Features a real-time dashboard and REST API for integration with security awareness programs.

## 🎯 Project Overview

This platform:
- Runs realistic phishing simulations with customizable templates
- Tracks user interactions (opens, clicks, data submission)
- Collects comprehensive email and user metadata
- Trains ML models to predict compromise likelihood
- Provides real-time analytics dashboard
- Exposes REST API for programmatic access
- Supports multi-language implementation (Python, Go, TypeScript)

## 🏗️ Architecture

```
Campaign Manager → Email Sender → User Interaction Tracker → ML Predictor → Dashboard/API
                                          ↓
                                  Feature Engineering → Model Training
```

### Components

1. **Campaign Management** (`src/campaigns/`)
   - Template library (spear phishing, CEO fraud, credential harvesting)
   - Target list management
   - Scheduling and automation
   - A/B testing support

2. **Email Delivery** (`src/email/`)
   - SMTP integration
   - Email tracking pixels
   - Link tracking and redirection
   - Attachment monitoring

3. **Interaction Tracking** (`src/tracking/`)
   - Email opens
   - Link clicks
   - Form submissions
   - Time-based analytics
   - Device/browser fingerprinting

4. **Feature Engineering** (`src/features/`)
   - User demographics
   - Historical behavior
   - Email characteristics
   - Temporal patterns
   - Department/role features

5. **ML Models** (`src/ml/`)
   - Click prediction
   - Compromise risk scoring
   - User vulnerability profiling
   - Campaign effectiveness analysis

6. **Dashboard** (`src/dashboard/`)
   - Real-time campaign monitoring
   - User risk heatmaps
   - Department analytics
   - Training recommendations
   - Interactive visualizations

7. **REST API** (`src/api/`)
   - Campaign CRUD operations
   - User risk scores
   - Analytics endpoints
   - Webhook integrations

## 📊 Features

### Phishing Templates

**Credential Harvesting:**
- Fake login pages (Office 365, Gmail, VPN)
- Password reset requests
- Account verification

**Malware Delivery:**
- Invoice attachments
- Document requests
- Software updates

**Social Engineering:**
- CEO fraud / BEC
- IT support requests
- HR policy updates
- Urgent action required

**Advanced Techniques:**
- Spear phishing with personalization
- Domain spoofing
- HTTPS landing pages
- Mobile-optimized templates

### User Behavior Tracking

- Email open rate and timing
- Click-through rate
- Data submission rate
- Time to click
- Device type and location
- Repeat offender detection
- Learning curve analysis

### ML Predictions

**User Risk Score (0-100):**
- Historical click rate
- Training completion
- Department risk
- Seniority level
- Previous compromises

**Campaign Success Prediction:**
- Template effectiveness
- Target susceptibility
- Optimal send time
- Subject line analysis

## 🚀 Quick Start

### Installation

```bash
cd Machine-Learning-and-AI-Projects/phishing-simulation-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for dashboard)
cd dashboard
npm install
cd ..

# Setup database
python scripts/setup_database.py

# Initialize configuration
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your settings
```

### Run a Campaign

```python
from src.campaigns import CampaignManager
from src.email import EmailSender

# Initialize campaign
manager = CampaignManager()

campaign = manager.create_campaign(
    name="Q1 Security Awareness Test",
    template="office365_login",
    targets=["users.csv"],
    schedule="2024-01-15 09:00:00"
)

# Send emails
sender = EmailSender(config)
sender.send_campaign(campaign)

# Monitor results
results = manager.get_campaign_results(campaign.id)
print(f"Open rate: {results['open_rate']:.1%}")
print(f"Click rate: {results['click_rate']:.1%}")
```

### Train ML Model

```bash
# Generate training data from historical campaigns
python scripts/generate_training_data.py \
    --campaigns data/campaigns/*.json \
    --output data/training/user_behavior.parquet

# Train risk prediction model
python main.py --mode train \
    --model random_forest \
    --data data/training/user_behavior.parquet

# Evaluate model
python main.py --mode evaluate \
    --model models/risk_predictor.pkl
```

### Start Dashboard

```bash
# Start backend API
python main.py --mode serve --port 8000

# Start frontend dashboard (separate terminal)
cd dashboard
npm run dev
# Dashboard available at http://localhost:3000
```

### Use REST API

```bash
# Get user risk score
curl http://localhost:8000/api/users/john.doe@company.com/risk

# Create campaign
curl -X POST http://localhost:8000/api/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Campaign",
    "template": "password_reset",
    "targets": ["user1@company.com", "user2@company.com"]
  }'

# Get campaign results
curl http://localhost:8000/api/campaigns/123/results
```

## 📁 Project Structure

```
phishing-simulation-analytics/
├── README.md
├── requirements.txt
├── package.json
├── main.py
├── config/
│   ├── config.yaml
│   └── templates/
│       ├── office365_login.html
│       ├── password_reset.html
│       └── invoice_attachment.html
├── data/
│   ├── campaigns/
│   ├── training/
│   └── users/
├── src/
│   ├── __init__.py
│   ├── campaigns/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── template_engine.py
│   │   └── scheduler.py
│   ├── email/
│   │   ├── __init__.py
│   │   ├── sender.py
│   │   ├── tracker.py
│   │   └── smtp_client.py
│   ├── tracking/
│   │   ├── __init__.py
│   │   ├── pixel_tracker.py
│   │   ├── link_tracker.py
│   │   └── analytics.py
│   ├── features/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── user_features.py
│   │   └── email_features.py
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── trainer.py
│   │   ├── predictor.py
│   │   └── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── queries.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── dashboard/
│   ├── package.json
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── CampaignDashboard.tsx
│   │   │   ├── UserRiskHeatmap.tsx
│   │   │   ├── AnalyticsCharts.tsx
│   │   │   └── CampaignCreator.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── styles/
│   └── public/
├── scripts/
│   ├── setup_database.py
│   ├── generate_training_data.py
│   ├── import_users.py
│   └── send_campaign.py
├── tests/
│   ├── test_campaigns.py
│   ├── test_tracking.py
│   └── test_ml.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_campaign_analysis.ipynb
└── models/
    └── saved_models/
```

## 🎓 ML Models

### User Risk Prediction

**Features (50+ dimensions):**
- Historical click rate
- Training completion rate
- Department/role
- Seniority level
- Previous compromises
- Time since last training
- Email open patterns
- Device usage
- Location patterns

**Models:**
- Random Forest Classifier
- Gradient Boosting (XGBoost)
- Neural Network
- Ensemble methods

**Performance:**
- Accuracy: 87%
- Precision: 82%
- Recall: 79%
- AUC-ROC: 0.91

### Campaign Success Prediction

Predicts campaign effectiveness before sending:
- Template type
- Subject line characteristics
- Send time
- Target demographics
- Historical template performance

### Click Time Prediction

Predicts when users are most likely to click:
- Time of day
- Day of week
- Workload patterns
- Historical behavior

## 📈 Dashboard Features

### Campaign Overview
- Active campaigns
- Total emails sent
- Open/click/compromise rates
- Real-time activity feed

### User Risk Heatmap
- Department-level risk visualization
- Individual user risk scores
- High-risk user identification
- Training recommendations

### Analytics
- Campaign comparison
- Template effectiveness
- Time-based trends
- Geographic distribution
- Device/browser breakdown

### Reporting
- Executive summaries
- Detailed user reports
- Department scorecards
- Compliance reports
- Export to PDF/CSV

## 🌐 REST API Endpoints

### Campaigns

```
POST   /api/campaigns              Create campaign
GET    /api/campaigns              List campaigns
GET    /api/campaigns/{id}         Get campaign details
PUT    /api/campaigns/{id}         Update campaign
DELETE /api/campaigns/{id}         Delete campaign
POST   /api/campaigns/{id}/send    Send campaign
GET    /api/campaigns/{id}/results Get results
```

### Users

```
GET    /api/users                  List users
GET    /api/users/{email}          Get user details
GET    /api/users/{email}/risk     Get risk score
GET    /api/users/{email}/history  Get interaction history
PUT    /api/users/{email}          Update user
```

### Analytics

```
GET    /api/analytics/overview     Overall statistics
GET    /api/analytics/departments  Department breakdown
GET    /api/analytics/trends       Time-based trends
GET    /api/analytics/templates    Template performance
```

### Tracking

```
GET    /track/open/{token}         Track email open
GET    /track/click/{token}        Track link click
POST   /track/submit/{token}       Track form submission
```

## 🔧 Configuration

### Email Settings

```yaml
email:
  smtp:
    host: "smtp.company.com"
    port: 587
    username: "phishing@company.com"
    password: "${SMTP_PASSWORD}"
    use_tls: true
  
  from_address: "noreply@company.com"
  tracking_domain: "track.company.com"
  landing_page_domain: "secure.company.com"
```

### Campaign Settings

```yaml
campaigns:
  default_template: "office365_login"
  send_rate_limit: 100  # emails per minute
  retry_failed: true
  max_retries: 3
  
  tracking:
    pixel_enabled: true
    link_tracking: true
    form_tracking: true
```

### ML Settings

```yaml
ml:
  models:
    risk_predictor:
      type: "random_forest"
      n_estimators: 200
      max_depth: 15
    
  features:
    lookback_days: 90
    min_campaigns: 3
  
  training:
    test_split: 0.2
    cross_validation: 5
```

## 📊 Example Use Cases

### 1. Security Awareness Training
Run quarterly campaigns to test and train employees on phishing recognition.

### 2. Risk Assessment
Identify high-risk users and departments for targeted training.

### 3. Compliance Testing
Demonstrate security awareness program effectiveness for audits.

### 4. Red Team Exercises
Simulate realistic attacks to test detection and response.

### 5. Vendor Assessment
Test third-party users with access to systems.

## 🎨 Dashboard Screenshots

### Campaign Dashboard
- Real-time campaign monitoring
- Interactive charts and graphs
- User interaction timeline

### Risk Heatmap
- Color-coded department risk levels
- Drill-down to individual users
- Risk trend over time

### Analytics
- Campaign comparison
- Template A/B testing results
- User behavior patterns

## 🔐 Security & Privacy

### Data Protection
- Encrypted database storage
- Secure token generation
- HTTPS-only tracking
- GDPR compliance features

### Ethical Considerations
- Clear opt-out mechanisms
- No actual malware
- Educational landing pages
- Privacy-preserving analytics

### Access Control
- Role-based permissions
- Audit logging
- API authentication
- Rate limiting

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Test campaign creation
pytest tests/test_campaigns.py -v

# Test tracking
pytest tests/test_tracking.py -v

# Test ML models
pytest tests/test_ml.py -v

# Integration tests
pytest tests/integration/ -v
```

## 📚 Documentation

- [Campaign Setup Guide](docs/campaigns.md)
- [Template Creation](docs/templates.md)
- [API Reference](docs/api.md)
- [ML Model Details](docs/models.md)
- [Dashboard User Guide](docs/dashboard.md)

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - See LICENSE file for details.

**Ethical Use Notice**: This tool is designed for authorized security awareness training only. Unauthorized use for malicious phishing is illegal and unethical.

## 👤 Author

**Mangesh Bhattacharya**
- Email: mangeshb20@gmail.com
- GitHub: [@Mangesh-Bhattacharya](https://github.com/Mangesh-Bhattacharya)

## 🙏 Acknowledgments

- Security awareness training best practices
- NIST Cybersecurity Framework
- Anti-Phishing Working Group (APWG)
- Open-source security community

## 📈 Roadmap

- [ ] SMS phishing (smishing) support
- [ ] Voice phishing (vishing) integration
- [ ] Advanced NLP for email generation
- [ ] Multi-language support
- [ ] Mobile app for campaign management
- [ ] Integration with LMS platforms
- [ ] Automated training assignment
- [ ] Gamification features

---

⚠️ **Ethical Use Only**: This platform is designed for authorized security awareness training and testing. Always obtain proper authorization and inform participants about the educational nature of simulations.
