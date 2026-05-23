"""Pytest module tests for in-memory /records API."""

import pytest
from fastapi.testclient import TestClient


class TestRegisterRecord:
    """POST /records/ — create (register) a record."""

    def test_register_success(self, client: TestClient) -> None:
        response = client.post(
            "/records/",
            json={"username": "alice", "email": "alice@example.com"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["username"] == "alice"
        assert data["email"] == "alice@example.com"

    def test_register_multiple_increments_id(self, client: TestClient) -> None:
        first = client.post(
            "/records/",
            json={"username": "a", "email": "a@example.com"},
        )
        second = client.post(
            "/records/",
            json={"username": "b", "email": "b@example.com"},
        )
        assert first.status_code == 201
        assert second.status_code == 201
        assert first.json()["id"] == 1
        assert second.json()["id"] == 2

    def test_register_invalid_email_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/records/",
            json={"username": "bob", "email": "not-email"},
        )
        assert response.status_code == 422
        body = response.json()
        assert body["error_code"] == "validation_error"
        assert any(d["field"] == "email" for d in body["details"])

    def test_register_missing_username_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/records/",
            json={"email": "only@example.com"},
        )
        assert response.status_code == 422

    def test_register_empty_username_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/records/",
            json={"username": "", "email": "x@example.com"},
        )
        assert response.status_code == 422


class TestGetRecord:
    """GET /records/{record_id} — retrieve a record."""

    def test_get_existing_record(self, client: TestClient, sample_record: dict) -> None:
        record_id = sample_record["id"]
        response = client.get(f"/records/{record_id}")
        assert response.status_code == 200
        assert response.json() == sample_record

    def test_get_not_found(self, client: TestClient) -> None:
        response = client.get("/records/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Record 999 not found"

    def test_get_invalid_id_type(self, client: TestClient) -> None:
        response = client.get("/records/abc")
        assert response.status_code == 422


class TestDeleteRecord:
    """DELETE /records/{record_id} — remove a record."""

    def test_delete_existing_record(self, client: TestClient, sample_record: dict) -> None:
        record_id = sample_record["id"]
        response = client.delete(f"/records/{record_id}")
        assert response.status_code == 200
        assert response.json() == {"deleted": True, "id": record_id}

    def test_delete_not_found(self, client: TestClient) -> None:
        response = client.delete("/records/42")
        assert response.status_code == 404
        assert response.json()["detail"] == "Record 42 not found"

    def test_get_after_delete_returns_404(
        self, client: TestClient, sample_record: dict
    ) -> None:
        record_id = sample_record["id"]
        assert client.delete(f"/records/{record_id}").status_code == 200
        assert client.get(f"/records/{record_id}").status_code == 404

    def test_delete_twice_second_is_404(
        self, client: TestClient, sample_record: dict
    ) -> None:
        record_id = sample_record["id"]
        assert client.delete(f"/records/{record_id}").status_code == 200
        assert client.delete(f"/records/{record_id}").status_code == 404


class TestRecordsWorkflow:
    """End-to-end scenarios across all three endpoints."""

    def test_full_crud_flow(self, client: TestClient) -> None:
        created = client.post(
            "/records/",
            json={"username": "workflow", "email": "flow@example.com"},
        ).json()

        fetched = client.get(f"/records/{created['id']}")
        assert fetched.status_code == 200
        assert fetched.json()["username"] == "workflow"

        deleted = client.delete(f"/records/{created['id']}")
        assert deleted.status_code == 200

        assert client.get(f"/records/{created['id']}").status_code == 404
