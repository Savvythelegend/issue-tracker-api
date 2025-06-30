# app/__init__.py

from flask import Flask
from dotenv import load_dotenv
from .extensions import db, jwt, swagger, migrate
from .routes import bp
from .models import BlackListTokens
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    config_name = os.getenv("FLASK_CONFIG", "development").capitalize() + "Config"
    app.config.from_object(f"app.config.{config_name}")

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
