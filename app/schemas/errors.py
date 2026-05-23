from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Consistent error payload for all custom exception handlers."""

    error_code: str = Field(..., examples=["resource_not_found"])
    message: str = Field(..., examples=["Product with id=99 was not found"])
    status_code: int = Field(..., examples=[404])
