from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.schemas.errors import ErrorResponse, ValidationErrorDetail, ValidationErrorResponse


def _build_error_response(exc: CustomExceptionA | CustomExceptionB) -> ErrorResponse:
    return ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        status_code=exc.status_code,
    )


async def handle_custom_exception_a(
    request: Request, exc: CustomExceptionA
) -> JSONResponse:
    print(f"[ERROR] {exc.error_code} path={request.url.path} message={exc.message}")
    body = _build_error_response(exc)
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def handle_custom_exception_b(
    request: Request, exc: CustomExceptionB
) -> JSONResponse:
    print(f"[ERROR] {exc.error_code} path={request.url.path} message={exc.message}")
    body = _build_error_response(exc)
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


def _format_validation_errors(exc: RequestValidationError) -> list[ValidationErrorDetail]:
    details: list[ValidationErrorDetail] = []
    for err in exc.errors():
        loc = err.get("loc", ())
        err_type = err.get("type", "")

        if err_type in ("json_invalid", "value_error.jsondecode"):
            field = "body"
            message = "Invalid JSON in request body"
        else:
            field_parts = [
                str(part)
                for part in loc
                if part != "body" and not isinstance(part, int)
            ]
            field = ".".join(field_parts) if field_parts else "body"
            message = err.get("msg", "Invalid value")

        details.append(ValidationErrorDetail(field=field, message=message))
    return details


def register_validation_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        print(f"[VALIDATION ERROR] path={request.url.path} errors={exc.errors()}")
        body = ValidationErrorResponse(
            message="Request validation failed",
            status_code=422,
            details=_format_validation_errors(exc),
        )
        return JSONResponse(status_code=422, content=body.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(CustomExceptionA, handle_custom_exception_a)
    app.add_exception_handler(CustomExceptionB, handle_custom_exception_b)
    register_validation_handler(app)
