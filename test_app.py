import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_get(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_dashboard_redirect(client):
    rv = client.get('/dashboard')
    assert rv.status_code == 302  # Should redirect to login

def test_resource_usage(client):
    rv = client.get('/resource_usage')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'cpu' in json_data
    assert 'memory' in json_data
    assert 'disk' in json_data
    assert 'network' in json_data