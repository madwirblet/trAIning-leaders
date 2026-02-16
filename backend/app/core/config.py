from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Vector DB (chroma)
    CHROMA_DIR: str = None
    COLLECTION_NAME: str = None

    # Ingestion Settings
    DOCS_DIR: str = None
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 50

    # Retrieval Settings
    TOP_K: int = 3

    class Config:
        env_file = ".env"

settings = Settings()