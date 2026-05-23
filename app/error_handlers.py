from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.schemas.errors import ErrorResponse


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


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(CustomExceptionA, handle_custom_exception_a)
    app.add_exception_handler(CustomExceptionB, handle_custom_exception_b)
