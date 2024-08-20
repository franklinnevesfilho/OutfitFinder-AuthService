from typing import Any, List, Optional
from pydantic import BaseModel
from app.config import logger

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