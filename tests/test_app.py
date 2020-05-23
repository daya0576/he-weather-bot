import pytest

from telegram_bot import telegram_bot


@pytest.fixture
def client():
    telegram_bot.app.config['TESTING'] = True
    client = telegram_bot.app.test_client()
    yield client


def test_route(client):
    response = client.get('/')
    assert response.status_code == 200
