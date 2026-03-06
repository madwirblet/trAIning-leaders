from openai import OpenAI, AuthenticationError
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
    
    except AuthenticationError as e:
        logger.error("OpenAI authentication failed")
        raise OpenAIAuthError("Invalid OpenAI API key") from e

    except Exception as e:
        logger.error("Embedding generation failed: %s", e)
        raise EmbeddingError("Embedding generation failed") from e