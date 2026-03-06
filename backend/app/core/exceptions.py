class RAGException(Exception):
    pass

class OpenAIAuthError(RAGException):
    pass

class VectorStoreError(RAGException):
    pass

class RetrievalError(RAGException):
    pass

class DocumentProcessingError(RAGException):
    pass

class EmbeddingError(RAGException):
    pass

class GenerationError(RAGException):
    pass