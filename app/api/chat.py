from fastapi import APIRouter
from app.agent import CryptoAgent

router = APIRouter()
crypto_agent = CryptoAgent()

@router.post("/chat")
def chat_with_agent(user_message: str):
    """Main chat endpoint."""
    response = crypto_agent.process_message(user_message)
    return {"response": response}
