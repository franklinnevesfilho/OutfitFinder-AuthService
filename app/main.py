from fastapi import FastAPI
from app.handlers.response_handler import RequestValidationError, JsonResponse, validation_error_handler, Response

app = FastAPI(
    default_response_class=JsonResponse,
    exception_handlers={RequestValidationError: validation_error_handler}
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return Response(node=f"Hello {name}!", status=200)
