import unittest

from fastapi import testclient

from app import db
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

    def test_posts_add_with_unauthorized(self):
        payload = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        response = client.post("/api/posts/", json=payload)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_posts_add_with_admin(self):
        payload = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        response = client.post(
            "/api/posts/",
            json=payload,
            headers={"X-Token": self.token},
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "title": "Test Post",
            "content": "This is a test post.",
            "views": 0,
        }
