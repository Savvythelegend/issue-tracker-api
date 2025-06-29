from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

from .blacklist import blacklisted_tokens  # Import this

db = SQLAlchemy()
jwt = JWTManager()
swagger = Swagger()

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ["access", "refresh"]

    db.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    # Register token blacklist callback
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in blacklisted_tokens

    from .routes import bp
    app.register_blueprint(bp)

    return app
