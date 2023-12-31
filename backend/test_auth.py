# tests/test_auth.py
from fastapi.testclient import TestClient
from backend.main import app  # Update this line to use an absolute import 


client = TestClient(app)

def test_register():
    response = client.post("/auth/register/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login():
    response = client.post("/auth/login/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
