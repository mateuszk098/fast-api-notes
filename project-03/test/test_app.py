from fastapi.testclient import TestClient
from starlette import status

from app import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}
