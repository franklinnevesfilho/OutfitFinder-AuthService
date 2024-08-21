from contextlib import asynccontextmanager, AbstractAsyncContextManager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.config import database, scheduler
from app.utils import JwtUtil
from app.models import Base
from app.routers import auth_router
from app.handlers import (
    validation_error_handler,
    JsonResponse,
    Response,
    HTTPException_handler
)

"""
This is the main entry point for the FastAPI application.

The `lifespan` context manager is used to manage the lifecycle of the application.
The `database.db_init` method is called to initialize the database connection.
The `scheduler.start` method is called to start the background scheduler.
The `JwtUtil.generate_keys` method is called to generate the RSA keys used for JWT signing.
"""
Base.metadata.create_all(bind=database.get_engine())

@asynccontextmanager
async def lifespan(app) -> AbstractAsyncContextManager[None]:
    JwtUtil.generate_keys()
    database.db_init()
    scheduler.start()

    yield

    database.db_shutdown()
    scheduler.shutdown()


app = FastAPI(
    default_response_class=JsonResponse,
    lifespan=lifespan,
    exception_handlers={
        RequestValidationError: validation_error_handler,
        HTTPException: HTTPException_handler
    }
)

app.include_router(auth_router)


"""
This is the health check endpoint for the FastAPI application.
"""
@app.get("/", tags=["health"])
async def health() -> Response:
    return Response(node="Healthy", status=200)


