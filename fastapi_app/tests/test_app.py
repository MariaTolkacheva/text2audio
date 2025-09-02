from fastapi.testclient import TestClient

from fastapi_app import api

client = TestClient(api)


def test_ping():
    response = client.post("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"
