
def test_get_data(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json == {'hello': 'world'}
