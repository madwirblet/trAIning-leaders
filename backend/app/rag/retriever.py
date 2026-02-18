## Retrieve top k relevant chunks
#### Accept query vector, find top k similar chunks, return them

from app.core.config import settings
from app.rag.vector_store import get_collection

from typing import List, Dict

def retrieve(query: str, k: int = settings.TOP_K) -> List[Dict[str,str]]:
    """
    Retrieve the k most relevant documents from the vector database given user query.
    - Convert query into an embedding
    - Perform similarity search against Chrome vector store
    - Return k most relevant text chunks

    Each retrieved result of the form:
    {
        "chunk": "<retrieved text content>",
        "source": "<filename>#chunk<i>"
    }
    """


    collection = get_collection()


    # TODO: figure out embeddings

    results = collection.query(
        query_embeddings=None,
        n_results=k
    )

    return results["documents"][0]