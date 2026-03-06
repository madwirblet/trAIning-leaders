from openai import OpenAI
from typing import List
import logging
from app.core.config import settings
from app.core.exceptions import OpenAIAuthError, EmbeddingError

client = OpenAI(api_key = settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)

def embed_text(text: str) -> List[float]:
    try:
        logger.info("Embedding text")

        res = client.embeddings.create(
            model = settings.EMBEDDING_MODEL,
            input = text
        )

        logger.info("Embedded text successfully")

        return res.data[0].embedding
    
    except Exception as e:

        if "401" in str(e):
            logger.error("OpenAI authentication failed")
            raise OpenAIAuthError("Invalid OpenAI API key") from e

        logger.error("Embedding generation failed: %s", e)
        raise EmbeddingError("Embedding generation failed") from e