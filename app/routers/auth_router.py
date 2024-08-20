from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from app.handlers import auth
from app.schemas import UserLogin, Response

# Create a router that always requires the bearer token
auth_scheme = HTTPBearer(
    bearerFormat="JWT",
)
router = APIRouter(
    tags=["auth"],
)

@router.get("/token", tags=["auth"])
async def get_token(token: Annotated[str, Depends(auth_scheme)]) -> Response:
    return await auth.token(token)

@router.post(
    "/login",
    tags=["auth"],
)
async def login(user: UserLogin) -> Response:
    return await auth.login(user)

@router.post("/logout", tags=["auth"])
async def logout(token: Annotated[str, Depends(auth_scheme)]) -> Response:
    return await auth.logout(token)

