import mongomock
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.routes import student_routes, skill_routes


@pytest.fixture
def client(monkeypatch):
    mock_db = mongomock.MongoClient()["skillsync_test"]

    users = mock_db["users"]
    skills = mock_db["skills"]

    monkeypatch.setattr(
        student_routes,
        "users_collection",
        users
    )

    monkeypatch.setattr(
        skill_routes,
        "users_collection",
        users
    )

    monkeypatch.setattr(
        skill_routes,
        "skills_collection",
        skills
    )

    return TestClient(app)


def create_test_student(client):
    response = client.post(
        "/api/students/",
        json={
            "name": "Test Student",
            "email": "student@example.com",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3
        }
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_add_skill(client):
    student_id = create_test_student(client)

    response = client.post(
        f"/api/students/{student_id}/skills/",
        json={
            "skill_name": "Python",
            "category": "Programming",
            "proficiency": "Intermediate",
            "progress": 60
        }
    )

    assert response.status_code == 201
    assert response.json()["skill_name"] == "Python"


def test_get_student_skills(client):
    student_id = create_test_student(client)

    client.post(
        f"/api/students/{student_id}/skills/",
        json={
            "skill_name": "Java",
            "category": "Programming",
            "proficiency": "Beginner",
            "progress": 30
        }
    )

    response = client.get(
        f"/api/students/{student_id}/skills/"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_skill(client):
    student_id = create_test_student(client)

    created = client.post(
        f"/api/students/{student_id}/skills/",
        json={
            "skill_name": "Python",
            "category": "Programming",
            "proficiency": "Beginner",
            "progress": 20
        }
    )

    skill_id = created.json()["id"]

    response = client.put(
        f"/api/students/{student_id}/skills/{skill_id}",
        json={
            "proficiency": "Advanced",
            "progress": 80
        }
    )

    assert response.status_code == 200
    assert response.json()["proficiency"] == "Advanced"
    assert response.json()["progress"] == 80


def test_delete_skill(client):
    student_id = create_test_student(client)

    created = client.post(
        f"/api/students/{student_id}/skills/",
        json={
            "skill_name": "C++",
            "category": "Programming",
            "proficiency": "Intermediate",
            "progress": 50
        }
    )

    skill_id = created.json()["id"]

    response = client.delete(
        f"/api/students/{student_id}/skills/{skill_id}"
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/students/{student_id}/skills/"
    )

    assert response.json() == []


def test_skill_progress_summary(client):
    student_id = create_test_student(client)

    for name, progress in [
        ("Python", 60),
        ("Java", 80)
    ]:
        client.post(
            f"/api/students/{student_id}/skills/",
            json={
                "skill_name": name,
                "category": "Programming",
                "proficiency": "Intermediate",
                "progress": progress
            }
        )

    response = client.get(
        f"/api/students/{student_id}/skills/progress/summary"
    )

    assert response.status_code == 200
    assert response.json()["total_skills"] == 2
    assert response.json()["average_progress"] == 70


def test_invalid_skill_data(client):
    student_id = create_test_student(client)

    response = client.post(
        f"/api/students/{student_id}/skills/",
        json={
            "skill_name": "Python",
            "category": "Programming",
            "proficiency": "Master",
            "progress": 150
        }
    )

    assert response.status_code == 422