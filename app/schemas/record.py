from pydantic import BaseModel, EmailStr, Field


class RecordCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr


class RecordResponse(BaseModel):
    id: int
    username: str
    email: str
