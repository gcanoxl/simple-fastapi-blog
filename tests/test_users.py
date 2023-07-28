from fastapi.testclient import TestClient

from app import db
from app.main import app

client = TestClient(app)

import unittest


class TestUserSignUp(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)

    def test_user_signup(self):
        payload = {
            "username": "test",
            "password": "test123",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["username"] == "test"
        assert "password" not in response.json()
        assert "token" in response.json()

    def test_user_signup_existing_username(self):
        payload = {
            "username": "test1",
            "password": "test123",
        }
        response = client.post("/api/users/signup", json=payload)
        payload = {
            "username": "test1",
            "password": "test456",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 409
        assert response.json() == {"detail": "Username already exists"}


class TestUserLogin(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)
        payload = {
            "username": "test",
            "password": "test123",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 201

    def test_user_login(self):
        payload = {
            "username": "test",
            "password": "test123",
        }
        response = client.post("/api/users/login", json=payload)
        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["username"] == "test"
        assert "token" in response.json()

    def test_user_login_user_not_found(self):
        payload = {
            "username": "test1",
            "password": "test123",
        }
        response = client.post("/api/users/login", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}

    def test_user_login_wrong_password(self):
        payload = {
            "username": "test",
            "password": "test456",
        }
        response = client.post("/api/users/login", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect username or password"}
