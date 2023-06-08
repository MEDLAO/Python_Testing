

def test_book_should_status_code_ok(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[0]['name']
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200


def test_purchasePlaces_should_booked_places_less_than_allowed_points(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[0]['name']
    places = 10
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert int(mock_clubs[0]['points']) >= 0
    assert "Great-booking complete!" in response.data.decode()


def test_purchasePlaces_not_enough_points(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[0]['name']
    places = 41
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert "You do not have enough points" in response.data.decode()
