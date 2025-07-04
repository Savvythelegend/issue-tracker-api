import pytest

from app import create_app
from app.extensions import db


# creating a flask app for testing config:
@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


# This fixture sets up the Flask application for testing, creating a new database for each test run.


@pytest.fixture
def client(app):
    return app.test_client()
