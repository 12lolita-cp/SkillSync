
import mongomock
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.routes import application_routes, auth_routes
from app.services.auth_service import create_access_token


@pytest.fixture
def client(monkeypatch):

    test_db = mongomock.MongoClient()["application_test"]

    test_applications = test_db["applications"]
    test_users = test_db["users"]
    test_internships = test_db["internships"]
    test_admins = test_db["admins"]

    monkeypatch.setattr(
        application_routes,
        "applications_collection",
        test_applications
    )

    monkeypatch.setattr(
        application_routes,
        "users_collection",
        test_users
    )

    monkeypatch.setattr(
        application_routes,
        "internships_collection",
        test_internships
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

    student_result = test_users.insert_one({
        "name": "Test Student",
        "email": "student@test.com",
        "college": "Test College",
        "department": "Computer Science",
        "year": 2
    })

    internship_result = test_internships.insert_one({
        "title": "Python Developer Intern",
        "company": "Tech Solutions",
        "description": "Work on Python projects.",
        "location": "Bengaluru",
        "skills_required": ["Python"],
        "duration": "3 months",
        "stipend": 15000,
        "application_deadline": "2099-12-31",
        "status": "Active"
    })

    return {
        "client": test_client,
        "student_id": str(student_result.inserted_id),
        "internship_id": str(internship_result.inserted_id)
    }


# 1. Test submitting an application
def test_create_application(client):

    response = client["client"].post(
        "/api/applications/",
        json={
            "student_id": client["student_id"],
            "internship_id": client["internship_id"],
            "cover_letter": "I am interested in this internship."
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "Applied"


# 2. Test preventing duplicate applications
def test_duplicate_application(client):

    data = {
        "student_id": client["student_id"],
        "internship_id": client["internship_id"]
    }

    client["client"].post("/api/applications/", json=data)

    response = client["client"].post(
        "/api/applications/",
        json=data
    )

    assert response.status_code == 409


# 3. Test viewing a student's applications
def test_get_student_applications(client):

    client["client"].post(
        "/api/applications/",
        json={
            "student_id": client["student_id"],
            "internship_id": client["internship_id"]
        }
    )

    response = client["client"].get(
        f"/api/applications/student/{client['student_id']}"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# 4. Test admin viewing all applications
def test_get_all_applications(client):

    client["client"].post(
        "/api/applications/",
        json={
            "student_id": client["student_id"],
            "internship_id": client["internship_id"]
        }
    )

    response = client["client"].get("/api/applications/")

    assert response.status_code == 200
    assert len(response.json()) == 1


# 5. Test admin updating application status
def test_update_application_status(client):

    create_response = client["client"].post(
        "/api/applications/",
        json={
            "student_id": client["student_id"],
            "internship_id": client["internship_id"]
        }
    )

    application_id = create_response.json()["id"]

    response = client["client"].put(
        f"/api/applications/{application_id}/status",
        json={"status": "Shortlisted"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Shortlisted"


# 6. Test invalid application ID
def test_invalid_application_id(client):

    response = client["client"].put(
        "/api/applications/invalid-id/status",
        json={"status": "Selected"}
    )

    assert response.status_code == 400


# 7. Test invalid application status
def test_invalid_application_status(client):

    create_response = client["client"].post(
        "/api/applications/",
        json={
            "student_id": client["student_id"],
            "internship_id": client["internship_id"]
        }
    )

    application_id = create_response.json()["id"]

    response = client["client"].put(
        f"/api/applications/{application_id}/status",
        json={"status": "Pending"}
    )

    assert response.status_code == 422
