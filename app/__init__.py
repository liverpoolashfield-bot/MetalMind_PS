from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='default'):
    from app.config import config
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'auth.login'
    
    from app.modules.auth import auth_bp
    from app.modules.members import members_bp
    from app.modules.billing import billing_bp
    from app.modules.subscriptions import subscriptions_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(billing_bp, url_prefix='/billing')
    app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')
    
    @app.route('/')
    def index():
        return redirect(url_for('members.dashboard'))
    
    from app import models
    
    return app