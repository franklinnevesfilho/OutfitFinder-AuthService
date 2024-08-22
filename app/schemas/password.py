from pydantic import BaseModel


class Password(BaseModel):
    """
    This is the Password schema.
    It is used to validate the password field in the request body, when requesting a reset.
    """
    password: str
