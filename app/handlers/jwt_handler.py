from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPAuthorizationCredentials
import secrets
from app.utils import JwtUtil

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_session_token():
    """
    Generates a random string of 64 characters
    :return: string
    """
    return secrets.token_urlsafe(64)

def decode_jwt(token: str) -> dict:
    """
    Decode a JWT token
    :param token: HTTPAuthorizationCredentials model containing the JWT token
    :return: The decoded JWT token
    """
    return JwtUtil.decode_jwt(token)

def sign_jwt(payload: dict) -> str:
    """
    Sign a JWT token
    :param payload: The payload to sign
    :return: The signed JWT token
    """
    return JwtUtil.encode_jwt(payload)
