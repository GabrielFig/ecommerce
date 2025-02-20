from fastapi import Request, Response, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.utils import is_body_allowed_for_status_code

from app.services.utils import log_exception


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    if exc.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        log_exception(exc)

    headers = getattr(exc, "headers", None)

    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)

    return JSONResponse(
        {"message": exc.detail}, status_code=exc.status_code, headers=headers
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors: dict[str, str] = {}

    for item in exc.errors():
        item_loc: tuple | None = item.get("loc", None)
        item_msg: str | None = item.get("msg", None)

        if item_loc is not None and item_msg is not None and len(item_loc) > 0:
            error_loc = item_loc[0]
            error_key = item_loc[0]

            if len(item_loc) > 1:
                error_key = item_loc[1]

            errors[error_key] = f"{error_loc}: {item_msg}"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation error", "erros": errors},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log_exception(exc)
    return JSONResponse(
        content={"message": f"An error occurred: {exc}"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
