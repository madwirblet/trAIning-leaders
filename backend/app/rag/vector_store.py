import chromadb
from app.core.config import settings

def get_collection():
    client = chromadb.PersistentClient(path = settings.CHROMA_DIR)
    return client.get_or_create_collection(settings.COLLECTION_NAME)