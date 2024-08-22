from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import (HTTPBearer, OAuth2PasswordBearer,
                              OAuth2PasswordRequestForm)

from app.handlers import auth
from app.schemas import UserLogin, Response, RefreshRequest, UserRegistration, Tokens

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

@router.post("/token")
async def get_token(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Response:
    return auth.get_token(credentials)

@router.post("/token/refresh")
async def refresh_token(refresh_request: RefreshRequest) -> Response:
    return await auth.token_refresh_request(refresh_request)

@router.post("/register")
async def register(user: UserRegistration) -> Response:
    return await auth.register(user)

@router.post("/login")
async def login(user: UserLogin) -> Response:
    return auth.login(user)

@router.post("/logout/all")
async def logout(tokens: Tokens) -> Response:
    return auth.logout(tokens, option="all")

@router.post("/logout")
async def logout(tokens: Tokens) -> Response:
    return auth.logout(tokens)

