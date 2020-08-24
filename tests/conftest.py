"""
Test configuration and fixtures.
"""

import flask
import pytest

from application import create_app


@pytest.fixture
def app():
    """
    Create the app fixture
    :return:
    """
    from application.database import db
    app = create_app({"TESTING": True,
                      "SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:',
                      'SECRET_KEY': 's3cr3t!',
                      'SQLALCHEMY_ECHO': False,
                      'HTI_ALLOWED_PORTALS': 'https://localhost:8080',
                      'SQLALCHEMY_TRACK_MODIFICATIONS': False})
    with app.app_context():
        db.create_all()
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self):
        with self._client.session_transaction() as sess:
            sess['task'] = {
                "resourceType": "Task",
                "id": "8c83a9ae",
                "definitionReference": {
                    "reference": "ActivityDefinition/2"
                },
                "status": "requested",
                "intent": "plan",
                "for": {
                    "reference": "Person/fa1636df"
                }
            }

    def logout(self):
        flask.session['task'] = None


@pytest.fixture
def auth(client):
    return AuthActions(client)
