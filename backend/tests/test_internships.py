
import mongomock
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.routes import internship_routes
from app.routes import auth_routes
from app.services.auth_service import create_access_token


@pytest.fixture
def client(monkeypatch):
    test_db = mongomock.MongoClient()["internship_test"]

    test_collection = test_db["internships"]
    test_admins = test_db["admins"]

    monkeypatch.setattr(
        internship_routes,
        "internships_collection",
        test_collection
    )

    monkeypatch.setattr(
        auth_routes,
        "admins_collection",
        test_admins
    )

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-testing-only"
    )

    admin_result = test_admins.insert_one({
        "name": "Test Admin",
        "email": "admin@test.com",
        "role": "admin"
    })

    token = create_access_token(str(admin_result.inserted_id))

    test_client = TestClient(app)

    test_client.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return test_client


def sample_internship():
    return {
        "title": "Python Developer Intern",
        "company": "Tech Solutions",
        "description": "Work on real-world Python projects.",
        "location": "Bengaluru",
        "skills_required": ["Python", "FastAPI"],
        "duration": "3 months",
        "stipend": 15000,
        "application_deadline": "2026-12-15",
        "status": "Active"
    }


# 1. Test creating an internship
def test_create_internship(client):
    response = client.post(
        "/api/internships/",
        json=sample_internship()
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Python Developer Intern"
    assert response.json()["company"] == "Tech Solutions"


# 2. Test viewing all internships
def test_get_internships(client):
    client.post("/api/internships/", json=sample_internship())

    response = client.get("/api/internships/")

    assert response.status_code == 200
    assert len(response.json()) == 1


# 3. Test searching internships
def test_search_internships(client):
    client.post("/api/internships/", json=sample_internship())

    response = client.get(
        "/api/internships/",
        params={"search": "Python"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# 4. Test filtering by location
def test_filter_by_location(client):
    client.post("/api/internships/", json=sample_internship())

    response = client.get(
        "/api/internships/",
        params={"location": "Bengaluru"}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# 5. Test viewing internship details
def test_get_internship_details(client):
    create_response = client.post(
        "/api/internships/",
        json=sample_internship()
    )

    internship_id = create_response.json()["id"]

    response = client.get(
        f"/api/internships/{internship_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == internship_id


# 6. Test updating an internship
def test_update_internship(client):
    create_response = client.post(
        "/api/internships/",
        json=sample_internship()
    )

    internship_id = create_response.json()["id"]

    response = client.put(
        f"/api/internships/{internship_id}",
        json={"stipend": 20000}
    )

    assert response.status_code == 200
    assert response.json()["stipend"] == 20000


# 7. Test deleting an internship
def test_delete_internship(client):
    create_response = client.post(
        "/api/internships/",
        json=sample_internship()
    )

    internship_id = create_response.json()["id"]

    response = client.delete(
        f"/api/internships/{internship_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Internship deleted successfully"


# 8. Test invalid internship ID
def test_invalid_internship_id(client):
    response = client.get("/api/internships/invalid-id")

    assert response.status_code == 400
