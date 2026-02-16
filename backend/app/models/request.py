from pydantic import BaseModel

# Define what frontend sends

class ChatRequest(BaseModel):
    message: str