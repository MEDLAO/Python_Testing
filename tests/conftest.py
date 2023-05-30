import pytest

import server
from server import app


"""@pytest.fixture
def client():
    with app.test_client() as client:
        yield client"""


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client


@pytest.fixture
def mock_clubs(mocker):
    clubs = [
        {
            "name": "Test Club 1",
            "email": "club1@test.com",
            "points": "40"
        },
        {
            "name": "Test Club 2",
            "email": "club2@test.com",
            "points": "25"
        },
        {
            "name": "Test Club 3",
            "email": "club3@test.com",
            "points": "2"
        },
    ]
    mocked = mocker.patch.object(server, 'clubs', clubs)
    yield mocked


@pytest.fixture
def mock_competitions(mocker):
    competitions = [
        {
            "name": "Test Competition 1",
            "date": "2024-06-07 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Test Competition 2",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Test Competition 3",
            "date": "2022-06-09 10:00:00",
            "numberOfPlaces": "5"
        },
        {
            "name": "Test Competition 4",
            "date": "2020-06-09 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    mocked = mocker.patch.object(server, 'competitions', competitions)
    yield mocked
