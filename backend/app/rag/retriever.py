## Retrieve top k relevant chunks
#### Accept query vector, find top k similar chunks, return them

from app.core.config import settings
from app.core.exceptions import RetrievalError, OpenAIAuthError
from app.rag.embedder import embed_text
from app.rag.vector_store import get_collection

from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

def filter_by_dist(docs: List[str], sources: List[str], distances: List[float], threshold: float) -> Tuple[List[str], List[str]]:
    logger.info("Filtering documents...")

    filtered_docs = []
    filtered_sources = []

    for doc, src, dist in zip(docs, sources, distances):
        if dist <= threshold:
            filtered_docs.append(doc)
            filtered_sources.append(src)

    return filtered_docs, filtered_sources


def retrieve(query: str, k: int = settings.TOP_K) -> Tuple[List[str], List[str]]:
    """
    Retrieve the k most relevant documents from the vector database given user query.
    - Convert query into an embedding
    - Perform similarity search against ChromaDB vector store
    - Return k most relevant text chunks

    Each retrieved result of the form:
    {
        "chunk": "<retrieved text content>":
        "source": "<filename>#chunk<i>"
    }
    """

    try:
        logger.info("Retrieving relevant documents")

        collection = get_collection()
        qVec = embed_text(query)

        results = collection.query(
            query_embeddings = qVec,
            n_results = k,
            include = ["documents", "distances", "metadatas"]
        )


        docs = results["documents"][0]
        sources = [m["source"] for m in results["metadatas"][0]]
        distances = results["distances"][0]

        logger.info(f"Retrieved {len(docs)} documents")

        docs, sources = filter_by_dist(docs, sources, distances, threshold=settings.EMBEDDING_THRESHOLD)

        logger.info(f"Filtered to {len(docs)} relevant documents")

        return docs, sources
    
    except OpenAIAuthError:
        raise

    except Exception as e:
        logger.exception("Retrieval failed: %s", e)
        raise RetrievalError("Failed to retrieve content") from e