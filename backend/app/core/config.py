from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Central backend config - loaded from .env or defaults
    """

    # Vector DB (chroma) persistence
    CHROMA_DIR: str = "data/chroma_db"
    COLLECTION_NAME: str = "course_docs"

    # Document ingestion
    DOCS_DIR: str = "docs"

    # Ingestion Settings
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    # Retrieval Settings
    TOP_K: int = 3

    # OpenAI
    OPENAI_API_KEY: str | None = None
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"

    # Allows .env file to load globals
    class Config:
        env_file = ".env"

# Shared settings instance (import where needed)
settings = Settings()