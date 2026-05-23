"""Test custom validation error handling with TestClient."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_USER = {
    "username": "alice",
    "age": 25,
    "email": "alice@example.com",
    "password": "secret123",
}


def assert_validation_error(response, expected_fields: set[str]) -> None:
    assert response.status_code == 422, response.text
    data = response.json()
    assert data["error_code"] == "validation_error"
    assert data["status_code"] == 422
    assert data["message"] == "Request validation failed"
    assert "details" in data and len(data["details"]) > 0
    fields = {item["field"] for item in data["details"]}
    assert expected_fields <= fields, f"expected {expected_fields}, got {fields}"
    print(f"OK  422 fields={fields} sample={data['details'][0]}")


def main() -> None:
    ok = client.post("/users/register", json=VALID_USER)
    assert ok.status_code == 201, ok.text
    print(f"OK  valid user: {ok.status_code} {ok.json()}")

    # age <= 18
    bad_age = {**VALID_USER, "age": 16}
    assert_validation_error(
        client.post("/users/register", json=bad_age),
        {"age"},
    )

    # invalid email
    bad_email = {**VALID_USER, "email": "not-an-email"}
    assert_validation_error(
        client.post("/users/register", json=bad_email),
        {"email"},
    )

    # password too short
    bad_password = {**VALID_USER, "password": "short"}
    assert_validation_error(
        client.post("/users/register", json=bad_password),
        {"password"},
    )

    # missing required field
    missing = {k: v for k, v in VALID_USER.items() if k != "username"}
    resp = client.post("/users/register", json=missing)
    assert_validation_error(resp, {"username"})

    print("All validation checks passed.")


if __name__ == "__main__":
    main()
