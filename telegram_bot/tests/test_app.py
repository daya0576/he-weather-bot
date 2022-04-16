import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv(".env_test")


@pytest.fixture
def client():
    from telegram_bot import app
    # app.app.config['TESTING'] = True
    client = TestClient(app.app)
    return client


def test_route(client):
    response = client.get("/")
    assert response.status_code == 200
