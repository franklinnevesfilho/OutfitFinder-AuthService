from fastapi import APIRouter
from app.schemas import Response

router = APIRouter(
    tags=["token"],
    prefix="/token"
)

@router.post("/")
async def get_token() -> Response:
    pass


