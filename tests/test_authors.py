import random
import string
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def random_name(prefix="Author"):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase, k=6))}"


@pytest.fixture
def author_data():
    return {
        "name": random_name()
    }


@pytest.fixture
def auth_headers(user_data):
    # Регистрация и авторизация
    client.post("/register", json=user_data)
    response = client.post("/token", data=user_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_author(author_data, auth_headers):
    response = client.post("/authors/", json=author_data, headers=auth_headers)
    assert response.status_code == 200, f"Unexpected: {response.text}"
    assert "name" in response.json()
    assert response.json()["name"] == author_data["name"]


def test_list_authors(auth_headers):
    response = client.get("/authors/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
