import pytest

from telegram_bot import app


@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    yield client


def test_route(client):
    response = client.get('/')
    assert response.status_code == 200

