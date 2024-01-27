# tests/conftest.py
import sys
from os.path import dirname, abspath
import pytest

sys.path.append(dirname(dirname(abspath(__file__))))
from app.create_app import create_app, db, ConfigTesting


@pytest.fixture
def app():
    app = create_app(config_class=ConfigTesting)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
