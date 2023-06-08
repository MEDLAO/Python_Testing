
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
