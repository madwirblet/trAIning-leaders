## Configure environment variables that are usable throughout the server

import os
from pydantic_settings import BaseSettings

def resolve_env_file():
    """
    .env Path Resolver
    Locally, .env is stored in the root of 'backend/'
    On Render Deployment, .env is mounted in 'backend/secrets/'
    If neither is present, return None => server crashes
    """
    
    if os.path.exists(".env"):
        return ".env"
    if os.path.exists("./etc/secrets/.env"):
        return "./etc/secrets/.env"
    return None


class Settings(BaseSettings):
    """
    Central backend config - loaded from .env or defaults
    """
    # Python Version
    PYTHON_VERSION: str | None = None
    
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

    # Query Relevance
    RELEVANCE_THRESHOLD: float = 0.35 

    COURSE_CONTEXT: str = "Leadership course, team management, conflict resolution, emotional intelligence, and personal development principles."

    # OpenAI
    OPENAI_API_KEY: str | None = None
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    LLM_MODEL: str = "gpt-4o-mini"

    # Allows .env file to load globals
    class Config:
        env_file = resolve_env_file()

# Shared settings instance (import where needed)
settings = Settings()