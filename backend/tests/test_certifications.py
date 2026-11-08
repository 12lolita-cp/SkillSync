import mongomock
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.routes import student_routes, certification_routes


@pytest.fixture
def client(monkeypatch):
    mock_db = mongomock.MongoClient()["skillsync_test"]

    users = mock_db["users"]
    certifications = mock_db["certifications"]

    monkeypatch.setattr(
        student_routes, "users_collection", users
    )

    monkeypatch.setattr(
        certification_routes, "users_collection", users
    )

    monkeypatch.setattr(
        certification_routes,
        "certifications_collection",
        certifications
    )

    return TestClient(app)


def create_student(client):
    response = client.post(
        "/api/students/",
        json={
            "name": "Test Student",
            "email": "cert@example.com",
            "college": "NIE Mysuru",
            "department": "Computer Science",
            "year": 3
        }
    )

    assert response.status_code == 201
    return response.json()["id"]


def test_add_certification(client):
    student_id = create_student(client)

    response = client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Python Certification",
            "issuing_organization": "Coursera",
            "issue_date": "2026-01-15",
            "expiry_date": "2027-01-15",
            "credential_id": "PY12345",
            "credential_url": "https://example.com/certificate"
        }
    )

    assert response.status_code == 201
    assert response.json()["certification_name"] == "Python Certification"
    assert response.json()["status"] == "Active"


def test_get_certifications(client):
    student_id = create_student(client)

    client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Java Certification",
            "issuing_organization": "Oracle",
            "issue_date": "2026-02-01"
        }
    )

    response = client.get(
        f"/api/students/{student_id}/certifications/"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_certification(client):
    student_id = create_student(client)

    created = client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Python Certification",
            "issuing_organization": "Coursera",
            "issue_date": "2026-01-15"
        }
    )

    certification_id = created.json()["id"]

    response = client.put(
        f"/api/students/{student_id}/certifications/{certification_id}",
        json={
            "issuing_organization": "Updated Organization"
        }
    )

    assert response.status_code == 200
    assert response.json()["issuing_organization"] == "Updated Organization"


def test_delete_certification(client):
    student_id = create_student(client)

    created = client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Java Certification",
            "issuing_organization": "Oracle",
            "issue_date": "2026-02-01"
        }
    )

    certification_id = created.json()["id"]

    response = client.delete(
        f"/api/students/{student_id}/certifications/{certification_id}"
    )

    assert response.status_code == 200

    response = client.get(
        f"/api/students/{student_id}/certifications/"
    )

    assert response.json() == []


def test_invalid_date_range(client):
    student_id = create_student(client)

    response = client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Python Certification",
            "issuing_organization": "Coursera",
            "issue_date": "2026-05-01",
            "expiry_date": "2026-01-01"
        }
    )

    assert response.status_code == 400


def test_expired_certification(client):
    student_id = create_student(client)

    response = client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Old Certification",
            "issuing_organization": "Test Organization",
            "issue_date": "2024-01-01",
            "expiry_date": "2025-01-01"
        }
    )

    assert response.status_code == 201
    assert response.json()["status"] == "Expired"


def test_invalid_certificate_url(client):
    student_id = create_student(client)

    response = client.post(
        f"/api/students/{student_id}/certifications/",
        json={
            "certification_name": "Python Certification",
            "issuing_organization": "Coursera",
            "issue_date": "2026-01-15",
            "credential_url": "not-a-valid-url"
        }
    )

    assert response.status_code == 422