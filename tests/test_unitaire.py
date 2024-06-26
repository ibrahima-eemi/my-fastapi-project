import pytest
from fastapi.testclient import TestClient
from my_fastapi_project.main import app

client = TestClient(app)

def test_create_student():
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    assert response.status_code == 200
    token = response.json().get("access_token")

    response = client.post(
        "/student",
        headers={"Authorization": f"Bearer {token}"},
        json={"first_name": "Jane", "last_name": "Doe", "email": "janedoe@example.com", "grades": []}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), str)

def test_create_student_duplicate_email():
    response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    assert response.status_code == 200
    token = response.json().get("access_token")

    client.post(
        "/student",
        headers={"Authorization": f"Bearer {token}"},
        json={"first_name": "Jane", "last_name": "Doe", "email": "janedoe@example.com", "grades": []}
    )
    response = client.post(
        "/student",
        headers={"Authorization": f"Bearer {token}"},
        json={"first_name": "John", "last_name": "Smith", "email": "janedoe@example.com", "grades": []}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"].startswith("Value error, Email must be unique")
