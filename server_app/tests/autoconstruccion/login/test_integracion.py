
def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_logout_page_loads(client):
    response = client.get('/logout')
    assert response.status_code in [401, 200]


def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200


