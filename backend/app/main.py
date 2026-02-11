from fastapi import FastAPI
from app.api import chat, health

app = FastAPI(title = "Thinkific RAG Chatbot Backend")

# Include routers
app.include_router(health.router, prefix = "/health")
app.include_router(chat.router, prefix = "/chat")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "RAG CHatbot Backend is running."}