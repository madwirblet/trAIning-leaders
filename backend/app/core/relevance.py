import math
import logging
from typing import List
from app.core.config import settings
from app.rag.embedder import embed_text 

logger = logging.getLogger(__name__)

# Cache the vector globally so it only generates once per server lifecycle
REFERENCE_VECTOR = None

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates the mathematical similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(x * x for x in v1))
    magnitude_v2 = math.sqrt(sum(y * y for y in v2))
    
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
    return dot_product / (magnitude_v1 * magnitude_v2)

def is_query_relevant(user_text: str) -> bool:
    """Checks if the user's query is relevant to the course context."""
    global REFERENCE_VECTOR
    try:
        # Lazy load the reference vector using the string from config.py
        if REFERENCE_VECTOR is None:
            logger.info("Generating reference vector from settings.COURSE_CONTEXT")
            REFERENCE_VECTOR = embed_text(settings.COURSE_CONTEXT)
        
        user_vector = embed_text(user_text)
        score = cosine_similarity(user_vector, REFERENCE_VECTOR)
        logger.info(f"Query relevance score: {score:.3f}")
        
        # Use the threshold from config.py
        return score >= settings.RELEVANCE_THRESHOLD
        
    except Exception as e:
        logger.error("Failed to validate query relevance: %s", e)
        return True