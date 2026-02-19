from app.rag.retriever import retrieve
from app.rag.augmenter import augment_prompt_with_context
from app.rag.generator import generate_answer

from typing import Dict

def rag_service(query: str) -> Dict[str, object]:
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

    chunks, sources = retrieve(query)

    prompt = augment_prompt_with_context(query, chunks)

    answer = generate_answer(prompt)


    return {
        "answer": answer,
        "context": chunks,
        "sources": sources
    }