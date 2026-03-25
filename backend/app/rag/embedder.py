from openai import OpenAI, AuthenticationError
from typing import List, Union
import logging
from app.core.config import settings
from app.core.exceptions import OpenAIAuthError, EmbeddingError

client = OpenAI(api_key = settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)


def embed_text(texts: Union[str, List[str]]) -> List[float]:
    try:
        # Ensure texts is a list
        texts = [texts] if isinstance(texts, str) else texts

        logger.info("Embedding %d texts", len(texts))

        res = client.embeddings.create(
            model = settings.EMBEDDING_MODEL,
            input = texts
        )

        embeddings = [item.embedding for item in res.data]

        logger.info("Embedded text successfully")

        return embeddings
    
    except AuthenticationError as e:
        logger.error("OpenAI authentication failed")
        raise OpenAIAuthError("Invalid OpenAI API key") from e

    except Exception as e:
        logger.error("Embedding generation failed: %s", e)
        raise EmbeddingError("Embedding generation failed") from e