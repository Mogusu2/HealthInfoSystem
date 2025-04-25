from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_client():
    response = client.post("/clients/", json={
        "name": "Test User",
        "age": 28,
        "contact": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"

def test_create_program():
    response = client.post("/programs/", json={
        "name": "Malaria",
        "description": "Malaria prevention and treatment"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Malaria"

def test_search_client():
    response = client.get("/clients/search?q=Test")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_enroll_client():
    # assuming client with id 1 and program id 1 exists
    response = client.post("/enrollments/", json={
        "client_id": 1,
        "program_ids": [1]
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Client enrolled successfully"

def test_public_profile():
    response = client.get("/public/client/1")
    assert response.status_code == 200
    assert "programs" in response.json()
