"""Async tests for in-memory /users API (pytest-asyncio + httpx + Faker)."""

import pytest
from faker import Faker
from httpx import AsyncClient


def user_payload(faker: Faker, *, age: int | None = None) -> dict:
    return {
        "username": faker.user_name(),
        "age": age if age is not None else faker.random_int(min=18, max=80),
    }


class TestUsersAsync:
    @pytest.mark.asyncio
    async def test_create_user_returns_201_and_valid_body(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        payload = user_payload(faker, age=25)
        response = await async_client.post("/users", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert set(data.keys()) == {"id", "username", "age"}
        assert data["username"] == payload["username"]
        assert data["age"] == payload["age"]
        assert isinstance(data["id"], int)
        assert data["id"] >= 1

    @pytest.mark.asyncio
    async def test_create_user_with_boundary_ages(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        for age in (0, 150):
            payload = user_payload(faker, age=age)
            response = await async_client.post("/users", json=payload)
            assert response.status_code == 201
            assert response.json()["age"] == age

    @pytest.mark.asyncio
    async def test_create_user_invalid_age_returns_422(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        payload = user_payload(faker, age=151)
        response = await async_client.post("/users", json=payload)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_get_existing_user_returns_200(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        created = await async_client.post("/users", json=user_payload(faker))
        user_id = created.json()["id"]

        response = await async_client.get(f"/users/{user_id}")

        assert response.status_code == 200
        assert response.json() == created.json()

    @pytest.mark.asyncio
    async def test_get_nonexistent_user_returns_404(
        self, async_client: AsyncClient
    ) -> None:
        response = await async_client.get("/users/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    @pytest.mark.asyncio
    async def test_delete_existing_user_returns_204(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        created = await async_client.post("/users", json=user_payload(faker))
        user_id = created.json()["id"]

        response = await async_client.delete(f"/users/{user_id}")

        assert response.status_code == 204
        assert response.content == b""

    @pytest.mark.asyncio
    async def test_delete_same_user_twice_second_returns_404(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        created = await async_client.post("/users", json=user_payload(faker))
        user_id = created.json()["id"]

        first = await async_client.delete(f"/users/{user_id}")
        second = await async_client.delete(f"/users/{user_id}")

        assert first.status_code == 204
        assert second.status_code == 404
        assert second.json()["detail"] == "User not found"

    @pytest.mark.asyncio
    async def test_get_after_delete_returns_404(
        self, async_client: AsyncClient, faker: Faker
    ) -> None:
        created = await async_client.post("/users", json=user_payload(faker))
        user_id = created.json()["id"]
        await async_client.delete(f"/users/{user_id}")

        response = await async_client.get(f"/users/{user_id}")
        assert response.status_code == 404
