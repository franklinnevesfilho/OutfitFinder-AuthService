from app.utils import email_util
from app.schemas import Response

def verification_request() -> Response:
    """
    Send an email requesting verification
    Create a JWT with the users id embedded in it and send it to the user's email
    Returns:

    """
    pass

def verify(verification_code: str) -> Response:
    """
    Verify a user's email
    Decode the JWT and mark the user as verified
    Returns:

    """
    pass
