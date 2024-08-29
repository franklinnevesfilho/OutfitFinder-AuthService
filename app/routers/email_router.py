from fastapi import APIRouter
from app.schemas import Response

router = APIRouter(
    tags=["email"],
    prefix="/email"
)

@router.post("/verify-request")
async def verify_request() -> Response:
    pass

@router.get("/{verification_code}")
async def verify(verification_code: str) -> Response:
    pass
