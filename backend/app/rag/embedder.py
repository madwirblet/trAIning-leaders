from openai import OpenAI
from typing import List
from app.core.config import settings

client = OpenAI(api_key = settings.OPENAI_API_KEY)

def embed_text(text: str) -> List[float]:
    res = client.embeddings.create(
        model = settings.EMBEDDING_MODEL,
        input = text
    )
    return res.data[0].embedding