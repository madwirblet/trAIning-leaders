from pydantic import BaseModel
from typing import List

# Define what backend returns

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    context: List[str]