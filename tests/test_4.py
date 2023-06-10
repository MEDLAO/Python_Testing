
def test_booking_places_future_competitions(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[0]['name']
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200
    assert "Places available:" in response.data.decode()


def test_booking_places_past_competitions(client, mock_clubs, mock_competitions):
    club = mock_clubs[0]['name']
    competition = mock_competitions[3]['name']
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 422
    assert "Sorry you cannot book past competitions" in response.data.decode()
