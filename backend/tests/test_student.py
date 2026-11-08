import mongomock
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.routes import student_routes


@pytest.fixture
def client(monkeypatch):
    mock_db = mongomock.MongoClient()
    test_collection = mock_db["skillsync_test"]["users"]

    monkeypatch.setattr(
        student_routes,
        "users_collection",
        test_collection
    )

    return TestClient(app)


def test_create_student(client):
    response = client.post(
        "/api/students/",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3,
            "bio": "Software developer"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Student"


def test_get_student(client):
    created = client.post(
        "/api/students/",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3
        }
    )

    student_id = created.json()["id"]

    response = client.get(f"/api/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["id"] == student_id


def test_update_student(client):
    created = client.post(
        "/api/students/",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3
        }
    )

    student_id = created.json()["id"]

    response = client.put(
        f"/api/students/{student_id}",
        json={"name": "Updated Student"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated Student"


def test_delete_student(client):
    created = client.post(
        "/api/students/",
        json={
            "name": "Test Student",
            "email": "test@example.com",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3
        }
    )

    student_id = created.json()["id"]

    response = client.delete(f"/api/students/{student_id}")

    assert response.status_code == 200

    response = client.get(f"/api/students/{student_id}")

    assert response.status_code == 404


def test_invalid_student_data(client):
    response = client.post(
        "/api/students/",
        json={
            "name": "A",
            "email": "invalid-email",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3
        }
    )

    assert response.status_code == 422