## RAG Pipeline driver
#### Accept query, embed, similarity search, augment query, generate response


def answer_query(message: str):

    return {
        "answer": f"LLM offline, see context below\nQuery: {message}",
        "context": ["TODO"],
        "sources": ["TODO"]
    }