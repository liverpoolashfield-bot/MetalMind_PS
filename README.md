# MetalMind PS - Web Subscription Portal

A modular Flask-based subscription portal with authentication, membership management, and billing.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Open http://localhost:5000 in your browser.

## Configuration

Copy `.env.example` to `.env` and configure:
- `SECRET_KEY` - Flask secret key
- `STRIPE_*` - Stripe API keys (get from https://dashboard.stripe.com)

## Features

- **Authentication**: Login, registration, password management
- **Membership**: Multiple membership tiers (Basic, Premium, Pro)
- **Subscriptions**: Monthly/yearly plans with Stripe integration
- **Billing**: Payment history, invoices, Stripe Checkout

## Adding New Modules

```bash
# Create new module
mkdir app/modules/newmodule
```

Create in `app/modules/newmodule/`:
- `__init__.py` - `from app.modules.newmodule.routes import newmodule_bp`
- `routes.py` - Blueprint with routes
- `forms.py` - WTForms
- `templates/` - HTML templates

Register in `app/__init__.py`:
```python
from app.modules.newmodule import newmodule_bp
app.register_blueprint(newmodule_bp, url_prefix='/newmodule')
```

## Tech Stack

- Flask 3.0
- Flask-SQLAlchemy
- Flask-Login
- Stripe API
- Bootstrap 5