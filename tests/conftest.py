import pytest
from faker import Faker
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from app import store, users_store
from app.main import app


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture
def client() -> TestClient:
    store.reset()
    users_store.reset()
    with TestClient(app) as test_client:
        yield test_client
    store.reset()
    users_store.reset()


@pytest.fixture
def sample_record(client: TestClient) -> dict:
    response = client.post(
        "/records/",
        json={"username": "testuser", "email": "test@example.com"},
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
async def async_client() -> AsyncClient:
    users_store.reset()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    users_store.reset()
