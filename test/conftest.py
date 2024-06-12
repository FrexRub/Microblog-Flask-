import pytest

from src.main import app as _app


@pytest.fixture(scope="session")
def app():
    app = _app
    app.set_config()
    app.config["TESTING"] = True

    yield app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
