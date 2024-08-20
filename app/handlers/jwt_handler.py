from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import secrets
from ..config import JwtUtil

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_refresh_token():
    return secrets.token_urlsafe(64)

def get_current_user(token: str = Depends(_oauth2_scheme)) -> dict:
    return JwtUtil.decode_jwt(token)

def get_current_user_id(token: str = Depends(_oauth2_scheme)) -> int:
    return JwtUtil.decode_jwt(token)["sub"]

def decode_jwt(token: str) -> dict:
    return JwtUtil.decode_jwt(token)

def sign_jwt(payload: dict) -> str:
    return JwtUtil.encode_jwt(payload)

def verify_token(token: str = Depends(_oauth2_scheme)) -> dict:
    return JwtUtil.decode_jwt(token)
