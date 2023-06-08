import json

from server import loadClubs, loadCompetitions
from unittest import mock


@mock.patch('server.COMPETITIONS_FILE', 'tests/competitions_test.json')
@mock.patch('server.CLUBS_FILE', 'tests/clubs_test.json')
def test_update_points(client):
    competitions = loadCompetitions()
    clubs = loadClubs()
    competition = competitions[0]['name']
    club = clubs[0]['name']
    places = 1
    places_available = competitions[0]['numberOfPlaces']
    points_club = clubs[0]['points']
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})

    a_file = open("tests/competitions_test.json", "r")
    json_object_comp = json.load(a_file)
    a_file.close()

    b_file = open("tests/clubs_test.json", "r")
    json_object_club = json.load(b_file)
    b_file.close()

    assert response.status_code == 200
    assert json_object_comp['competitions'][0]['numberOfPlaces'] == str(int(places_available) - places)
    assert json_object_club['clubs'][0]['points'] == str(int(points_club) - places)
