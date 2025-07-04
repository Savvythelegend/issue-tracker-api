# app/__init__.py

import os

from dotenv import load_dotenv
from flask import Flask

from .extensions import db, jwt, migrate, swagger
from .models import BlackListTokens
from .routes import bp

load_dotenv()


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development").capitalize() + "Config"
    else:
        config_name = config_name.capitalize() + "Config"
    app.config.from_object(f"app.core.config.{config_name}")

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
