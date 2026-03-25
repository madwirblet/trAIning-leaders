import logging
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import *

logger = logging.getLogger(__name__)

async def openai_auth_exception_handler(request: Request, exc: OpenAIAuthError):
    logger.error("OpenAI authentication error: %s", exc)

    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid or expired OpenAI API key"},
    )


async def embedding_exception_handler(request: Request, exc: EmbeddingError):
    logger.error("Embedding error: %s", exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Embedding generation failed"},
    )


async def generation_exception_handler(request: Request, exc: GenerationError):
    logger.error("LLM generation error: %s", exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "LLM response generation failed"},
    )


async def retrieval_exception_handler(request: Request, exc: RetrievalError):
    logger.error("Retrieval error: %s", exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Failed to retrieve context documents"},
    )


async def vector_store_exception_handler(request: Request, exc: VectorStoreError):
    logger.error("Vector store error: %s", exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Vector database operation failed"},
    )


async def document_exception_handler(request: Request, exc: DocumentProcessingError):
    logger.error("Document processing error: %s", exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Document ingestion failed"},
    )


async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc)

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )