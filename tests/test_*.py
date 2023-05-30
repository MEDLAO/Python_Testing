import json

from server import clubs, competitions, purchasePlaces


def test_purchasePlaces_book_less_than_12_places(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[0]['name']
    places = 12
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()


def test_purchasePlaces_cannot_book_more_than_12_places(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[0]['name']
    places = 13
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert "You cannot book more than 12 places per competition" in response.data.decode()
