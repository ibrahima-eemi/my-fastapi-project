from fastapi.testclient import TestClient
from my_fastapi_project.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Hello <span>World</span></h1>" in response.text

def test_create_student():
    response = client.post("/student", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "grades": []
    })
    assert response.status_code == 200
    assert response.json() is not None
    