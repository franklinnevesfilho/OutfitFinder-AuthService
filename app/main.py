from contextlib import asynccontextmanager, AbstractAsyncContextManager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from config import database, scheduler, JwtUtil
from models import Base
from routers import auth_router
from handlers import (
    validation_error_handler,
    JsonResponse,
    Response,
    HTTPException_handler
)

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


@app.get("/", tags=["health"])
async def health() -> Response:
    return Response(node="Healthy", status=200)


