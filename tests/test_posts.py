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
        assert response.json() == {"detail": "User is not admin"}

    def test_posts_add_with_admin(self):
        session = db.SessionLocal()
        session.query(models.User).filter(models.User.username == "testuser").update(
            {"is_admin": True}
        )
        session.commit()
        session.close()
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


class TestPostsGet(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)
        # create 5 posts
        session = db.SessionLocal()
        session.add_all(
            [
                models.Post(title="Test Post 1", content="This is a test post."),
                models.Post(title="Test Post 2", content="This is a test post."),
                models.Post(title="Test Post 3", content="This is a test post."),
                models.Post(title="Test Post 4", content="This is a test post."),
                models.Post(title="Test Post 5", content="This is a test post."),
            ]
        )
        session.commit()
        session.close()

    def test_posts_get_number(self):
        response = client.get("/api/posts/")
        assert response.status_code == 200
        assert response.json() == {
            "count": 5,
        }

    def test_posts_get_one(self):
        response = client.get("/api/posts/2")
        assert response.status_code == 200
        assert response.json() == {
            "id": 2,
            "title": "Test Post 2",
            "content": "This is a test post.",
            "views": 0,
        }

    def test_posts_get_unexisting(self):
        response = client.get("/api/posts/6")
        assert response.status_code == 404
        assert response.json() == {"detail": "Post not found"}

    def test_posts_get_unexisting_negative(self):
        response = client.get("/api/posts/-1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Post not found"}

    def test_posts_get_list(self):
        response = client.get("/api/posts/?limit=2")
        assert response.status_code == 200
        assert response.json() == {
            "count": 2,
            "posts": [
                {
                    "id": 1,
                    "title": "Test Post 1",
                    "content": "This is a test post.",
                    "views": 0,
                },
                {
                    "id": 2,
                    "title": "Test Post 2",
                    "content": "This is a test post.",
                    "views": 0,
                },
            ],
        }

    def test_posts_get_list_with_offset(self):
        response = client.get("/api/posts/?limit=2&offset=2")
        assert response.status_code == 200
        assert response.json() == {
            "count": 2,
            "posts": [
                {
                    "id": 3,
                    "title": "Test Post 3",
                    "content": "This is a test post.",
                    "views": 0,
                },
                {
                    "id": 4,
                    "title": "Test Post 4",
                    "content": "This is a test post.",
                    "views": 0,
                },
            ],
        }

    def test_posts_get_list_overflow(self):
        response = client.get("/api/posts/?limit=2&offset=5")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Offset + limit is greater than total number of posts"
        }

    def test_posts_get_list_larger_limit(self):
        response = client.get("/api/posts/?limit=10")
        assert response.status_code == 200
        assert response.json() == {
            "count": 5,
            "posts": [
                {
                    "id": 1,
                    "title": "Test Post 1",
                    "content": "This is a test post.",
                    "views": 0,
                },
                {
                    "id": 2,
                    "title": "Test Post 2",
                    "content": "This is a test post.",
                    "views": 0,
                },
                {
                    "id": 3,
                    "title": "Test Post 3",
                    "content": "This is a test post.",
                    "views": 0,
                },
                {
                    "id": 4,
                    "title": "Test Post 4",
                    "content": "This is a test post.",
                    "views": 0,
                },
                {
                    "id": 5,
                    "title": "Test Post 5",
                    "content": "This is a test post.",
                    "views": 0,
                },
            ],
        }


class TestPostsUpdate(unittest.TestCase):
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

    def test_update_one(self):
        session = db.SessionLocal()
        session.query(models.User).filter(models.User.username == "testuser").update(
            {"is_admin": True}
        )
        session.commit()
        session.close()
        response = client.put(
            "/api/posts/1",
            json={"title": "Updated title", "content": "Updated content"},
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "Updated title",
            "content": "Updated content",
            "views": 0,
        }

    def test_update_unexisting(self):
        # TODO: refactor
        session = db.SessionLocal()
        session.query(models.User).filter(models.User.username == "testuser").update(
            {"is_admin": True}
        )
        session.commit()
        session.close()
        response = client.put(
            "/api/posts/3",
            json={"title": "Updated title", "content": "Updated content"},
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Post not found"}

    def test_update_with_unauthorized_user(self):
        response = client.put(
            "/api/posts/1",
            json={"title": "Updated title", "content": "Updated content"},
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


class TestPostsDelete(unittest.TestCase):
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

    def test_delete_one(self):
        update_admin()
        response = client.delete(
            "/api/posts/1",
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 200
        assert response.json() == {"detail": "Post deleted"}

    def test_delete_unexisting(self):
        update_admin()
        response = client.delete(
            "/api/posts/3",
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Post not found"}

    def test_delete_unauthorized(self):
        response = client.delete(
            "/api/posts/1",
            headers={"Authorization": "Bearer " + self.token},
        )
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def update_admin(username: str = "testuser"):
    session = db.SessionLocal()
    session.query(models.User).filter(models.User.username == "testuser").update(
        {"is_admin": True}
    )
    session.commit()
    session.close()
