## Chat API endpoint
#### Accept chat request, call logic, return LLM response

from fastapi import APIRouter, HTTPException
import logging
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.rag.rag_orchestrator import rag_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    logger.info("Chat request received")

    result = rag_service(request.message)

    logger.info("Chat request complete")

    return ChatResponse(**result)
