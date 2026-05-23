from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Consistent error payload for all custom exception handlers."""

    error_code: str = Field(..., examples=["resource_not_found"])
    message: str = Field(..., examples=["Product with id=99 was not found"])
    status_code: int = Field(..., examples=[404])


class ValidationErrorDetail(BaseModel):
    field: str = Field(..., examples=["age"])
    message: str = Field(..., examples=["Input should be greater than 18"])


class ValidationErrorResponse(BaseModel):
    """Payload for request body / query validation failures."""

    error_code: str = Field(default="validation_error")
    message: str = Field(default="Request validation failed")
    status_code: int = Field(default=422)
    details: list[ValidationErrorDetail] = Field(default_factory=list)
