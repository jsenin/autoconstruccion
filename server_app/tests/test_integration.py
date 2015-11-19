import pytest
from autoconstruccion import create_app, db


# define app fixture for pytest-flask
@pytest.fixture()
def app():
    # for now we test over sqlite in memory, so no empty db needed
    test_app = create_app('TESTING_MEMORY')
    db.init_app(test_app)
    with test_app.test_request_context():
        db.create_all()
    return test_app


def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_projects_page_loads(client):
    response = client.get('/projects')
    assert response.status_code == 200


def test_users_page_loads(client):
    response = client.get('/users')
    assert response.status_code == 200

