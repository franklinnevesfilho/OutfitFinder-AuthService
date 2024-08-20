from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.responses import JSONResponse
from typing import Any, Optional, List
from app.config import logger

# Assuming logger is defined in your .config module

_status_codes = {
    200: "success",
    201: "created",
    204: "no content",
    400: "bad request",
    401: "unauthorized",
    403: "forbidden",
    404: "not found",
    405: "method not allowed",
    409: "conflict",
    422: "unprocessable entity",
    500: "internal server error",
    501: "not implemented",
    503: "service unavailable",
    504: "gateway timeout"
}


class Response(BaseModel):
    node: Optional[Any] = None
    errors: List[str] = []
    status: int = 200

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        logger.info(f"Response created with status: {self.status} - {_status_codes[self.status]}")


class JsonResponse(JSONResponse):

    def __init__(self, response: BaseModel, status_code=200, **kwargs):
        super().__init__(content=response.model_dump(), status_code=status_code, **kwargs)


def validation_error_handler(request, exc: RequestValidationError):
    """
    Custom exception handler for RequestValidationError.
    :param request: The request object.
    :param exc: The exception object.
    :return: JsonResponse
    """
    errors = []
    for error in exc.errors():
        errors.append(f'{error["loc"][0]}: {error["msg"]}')

    # Return a JsonResponse with the proper Response object
    return JsonResponse(Response(node=None, errors=errors, status=422))
