from fastapi import APIRouter
from app.api import chat

router = APIRouter()
router.include_router(chat.router, prefix="/api", tags=["Chat"])
