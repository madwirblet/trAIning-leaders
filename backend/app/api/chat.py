## Chat API endpoint
#### Accept chat request, call logic, return LLM response

from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse

router = APIRouter()


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    # Temporary chat - return what was said
    return ChatResponse(
        answer = f"Echoed: {request.message}",
        sources = [],
        context = []
    )