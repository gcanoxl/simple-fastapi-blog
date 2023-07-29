from fastapi.testclient import TestClient

from app import db, models
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

    def test_user_signup_invalid_is_admin(self):
        payload = {
            "username": "test",
            "password": "test123",
            "is_admin": True,
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert response.json()["username"] == "test"
        assert "password" not in response.json()
        assert "token" in response.json()
        assert response.json()["is_admin"] == False


class TestUserLogin(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)
        session = db.SessionLocal()
        session.add(models.User(username="test", password="test123"))
        session.commit()
        session.close()

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
