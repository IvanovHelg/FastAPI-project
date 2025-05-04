import random
import string
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def random_username():
    return "user_" + "".join(random.choices(string.ascii_lowercase, k=8))


@pytest.fixture
def user_data():
    return {
        "username": random_username(),
        "password": "testpassword"
    }


@pytest.fixture
def auth_headers(user_data):
    client.post("/register", json=user_data)
    response = client.post("/token", data=user_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
