import unittest

from fastapi import testclient

from app import db, models
from app.main import app

client = testclient.TestClient(app)


class TestPosts(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)
        payload = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 201
        self.token = response.json()["token"]

    def test_posts_add_without_token(self):
        payload = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        response = client.post("/api/posts/", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_posts_add_with_user(self):
        payload = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        response = client.post(
            "/api/posts/",
            json=payload,
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "Not authorized"}

    def test_posts_add_with_admin(self):
        session = db.SessionLocal()
        session.query(models.User).filter(models.User.username == "testuser").update(
            {"is_admin": True}
        )
        session.commit()
        payload = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        response = client.post(
            "/api/posts/",
            json=payload,
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "title": "Test Post",
            "content": "This is a test post.",
            "views": 0,
        }
        session.close()
