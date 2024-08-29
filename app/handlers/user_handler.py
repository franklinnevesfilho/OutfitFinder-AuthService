from sqlalchemy.orm import joinedload
from typing import Optional

from app.utils import Repository
from app.models import User
from app.schemas import UserLogin, Response, UserRegistration, Password
from app.handlers import jwt_handler


"""
This is the Auth Handler module

The module contains the business logic for the authentication endpoints

functions:
-----------
get_token
    Get a JWT token
    
login
    Login a user
    
logout
    Logout a user
    
register
    Register a new user
    
token_refresh_request
    Refresh a JWT token
    
reset_password_request
    Send an email requesting a password reset
    
reset_password
    Reset a user's password
    
_user_jwt
    get the jwt token for the user
"""

user_repo = Repository(
    base_model=User,
    options=joinedload(User.roles)
)


def login(user_login: UserLogin) -> Response:
    """
    Login a user
    If the user is found and the password is correct, return a response containing the access token and refresh token
    else return an error response with the appropriate status code and message
    :param user_login: UserLogin model
    :return: Response model containing the access token and refresh token
    """
    user: Optional[User] = user_repo.get_by(email=user_login.email)

    if not user:
        return Response(node={"message": "User not found"}, status=404)

    if not user.verify_password(user_login.password):
        return Response(node={"message": "Invalid password"}, status=401)

    return Response(node=_user_jwt(user), status=200)


def register(user: UserRegistration) -> Response:
    """
    Register a new user
    If the user is successfully created, return a response containing the access token and refresh token
    else return an error response with the appropriate status code and message
    :param user: UserRegistration model
    :return: Response model containing the access token and refresh token
    """

    if user_repo.get_by(email=user.email):
        return Response(node={"message": "User already exists"}, status=409)

    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
    )

    new_user.set_password(user.password)

    user_repo.create(new_user)

    return login(UserLogin(email=user.email, password=user.password))


def reset_password_request(token: str) -> Response:
    """
    Reset a user's password
    If the token is valid, send a password reset email
    else return an error response with the appropriate status code and message
    :param token: string
    :return: Response model
    """
    return Response(node={"message": "Password reset request sent"}, status=200)

def reset_password(token: str, password: Password) -> Response:
    """
    Reset a user's password
    If the token is valid, reset the user's password
    else return an error response with the appropriate status code and message
    :param token: a string representation of a jwt token containing the user's id
    :param password: the new password
    :return: Response model
    """
    response = Response()
    payload = jwt_handler.decode_jwt(token)
    if payload:
        userid = payload["sub"]
        user = user_repo.get_by(id=userid)

        if user:
            user.set_password(password.password)
            user_repo.update(user)
            # Update response
            response.status = 200
            response.node = {"message": "Password reset"}
        else:
            # Update response
            response.status = 404
            response.node = {"message": "User not found"}
    else:
        # Update response
        response.status = 401
        response.node = {"message": "Invalid token"}

    return response


def _user_jwt(user: User):
    """
    get the jwt token for the user
    :param user:
    :return: the jwt token containing the user's id and roles
    """
    return jwt_handler.sign_jwt(
        {
            "sub": user.id,
            "roles": [role.name for role in user.roles],
        }
    )