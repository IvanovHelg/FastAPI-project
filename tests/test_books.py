import random
import string
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def random_title(prefix="Book"):
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase, k=6))}"


@pytest.fixture
def book_data(auth_headers):
    # Сначала создаём автора
    author = {"name": f"Author_{random.randint(1000, 9999)}"}
    response = client.post("/authors/", json=author, headers=auth_headers)
    author_id = response.json()["id"]

    return {
        "title": random_title(),
        "author_id": author_id
    }


def test_create_book(book_data, auth_headers):
    response = client.post("/books/", json=book_data, headers=auth_headers)
    assert response.status_code == 200, f"Unexpected: {response.text}"
    assert response.json()["title"] == book_data["title"]


def test_list_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
