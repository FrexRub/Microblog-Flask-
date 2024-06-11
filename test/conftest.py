import pytest

from src.app import app as _app


@pytest.fixture()
def app():
    app = _app
    app.set_config()
    app.config["TESTING"] = True
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

