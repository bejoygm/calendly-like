from fastapi.testclient import TestClient

from app.main import app

test_client = TestClient(app=app)


def test_create_user_succeeds():
    payload = {"name": "abc", "email": "abc@examsple.com"}
    response = test_client.post("/users", json=payload)
    assert response.status_code == 201
