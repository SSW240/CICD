import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Welcome to the Stock Data App' in rv.data

def test_data(client):
    rv = client.get('/data')
    assert rv.status_code == 200
    assert b'stock_price.png' in rv.data
