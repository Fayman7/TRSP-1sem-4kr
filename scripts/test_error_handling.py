"""Send requests to endpoints that trigger custom exceptions."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def check(name: str, method: str, url: str, expected_status: int, expected_code: str) -> None:
    response = client.request(method, url)
    data = response.json()
    assert response.status_code == expected_status, (
        f"{name}: expected status {expected_status}, got {response.status_code}"
    )
    assert data["status_code"] == expected_status
    assert data["error_code"] == expected_code
    assert "message" in data and data["message"]
    print(f"OK  {name}: {response.status_code} {data}")


def main() -> None:
    check(
        "CustomExceptionB (product not found)",
        "GET",
        "/products/9999",
        404,
        "resource_not_found",
    )
    check(
        "CustomExceptionA (insufficient stock)",
        "GET",
        "/products/1/reserve?quantity=1000",
        400,
        "condition_not_met",
    )
    ok = client.get("/products/1")
    assert ok.status_code == 200
    print(f"OK  success path: {ok.status_code} id={ok.json()['id']}")
    print("All error-handling checks passed.")


if __name__ == "__main__":
    main()
