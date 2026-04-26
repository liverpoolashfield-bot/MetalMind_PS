# MetalMind PS - Web Subscription Portal

## Architecture
- **Backend**: Flask (Python) with Flask-SQLAlchemy, Flask-Login
- **Frontend**: Flask templates + Bootstrap 5 (server-side rendering for simplicity)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Modular**: Flask Blueprints for each feature

## Project Structure
```
metalmind_ps/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py           # Configuration
│   ├── models.py           # Database models
│   ├── extensions.py      # Flask extensions
│   │
│   ├── modules/            # Modular blueprints
│   │   ├── auth/           # Login/registration
│   │   ├── members/        # Membership management
│   │   ├── billing/        # Payment gateway
│   │   └── subscriptions/ # Subscription plans
│   │
│   ├── static/            # CSS, JS, images
│   └── templates/         # HTML templates
│
├── requirements.txt
└── run.py
```

## Core Features
1. **Authentication**: User login, registration, logout, password reset
2. **Membership**: User profiles, membership tiers, access control
3. **Billing**: Stripe integration, invoice tracking, payment history
4. **Subscriptions**: Plan management, upgrade/downgrade, renewal

## To Extend
Add new modules under `app/modules/` - each with own:
- `routes.py` - endpoints
- `forms.py` - WTForms
- `templates/` - module-specific templates

## Run
```bash
pip install -r requirements.txt
python run.py
```