import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app


@pytest.fixture
def client() -> TestClient:
    store.reset()
    with TestClient(app) as test_client:
        yield test_client
    store.reset()


@pytest.fixture
def sample_record(client: TestClient) -> dict:
    response = client.post(
        "/records/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    assert response.status_code == 201
    return response.json()
