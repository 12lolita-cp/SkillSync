
import mongomock
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routes import auth_routes
from app.services.auth_service import create_access_token


@pytest.fixture
def client(monkeypatch):
    test_db = mongomock.MongoClient()["auth_test"]
    test_admins = test_db["admins"]

    monkeypatch.setattr(
        auth_routes,
        "admins_collection",
        test_admins
    )

    monkeypatch.setenv("ADMIN_SETUP_KEY", "test-setup-key")
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-secret-key-for-testing-only"
    )

    return TestClient(app)


def test_admin_registration(client):
    response = client.post(
        "/api/auth/admin/register",
        headers={"X-Admin-Setup-Key": "test-setup-key"},
        json={
            "name": "Test Admin",
            "email": "admin@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Admin registered successfully"


def test_admin_login(client):
    client.post(
        "/api/auth/admin/register",
        headers={"X-Admin-Setup-Key": "test-setup-key"},
        json={
            "name": "Test Admin",
            "email": "admin@test.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/admin/login",
        json={
            "email": "admin@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_admin_login_wrong_password(client):
    client.post(
        "/api/auth/admin/register",
        headers={"X-Admin-Setup-Key": "test-setup-key"},
        json={
            "name": "Test Admin",
            "email": "admin@test.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/admin/login",
        json={
            "email": "admin@test.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_admin_registration_wrong_setup_key(client):
    response = client.post(
        "/api/auth/admin/register",
        headers={"X-Admin-Setup-Key": "wrong-key"},
        json={
            "name": "Test Admin",
            "email": "admin@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 403


def test_admin_login_unknown_email(client):
    response = client.post(
        "/api/auth/admin/login",
        json={
            "email": "unknown@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 401


def test_second_admin_registration_blocked(client):
    client.post(
        "/api/auth/admin/register",
        headers={"X-Admin-Setup-Key": "test-setup-key"},
        json={
            "name": "First Admin",
            "email": "first@test.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/admin/register",
        headers={"X-Admin-Setup-Key": "test-setup-key"},
        json={
            "name": "Second Admin",
            "email": "second@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin registration is already completed"


def test_create_internship_without_token(client):
    test_client = TestClient(app)

    response = test_client.post(
        "/api/internships/",
        json={
            "title": "Python Developer Intern",
            "company": "ABC Technologies",
            "description": "Work on Python backend development projects.",
            "location": "Bengaluru",
            "skills_required": ["Python", "FastAPI"],
            "duration": "3 months",
            "stipend": 10000,
            "application_deadline": "2026-12-31",
            "status": "Active"
        }
    )

    assert response.status_code == 401


def test_create_internship_with_invalid_token(client):
    test_client = TestClient(app)
    test_client.headers.update({
        "Authorization": "Bearer invalid-token"
    })

    response = test_client.post(
        "/api/internships/",
        json={
            "title": "Python Developer Intern",
            "company": "ABC Technologies",
            "description": "Work on Python backend development projects.",
            "location": "Bengaluru",
            "skills_required": ["Python", "FastAPI"],
            "duration": "3 months",
            "stipend": 10000,
            "application_deadline": "2026-12-31",
            "status": "Active"
        }
    )

    assert response.status_code == 401
