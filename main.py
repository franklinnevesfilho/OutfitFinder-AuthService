from contextlib import asynccontextmanager, AbstractAsyncContextManager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.config import database, scheduler, logger
from app.utils import JwtUtil, response_util
from app.models import Base
from app.routers import *

Response = response_util.Response

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
    logger.info("Application started")

    yield

    database.db_shutdown()
    scheduler.shutdown()
    logger.info("Application stopped")


app = FastAPI(
    default_response_class=response_util.JsonResponse,
    lifespan=lifespan,
    exception_handlers={
        RequestValidationError: response_util.validation_error_handler,
        HTTPException: response_util.HTTPException_handler
    }
)

app.include_router(user_router)
app.include_router(email_router)
app.include_router(token_router)


"""
This is the health check endpoint for the FastAPI application.
"""
@app.get("/", tags=["health"])
async def health() -> Response:
    return Response(node="Healthy", status=200)

@app.get("/public-key")
async def public_key() -> Response:
    return Response(public_key=JwtUtil.get_public_key_pem(), status=200)


