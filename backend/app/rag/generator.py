## RAG Pipeline driver
#### Accept query, embed, similarity search, augment query, generate response

from app.core.config import settings
from app.core.exceptions import OpenAIAuthError, GenerationError
from openai import OpenAI
import logging

client = OpenAI(api_key = settings.OPENAI_API_KEY)
logger = logging.getLogger(__name__)

def generate_answer(prompt: str) -> str:
    """
    Generate LLM response to an engineered prompt. Returns answer.
    """
    try:
        logger.info("Generating response from LLM")

        res = client.chat.completions.create(
            model = settings.LLM_MODEL,
            messages = [{"role" : "user", "content" : prompt}]
        )

        answer = res.choices[0].message.content

        logger.info("Generated response successfully")

        return answer
    
    except Exception as e:
        if "401" in str(e):
            logger.error("OpenAI authentication failed")
            raise OpenAIAuthError("Invalid OpenAI API key") from e

        logger.error("LLM generation failed: %s", e)
        raise GenerationError("LLM generation failed") from e