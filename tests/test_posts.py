import unittest

from fastapi import testclient

from app import db
from app.main import app

client = testclient.TestClient(app)


class TestPosts(unittest.TestCase):
    def setUp(self):
        db.Base.metadata.drop_all(bind=db.engine)
        db.Base.metadata.create_all(bind=db.engine)

    def test_posts_add(self):
        payload = {
            "title": "Test Post",
            "content": "This is a test post.",
        }
        response = client.post("/api/posts/add", json=payload)
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "title": "Test Post",
            "content": "This is a test post.",
        }
