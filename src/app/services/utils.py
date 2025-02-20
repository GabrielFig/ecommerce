import sys
from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.logger import logger


def log_exception(exc: Exception) -> None:
    exc_type, exc_value, _ = sys.exc_info()
    exc_name = None

    if exc_type:
        exc_name = exc_type.__name__

    if isinstance(exc, HTTPException):
        exc_value = exc.detail

    logger.exception(f"An error ocurred [{exc_name}]: {exc_value}")


def log_request(request: Request, status_code: int, *additional: str) -> None:
    status_phrase = HTTPStatus(status_code).phrase
    host = None
    port = None
    url = request.url.path

    if request.client:
        host = request.client.host
        port = request.client.port

    if request.query_params:
        url += f"?{request.query_params}"

    message = f'{host}:{port} - "{request.method} {url}" {status_code} {status_phrase}'

    for item in additional:
        message += f" {item}"

    logger.info(message)


def raise_(exc: Exception) -> None:
    raise exc
