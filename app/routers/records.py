from fastapi import APIRouter, HTTPException

from app import store
from app.schemas.record import RecordCreate, RecordResponse

router = APIRouter(prefix="/records", tags=["records"])


@router.post("/", response_model=RecordResponse, status_code=201)
def register_record(payload: RecordCreate) -> RecordResponse:
    """Register (create) a record in in-memory storage."""
    record = store.create(username=payload.username, email=str(payload.email))
    return RecordResponse(**record)


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(record_id: int) -> RecordResponse:
    """Retrieve a record by id."""
    record = store.get(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return RecordResponse(**record)


@router.delete("/{record_id}")
def delete_record(record_id: int) -> dict:
    """Delete a record by id."""
    if not store.delete(record_id):
        raise HTTPException(status_code=404, detail=f"Record {record_id} not found")
    return {"deleted": True, "id": record_id}
