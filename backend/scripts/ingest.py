## Script to ingest course documents and repopulate vector database

from app.core.config import settings
from app.rag.ingester import build_chunks
from app.rag.vector_store import get_collection
from app.rag.embedder import embed_text

def main():
    print("Starting ingestion...")

    chunks = build_chunks(settings.DOCS_DIR)
    print(f"Loaded {len(chunks)} chunks")

    collection = get_collection()

    for chunk in chunks:
        id = chunk["id"]
        text = chunk["text"]
        embedding = embed_text(chunk["text"])
        
        metadata = chunk["metadata"]

        collection.add(
            ids = [id],
            documents = [text],
            embeddings = [embedding],
            metadatas = [metadata],
        )

    print("Ingestion complete.")
    print("Chroma vector DB is ready.")


if __name__ == "__main__":
    main()