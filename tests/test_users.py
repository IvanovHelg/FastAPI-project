import random
import string

import pytest
from fastapi.testclient import TestClient

from app.main import app  # Убедись, что у тебя есть app/main.py с FastAPI(app)
from app.database import Base, engine, SessionLocal

# Создаем таблицы в тестовой базе данных
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def random_username(prefix="testuser", length=6):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}_{suffix}"


@pytest.fixture
def user_data():
    return {
        "username": random_username(),
        "password": "testpassword"
    }


def test_register_user(user_data):
    response = client.post("/register", json=user_data)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, response: {response.text}"
    assert "username" in response.json()
    assert response.json()["username"] == user_data["username"]


def test_login_user(user_data):
    # Сначала регистрируем пользователя
    client.post("/register", json=user_data)

    # Теперь логинимся
    response = client.post("/token", data=user_data)
    assert response.status_code == 200, f"Login failed: {response.status_code}, response: {response.text}"
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"


def test_access_protected_endpoint(user_data):
    # Регистрируем и логинимся
    client.post("/register", json=user_data)
    login_response = client.post("/token", data=user_data)
    token = login_response.json()["access_token"]

    # Доступ к защищенному эндпоинту (например, /users/me или /books)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/books", headers=headers)
    assert response.status_code == 200, f"Failed access: {response.status_code}, response: {response.text}"


def test_get_books():
    # Публичный эндпоинт (если он открыт)
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
