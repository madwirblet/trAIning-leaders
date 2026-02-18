## RAG Pipeline driver
#### Accept query, embed, similarity search, augment query, generate response

from typing import List, Dict

def answer_query(message: str) -> Dict[str, object]:
    """
    Answer a user query using the RAG pipeline.

    This function interleaves the following subprocesses:
        1. Retrieval of top k similar documents
        2. Construction of an augmented prompt using retrieved contents
        3. Generates a final response using the configured LLM
        4. Returns answer, along with supporting context and source metadata

    Returned dictionary of the form:
    {
        "answer" : "<final chatbot response>",
        "context" : [retrieved chunks],
        "sources" : [sources]
    }
    """

    return {
        "answer": f"LLM offline, see context below\nQuery: {message}",
        "context": ["TODO"],
        "sources": ["TODO"]
    }