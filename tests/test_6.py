
def test_points_display_board(client):
    response = client.get('/pointsDisplayBoard')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT points board!' in response.data.decode()
