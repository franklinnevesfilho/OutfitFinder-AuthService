from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import joinedload

from app.utils import Repository, email_util
from app.models import User, SessionToken
from app.schemas import UserLogin, Tokens, Response, RefreshRequest, UserRegistration, Password
from app.handlers import jwt

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
token_repo = Repository(SessionToken)


def get_token(user_login: OAuth2PasswordRequestForm) -> Response:
    """
    Get a JWT token
    If the user is found and the password is correct, return a response containing the access token
    else return an error response with the appropriate status code and message
    :param user_login: OAuth2PasswordRequestForm model
    :return: Response model containing the access token
    """

    user_login = UserLogin(email=user_login.username, password=user_login.password)
    return login(user_login)


def login(user_login: UserLogin) -> Response:
    """
    Login a user
    If the user is found and the password is correct, return a response containing the access token and refresh token
    else return an error response with the appropriate status code and message
    :param user_login: UserLogin model
    :return: Response model containing the access token and refresh token
    """
    user = user_repo.get_by(email=user_login.email)

    if not user:
        return Response(node={"message": "User not found"}, status=404)

    if not user.verify_password(user_login.password):
        return Response(node={"message": "Invalid password"}, status=401)

    refresh_token = jwt.generate_refresh_token()
    token = SessionToken(
        token=str(refresh_token),
        user_id=user.id
    )

    token_repo.create(token)

    login_response = Tokens(
        access_token=_user_jwt(user),
        refresh_token=str(refresh_token)
    )

    return Response(node=login_response.model_dump(), status=200)

def logout(tokens: Tokens, option: str = None) -> Response:
    """
    Logout a user
    :param tokens: An object containing the access token and refresh token
    :param option: A string indicating the logout option
    :return: Response model
    """
    # first verify the jwt token then delete the refresh token
    result = False
    payload = jwt.decode_jwt(tokens.access_token)
    if payload:
        if option == "all":
            result = token_repo.delete_by(user_id=payload["sub"])
        elif tokens.refresh_token:
            result = token_repo.delete_by(token=tokens.refresh_token)

    if result:
        return Response(node={"message": "Logged out"}, status=200)
    else:
        return Response(node={"message": "Error logging out"}, status=500)

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



async def token_refresh_request(request: RefreshRequest) -> Response:
    """
    Refresh a JWT token
    If the refresh token is valid, return a response containing the new access token
    else return an error response with the appropriate status code and message
    :param request: RefreshRequest model
    :return: Response model containing the new access token
    """
    token = token_repo.get_by(token=request.refresh_token)

    if not token:
        return Response(node={"message": "Invalid refresh token"}, status=401)

    user = user_repo.get_by(id=token.user_id)

    if not user:
        return Response(node={"message": "User not found"}, status=404)

    token_repo.delete(token)

    login_response = Tokens(
        access_token=_user_jwt(user),
        refresh_token=str(jwt.generate_refresh_token())
    )

    return Response(node=login_response.model_dump(), status=200)

def reset_password_request(token: str) -> Response:
    """
    Reset a user's password
    If the token is valid, send a password reset email
    else return an error response with the appropriate status code and message
    :param token: string
    :return: Response model
    """
    payload = jwt.decode_jwt(token)
    if not payload:
        return Response(node={"message": "Invalid token"}, status=401)

    userid = payload["sub"]
    user = user_repo.get_by(id=userid)

    if not user:
        return Response(node={"message": "User not found"}, status=404)

    reset_code = jwt.generate_refresh_token()

    email_util.send_password_reset_email(user.email, reset_code)

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
    payload = jwt.decode_jwt(token)
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
    return jwt.sign_jwt(
        {
            "sub": user.id,
            "rls": [role.name for role in user.roles]
        }
    )