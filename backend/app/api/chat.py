## Chat API endpoint
#### Accept chat request, call logic, return LLM response

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Chat Request Schema
class ChatRequest(BaseModel):
    message: str

# Chat Response Schema
class ChatResponse(BaseModel):
    answer: str
    sources : List[str] = []

@router.post("/")
async def chat_endpoint(request: ChatRequest):
    # Temporary chat - return what was said
    return ChatResponse(
        answer = f"Echoed: {request.message}",
        sources = []
    )