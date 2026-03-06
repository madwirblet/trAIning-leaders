import chromadb
import logging
from app.core.config import settings

client = chromadb.PersistentClient(path = settings.CHROMA_DIR)
logger = logging.getLogger(__name__)

def get_collection() -> chromadb.Collection:
    try:
        logger.info("Connecting to ChromaDB")

        return client.get_or_create_collection(
            name = settings.COLLECTION_NAME
        )
    
    except Exception:
        logger.exception("Vector store initialization failed")
        raise