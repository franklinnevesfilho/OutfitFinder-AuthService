from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer,
)
from app.handlers import auth
from app.schemas import (
    UserLogin,
    Response,
    UserRegistration,
    Password
)

"""
This is the Auth Router module

The module contains the routes for the authentication endpoints

routes:
-------
GET /token
    Get a JWT token
    This route requires a valid username and password
    Returns a JWT token
    
POST /token/refresh
    Refresh a JWT token
    This route requires a valid refresh token
    Returns a new JWT token
    
POST /register
    Register a new user
    This route requires a valid username and password
    Returns a JWT token, and a refresh token
    
POST /login
    Login a user
    This route requires a valid username and password
    
POST /logout
    Logout a user
    This route requires a valid JWT token
"""

# Create a router that always requires the bearer token
bearer_scheme = HTTPBearer(bearerFormat="JWT")
auth_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["auth"],
)

@router.post("/register")
async def register(user: UserRegistration) -> Response:
    return auth.register(user)

@router.post("/login")
async def login(user: UserLogin) -> Response:
    return auth.login(user)

@router.get("/password/reset")
async def reset_password(password: Password, token: Annotated[str, Depends(auth_scheme)]) -> Response :
    return auth.reset_password(token, password)

