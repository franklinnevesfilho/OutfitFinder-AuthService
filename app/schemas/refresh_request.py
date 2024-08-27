from pydantic import BaseModel


class RefreshRequest(BaseModel):
    """
    This is the RefreshRequest schema.
    It is used to validate the refresh token in the request body, when requesting a token refresh.
    """
    session_token: str