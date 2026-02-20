import chromadb
from app.core.config import settings

client = chromadb.PersistentClient(path = settings.CHROMA_DIR)

def get_collection() -> chromadb.Collection:
    return client.get_or_create_collection(
        name = settings.COLLECTION_NAME
    )