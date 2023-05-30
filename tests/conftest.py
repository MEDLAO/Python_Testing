import pytest

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


"""@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client"""
