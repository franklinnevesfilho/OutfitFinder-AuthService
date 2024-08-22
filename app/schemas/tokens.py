from pydantic import BaseModel


class Tokens(BaseModel):
    """
    This is the Tokens schema.
    It is used to validate the access and refresh tokens in the request body, when requesting a token refresh
    """
    access_token: str
    refresh_token: str