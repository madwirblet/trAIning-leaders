## Chat API endpoint
#### Accept chat request, call logic, return LLM response

from fastapi import APIRouter, HTTPException
import logging
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.rag.rag_orchestrator import rag_service
from app.core.relevance import is_query_relevant

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/")
async def chat_endpoint(request: ChatRequest):
    logger.info("Chat request received")

    if not is_query_relevant(request.message):
        # Return a polite, hardcoded rejection if it's off-topic
        return {
            "reply": "I am specifically designed to help with this leadership course material. Could you rephrase your question to relate to the course?"
        }

    result = rag_service(request.message)

    logger.info("Chat request complete")

    return ChatResponse(**result)
