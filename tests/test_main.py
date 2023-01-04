from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_index():
    response = client.get("api/ping/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello you are home"}

def test_get_ping():
    response = client.get("api/ping/")
    assert response.status_code == 200
    data = response.json()
    assert data.message == "Hello! pong"