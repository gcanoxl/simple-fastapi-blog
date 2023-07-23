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
        "status": "User Added",
        "data": {
            "id": 1,
            "email": "test@test.com",
            "username": "test",
        },
    }
