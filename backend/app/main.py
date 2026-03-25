from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.api import chat, health
from app.api.exception_handlers import *
from app.core.logging import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

# Define lifespan for app (startup and shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info(f"{app.title} starting up")

    yield

    # Shutdown logic
    logger.info(f"{app.title} shutting down")


# Start FastAPI app
app = FastAPI(
    title = "Thinkific RAG Chatbot Backend",
    description = "RAG service",
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://leadershipuniversity.thinkific.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix = "/health")
app.include_router(chat.router, prefix = "/chat")

# Include error handlers
app.add_exception_handler(OpenAIAuthError, openai_auth_exception_handler)
app.add_exception_handler(EmbeddingError, embedding_exception_handler)
app.add_exception_handler(GenerationError, generation_exception_handler)
app.add_exception_handler(RetrievalError, retrieval_exception_handler)
app.add_exception_handler(VectorStoreError, vector_store_exception_handler)
app.add_exception_handler(DocumentProcessingError, document_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


# Root endpoint
@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running."}