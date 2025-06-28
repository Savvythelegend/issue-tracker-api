from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flasgger import Swagger
import os

db = SQLAlchemy()
load_dotenv()
swagger = Swagger()
def create_app():
    # This code initializes a Flask application, sets up SQLAlchemy for database interactions,
    # and loads environment variables from a .env file. The application is configured to use a database URL
    # specified in the environment variable `DATABASE_URL`, with a fallback to a default SQLite database.
    # It also registers a blueprint for routing, allowing for modular organization of routes within the application.

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    swagger.init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app
