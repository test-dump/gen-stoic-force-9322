import pytest
from flask_jwt_extended import create_access_token

from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

def test_user_register(client):
    response = client.post('/api/user/register', json={
        'username': 'testuser', 'password': 'password'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['username'] == 'testuser'

def test_user_login(client):
    user = User(username='testuser', password=User.encrypt_password('password'))
    db.session.add(user)
    db.session.commit()

    response = client.post('/api/user/login', json={
        'username': 'testuser', 'password': 'password'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data
