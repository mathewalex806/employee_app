from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint_is_public():
    response = client.get("api/v1/health")
    assert response.status_code == 200
    assert response.json()["message"] == "Server is healthy" 