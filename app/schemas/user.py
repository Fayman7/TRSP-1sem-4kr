from typing import Annotated, Optional

from pydantic import BaseModel, EmailStr, Field

# Pydantic v2: Field(gt=18) / Field(min_length=..., max_length=...) — аналог conint / constr из задания


class User(BaseModel):
    username: str
    age: Annotated[int, Field(gt=18)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=16)]
    phone: Optional[str] = "Unknown"
