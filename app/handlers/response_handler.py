from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.schemas.response import Response
from fastapi import HTTPException
from pydantic import BaseModel
# Assuming logger is defined in your .config module


class JsonResponse(JSONResponse):

    def __init__(self, response, status_code=200, **kwargs):
        if isinstance(response, Response):
            response = response.model_dump()
        super().__init__(response, status_code, **kwargs)


def validation_error_handler(request, exc: RequestValidationError):
    """
    Custom exception handler for RequestValidationError.
    :param request: The request object.
    :param exc: The exception object.
    :return: JsonResponse
    """
    errors = []
    for err in exc.errors():
        errors.append(f'{err["loc"][0]}: {err["msg"]}')

    # Return a JsonResponse with the proper Response object
    return JsonResponse(Response(node=None, errors=errors, status=422))

def HTTPException_handler(request, exc: HTTPException):
    """
    Custom exception handler for HTTPException.
    :param request: The request object.
    :param exc: The exception object.
    :return: JsonResponse
    """
    return JsonResponse(Response(node=None, errors=[exc.detail], status=exc.status_code))
