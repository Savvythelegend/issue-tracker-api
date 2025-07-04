# app/__init__.py
import os
from flask import Flask
from .extensions import db, jwt, migrate, swagger
from .models import BlackListTokens
from .routes import bp

# Only load dotenv in development
if os.getenv('FLASK_CONFIG', 'development') == 'development':
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # dotenv not available, skip loading
        pass

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Determine config name
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")
    
    # Map config names to classes
    config_mapping = {
        'development': 'DevelopmentConfig',
        'production': 'ProductionConfig',
        'testing': 'TestingConfig'
    }
    
    config_class = config_mapping.get(config_name.lower(), 'DevelopmentConfig')
    
    try:
        app.config.from_object(f"app.core.config.{config_class}")
        
        # Initialize ProductionConfig if needed (for validation)
        if config_name.lower() == 'production':
            from app.core.config import ProductionConfig
            ProductionConfig()  # This will validate required env vars
            
    except (ImportError, ValueError) as e:
        print(f"Config error: {e}")
        # Don't fall back in production - fail fast
        if config_name.lower() == 'production':
            raise
        else:
            app.config.from_object("app.core.config.DevelopmentConfig")
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)
    migrate.init_app(app, db)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return BlackListTokens.query.filter_by(jti=jti).first() is not None
    
    app.register_blueprint(bp)
    
    return app