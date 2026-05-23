class AppError(Exception):
    """Base class for application errors with HTTP metadata."""

    status_code: int = 500
    error_code: str = "internal_error"
    message: str = "An unexpected error occurred"

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


class CustomExceptionA(AppError):
    """Business rule violation (e.g. invalid input / condition not met)."""

    status_code = 400
    error_code = "condition_not_met"
    message = "The request did not satisfy a required business condition"


class CustomExceptionB(AppError):
    """Requested resource was not found."""

    status_code = 404
    error_code = "resource_not_found"
    message = "The requested resource was not found"
