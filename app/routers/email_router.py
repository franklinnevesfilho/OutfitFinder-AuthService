from fastapi import APIRouter
from app.handlers import email_handler
from app.schemas import Response

router = APIRouter(
    tags=["email"],
    prefix="/email"
)

@router.post("/verify-request")
async def verify_request() -> Response:
    return email_handler.verification_request()

@router.get("/{verification_code}")
async def verify(verification_code: str) -> Response:
    return email_handler.verify(verification_code)
