## Chat API endpoint
#### Accept chat request, call logic, return LLM response

from fastapi import APIRouter, HTTPException
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from backend.app.rag.rag_orchestrator import rag_service

router = APIRouter()


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    try:
        result = rag_service(request.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))