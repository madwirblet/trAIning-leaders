from app.core.config import settings
from app.core.exceptions import RetrievalError, OpenAIAuthError
from app.rag.embedder import embed_text
from app.rag.vector_store import get_collection
from app.core.relevance import cosine_similarity

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def retrieve(query: str, k: int = settings.TOP_K) -> List[Dict[str, str]]:
    """
    Retrieve the k most relevant documents from the vector database given user query.
    - Convert query into an embedding
    - Perform similarity search against ChromaDB vector store
    - Filter results below the relevance threshold via cosine similarity
    - Return k most relevant text chunks, or raise ValueError if none are relevant

    Each retrieved result of the form:
    {
        "chunk": "<retrieved text content>",
        "source": "<filename>#chunk<i>"
    }

    Raises:
        ValueError: If no retrieved chunks meet the relevance threshold.
        RetrievalError: If the database query itself fails.
        OpenAIAuthError: If embedding generation fails due to auth.
    """
    try:
        logger.info("Retrieving relevant documents")

        collection = get_collection()
        q_vec = embed_text(query)

        results = collection.query(
            query_embeddings=q_vec,
            n_results=k,
            include=["documents", "metadatas", "embeddings"]
        )

        docs = results["documents"][0]
        sources = [m["source"] for m in results["metadatas"][0]]
        embeddings = results["embeddings"][0]

        # Filter chunks that don't meet the relevance threshold
        relevant = [
            {"chunk": doc, "source": src}
            for doc, src, emb in zip(docs, sources, embeddings)
            if cosine_similarity(q_vec, emb) >= settings.RELEVANCE_THRESHOLD
        ]

        if not relevant:
            logger.warning("No relevant documents found for query (threshold=%.2f)", settings.RELEVANCE_THRESHOLD)
            raise ValueError(
                "Your question doesn't appear to be related to the course material. "
                "Please ask something relevant to the course content."
            )

        logger.info("Returning %d/%d chunks above relevance threshold", len(relevant), len(docs))
        return relevant

    except (OpenAIAuthError, ValueError):
        raise

    except Exception as e:
        logger.exception("Retrieval failed: %s", e)
        raise RetrievalError("Failed to retrieve content") from e