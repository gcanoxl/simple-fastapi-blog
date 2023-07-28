from fastapi.testclient import TestClient

from app import db
from app.main import app

client = TestClient(app)

import unittest


class TestUser(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)

    def test_user_signup(self):
        payload = {
            "email": "test@test.com",
            "username": "test",
            "password": "test123",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["email"] == "test@test.com"
        assert response.json()["username"] == "test"
        assert "password" not in response.json()

    def test_user_signup_existing_email(self):
        payload = {
            "email": "test@test.com",
            "username": "test1",
            "password": "test123",
        }
        response = client.post("/api/users/signup", json=payload)
        payload = {
            "email": "test@test.com",
            "username": "test2",
            "password": "test456",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 409
        assert response.json() == {"detail": "Email already exists"}
