"""In-memory storage for records (used by /records API and tests)."""

_records: dict[int, dict] = {}
_next_id: int = 1


def reset() -> None:
    global _records, _next_id
    _records = {}
    _next_id = 1


def create(username: str, email: str) -> dict:
    global _next_id
    record = {"id": _next_id, "username": username, "email": email}
    _records[_next_id] = record
    _next_id += 1
    return record.copy()


def get(record_id: int) -> dict | None:
    record = _records.get(record_id)
    return record.copy() if record else None


def delete(record_id: int) -> bool:
    if record_id not in _records:
        return False
    del _records[record_id]
    return True


def count() -> int:
    return len(_records)
