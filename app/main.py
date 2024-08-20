from fastapi import FastAPI, Depends
from app.handlers import (
    validation_error_handler,
    JsonResponse,
    Response,
    RequestValidationError,
    jwt
)

app = FastAPI(
    default_response_class=JsonResponse,
    exception_handlers={RequestValidationError: validation_error_handler}
)


@app.get("/", tags=["health"])
async def health() -> Response:
    return Response(node="Healthy!", status=200)


@app.get("/hello/{name}")
async def say_hello(name: str) -> Response:
    return Response(node=f"Hello {name}!", status=200)

@app.post("/token", tags=["auth"])
async def token(payload: dict) -> Response:
    return Response(node=jwt.sign_jwt(payload), status=200)

@app.get("/verify", tags=["auth"])
async def verify(payload: dict = Depends(jwt.verify_token)) -> Response:
    return Response(node=payload, status=200)
