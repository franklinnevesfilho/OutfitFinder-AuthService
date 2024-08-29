from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import UserLogin, Response
from .user_handler import login

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