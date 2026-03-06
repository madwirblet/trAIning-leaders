import chromadb
import logging
from app.core.config import settings
from app.core.exceptions import VectorStoreError

client = chromadb.PersistentClient(path = settings.CHROMA_DIR)
logger = logging.getLogger(__name__)

def get_collection() -> chromadb.Collection:
    try:
        logger.info("Connecting to ChromaDB")

        return client.get_or_create_collection(
            name = settings.COLLECTION_NAME
        )
    
    except Exception as e:
        logger.exception("Vector store init failed: %s", e)
        raise VectorStoreError("Vector store init failed") from e