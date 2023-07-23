from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_user_signup():
    payload = {
        "email": "test@test.com",
        "username": "test",
        "password": "test123",
    }
    response = client.post("/api/users/signup", json=payload)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "email": "test@test.com",
        "username": "test",
    }


def test_user_signup_existing_email():
    payload = {
        "email": "test@test.com",
        "username": "test2",
        "password": "test456",
    }
    response = client.post("/api/users/signup", json=payload)
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}
