# app/core/config.py
import os
from datetime import timedelta

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///default.db")

class ProductionConfig(BaseConfig):
    DEBUG = False
    # Render provides DATABASE_URL automatically
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    
    # Ensure required environment variables are set
    def __init__(self):
        if not os.getenv("DATABASE_URL"):
            raise ValueError("DATABASE_URL environment variable is required for production")
        if os.getenv("JWT_SECRET_KEY") == "changeme-in-production":
            raise ValueError("JWT_SECRET_KEY must be changed from default value")

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///test.db")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3)
    JWT_BLACKLIST_ENABLED = False  # Disable blacklist in tests