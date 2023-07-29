import unittest

from fastapi import testclient

from app import db, models
from app.main import app
from tests.test_posts import update_admin

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


class TestCommentGet(unittest.TestCase):
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
        session.add_all(
            [
                models.Comment(content="Test Comment 1", post_id=1, user_id=1),
                models.Comment(content="Test Comment 2", post_id=1, user_id=1),
                models.Comment(content="Test Comment 3", post_id=2, user_id=1),
            ]
        )
        session.commit()
        session.close()

    def test_comment_get_all(self):
        response = client.get("/api/comments/1")
        assert response.status_code == 200
        assert response.json() == {
            "count": 2,
            "comments": [
                {
                    "id": 1,
                    "content": "Test Comment 1",
                    "post_id": 1,
                    "user_id": 1,
                },
                {
                    "id": 2,
                    "content": "Test Comment 2",
                    "post_id": 1,
                    "user_id": 1,
                },
            ],
        }

    def test_comment_get_all_2(self):
        response = client.get("/api/comments/2")
        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "comments": [
                {
                    "id": 3,
                    "content": "Test Comment 3",
                    "post_id": 2,
                    "user_id": 1,
                },
            ],
        }


class TestCommentUpdate(unittest.TestCase):
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
        session.add_all(
            [
                models.Comment(content="Test Comment 1", post_id=1, user_id=1),
                models.Comment(content="Test Comment 2", post_id=1, user_id=2),
                models.Comment(content="Test Comment 3", post_id=2, user_id=2),
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

    def test_comment_update(self):
        response = client.put(
            "/api/comments/1",
            json={
                "content": "updated content",
            },
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "content": "updated content",
            "post_id": 1,
            "user_id": 1,
        }

    def test_comment_update_unauthorized(self):
        response = client.put(
            "/api/comments/1",
            json={
                "content": "updated content",
            },
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}

    def test_comment_update_by_wrong_user(self):
        response = client.put(
            "/api/comments/2",
            json={
                "content": "updated content",
            },
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert response.status_code == 403
        assert response.json() == {"detail": "User is not comment owner"}

    def test_comment_update_by_admin(self):
        update_admin()
        response = client.put(
            "/api/comments/2",
            json={
                "content": "updated content",
            },
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 2,
            "content": "updated content",
            "post_id": 1,
            "user_id": 2,
        }
