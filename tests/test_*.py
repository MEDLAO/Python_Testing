
from server import clubs, competitions


def test_index_should_status_code_ok(client):
    response = client.get('/')
    assert response.status_code == 200


def test_showSummary_should_status_code_ok(client):
    email = 'john@simplylift.co'
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200


def test_showSummary_should_return_422_with_wrong_email(client):
    email = 'test@site.com'
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 422
    assert "Unknown email" == response.data.decode()


def test_showSummary_should_return_422_without_email(client):
    email = ''
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 422


def test_book_should_status_code_ok(client):
    club = clubs[0]['name']
    competition = competitions[0]['name']
    response = client.get(f'/book/{competition}/{club}')
    assert response.status_code == 200


def test_purchasePlaces_should_booked_places_less_than_allowed_points(client):
    club = clubs[0]['name']
    competition = competitions[0]['name']
    places = 10
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert int(clubs[0]['points']) >= 0
    assert "Great-booking complete!" in response.data.decode()


def test_purchasePlaces_not_enough_points(client):
    club = clubs[0]['name']
    competition = competitions[0]['name']
    places = 14
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert "You do not have enough points" in response.data.decode()


def test_purchasePlaces_book_less_than_12_places(client):
    club = clubs[0]['name']
    competition = competitions[0]['name']
    places = 12
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode()


def test_purchasePlaces_cannot_book_more_than_12_places(client):
    club = clubs[0]['name']
    competition = competitions[0]['name']
    places = 13
    response = client.post('/purchasePlaces', data={'club': club, 'competition': competition, 'places': places})
    assert response.status_code == 200
    assert "You cannot book more than 12 places per competition" in response.data.decode()


def test_booking_places_past_competitions(client):
    club = clubs[0]['name']
    competition = competitions[0]['name']
    date = competitions[0]['date']
    response = client.post(f'/book/{competition}/{club}', data={'club': club, 'competition': competition})
