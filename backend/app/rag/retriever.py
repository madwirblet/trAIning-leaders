## Retrieve top k relevant chunks
#### Accept query vector, find top k similar chunks, return them

from app.core.config import settings

from app.rag.vector_store import get_collection

def retrieve(query: str, k: int = settings.TOP_K):
    collection = get_collection()


    # TODO: figure out embeddings
    
    results = collection.query(
        query_embeddings=None,
        n_results=k
    )

    return results["documents"][0]