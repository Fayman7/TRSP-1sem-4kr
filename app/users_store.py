"""Thread-safe in-memory user storage (dict) for /users API."""

from itertools import count
from threading import Lock

_db: dict[int, dict] = {}
_id_seq = count(start=1)
_id_lock = Lock()


def reset() -> None:
    global _db, _id_seq
    with _id_lock:
        _db = {}
        _id_seq = count(start=1)


def next_user_id() -> int:
    with _id_lock:
        return next(_id_seq)


def create(username: str, age: int) -> dict:
    user_id = next_user_id()
    payload = {"username": username, "age": age}
    _db[user_id] = payload
    return {"id": user_id, **payload}


def get(user_id: int) -> dict | None:
    row = _db.get(user_id)
    if row is None:
        return None
    return {"id": user_id, **row}


def delete(user_id: int) -> bool:
    return _db.pop(user_id, None) is not None
