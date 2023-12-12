import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app as flask_app, db

@pytest.fixture(scope='module')
def test_client():
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    testing_client = flask_app.test_client()
    with flask_app.app_context():
        db.create_all()

    yield testing_client
    # Teardown
    with flask_app.app_context():
        db.session.remove()
        db.drop_all()