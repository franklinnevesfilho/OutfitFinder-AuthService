from contextlib import asynccontextmanager, AbstractAsyncContextManager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.config import database, scheduler, JwtUtil
from app.models import Base
from app.routers import auth_router
from app.handlers import (
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


if __name__ == "__main__":
    import uvicorn
    import os
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))
