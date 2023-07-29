import unittest

from fastapi import testclient

from app import db, models
from app.main import app

client = testclient.TestClient(app)


class TestCommentAdd(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)
        session = db.SessionLocal()
        session.add_all(
            [
                models.Post(title="Test Post 1", content="This is a test post."),
                models.Post(title="Test Post 2", content="This is a test post."),
            ]
        )
        session.commit()
        session.close()
        payload = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = client.post("/api/users/signup", json=payload)
        assert response.status_code == 201
        self.token = response.json()["token"]

    def test_comment_add(self):
        response = client.post(
            "/api/comments/",
            json={
                "post_id": 1,
                "content": "test content",
            },
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "post_id": 1,
            "user_id": 1,
            "content": "test content",
        }

    def test_comment_add_unauthorized(self):
        response = client.post(
            "/api/comments/",
            json={
                "content": "test content",
                "post_id": 1,
            },
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_comment_add_invalid_post_id(self):
        response = client.post(
            "/api/comments/",
            json={
                "content": "test content",
                "post_id": 3,
            },
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Post not found"}
