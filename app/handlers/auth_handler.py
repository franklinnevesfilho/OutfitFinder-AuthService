from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import joinedload

from app.utils import Repository
from app.models import User, RefreshToken
from app.schemas import UserLogin, LoginResponse, Response, RefreshRequest
from app.handlers import jwt

user_repo = Repository(
    base_model=User,
    options=joinedload(User.roles)
)
token_repo = Repository(RefreshToken)


def get_token(userLogin: OAuth2PasswordRequestForm) -> Response:
    """
    Get a JWT token
    If the user is found and the password is correct, return a response containing the access token
    else return an error response with the appropriate status code and message
    :param userLogin: OAuth2PasswordRequestForm model
    :return: Response model containing the access token
    """

    userLogin = UserLogin(email=userLogin.username, password=userLogin.password)
    return login(userLogin)


def login(userLogin: UserLogin) -> Response:
    """
    Login a user
    If the user is found and the password is correct, return a response containing the access token and refresh token
    else return an error response with the appropriate status code and message
    :param userLogin: UserLogin model
    :return: Response model containing the access token and refresh token
    """
    user = user_repo.get_by(email=userLogin.email)

    if not user:
        return Response(node={"message": "User not found"}, status=404)

    if not user.verify_password(userLogin.password):
        return Response(node={"message": "Invalid password"}, status=401)

    refresh_token = jwt.generate_refresh_token()
    token = RefreshToken(
        token=str(refresh_token),
        user_id=user.id
    )

    token_repo.create(token)

    login_response = LoginResponse(
        access_token=_user_jwt(user),
        refresh_token=str(refresh_token)
    )

    return Response(node=login_response.model_dump(), status=200)

def logout(jwtToken: str) -> Response:
    """
    Logout a user
    Remove all refresh tokens associated with the user
    :param jwtToken: HTTPAuthorizationCredentials model containing the JWT token
    :return: Response model containing the message "Logout successful"
    """
    user = user_repo.get_by(id=jwt.decode_jwt(jwtToken)["sub"])
    if not user:
        return Response(node={"message": "User not found"}, status=404)

    token = token_repo.get_by(user_id=user.id)

    if not token:
        return Response(node={"message": "Error logging out"}, status=500)

    token_repo.delete(token)

    return Response(node={"message": "Logout successful"}, status=200)



async def token_refresh_request(request: RefreshRequest) -> Response:
    """
    Refresh a JWT token
    If the refresh token is valid, return a response containing the new access token
    else return an error response with the appropriate status code and message
    :param request: RefreshRequest model containing the refresh token
    :return: Response model containing the new access token
    """
    token = token_repo.get_by(token=request.refresh_token)

    if not token:
        return Response(node={"message": "Invalid refresh token"}, status=401)

    user = user_repo.get_by(id=token.user_id)

    if not user:
        return Response(node={"message": "User not found"}, status=404)

    token_repo.delete(token)

    login_response = LoginResponse(
        access_token=_user_jwt(user),
        refresh_token=str(jwt.generate_refresh_token())
    )

    return Response(node=login_response.model_dump(), status=200)


def _user_jwt(user: User):
    return jwt.sign_jwt(
        {
            "sub": user.id,
            "roles": [role.name for role in user.roles]
        }
    )