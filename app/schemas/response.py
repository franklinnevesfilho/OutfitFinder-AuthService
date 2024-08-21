from typing import Any, List, Optional
from pydantic import BaseModel
from app.config import logger

"""
This is the Response schema. It is used to return a response to the client.

Attributes:
    node (Any): The response data.
    errors (List[str]): A list of errors.
    status (int): The status code of the response.
    
    logger (Logger): The logger object used for logging.
    _status_codes (dict): A dictionary of status codes and their corresponding messages.
"""

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