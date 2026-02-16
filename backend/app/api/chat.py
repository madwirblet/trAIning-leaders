## Chat API endpoint
#### Accept chat request, call logic, return LLM response

from fastapi import APIRouter
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.rag.rag_service import answer_query

router = APIRouter()


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    result = answer_query(request.message)
    # Temporary chat - return what was said
    return ChatResponse(**result)