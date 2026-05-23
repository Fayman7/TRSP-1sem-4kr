from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=150)


class UserOut(BaseModel):
    id: int
    username: str
    age: int
