## Script to ingest course documents and repopulate vector database

from app.core.config import settings
from app.rag.ingester import build_chunks
from app.rag.vector_store import get_collection
from app.rag.embedder import embed_text


BATCH_SIZE = 50

def batch_chunks(chunks, batch_size = BATCH_SIZE):
    for i in range(0, len(chunks), batch_size):
        yield chunks[i:i + batch_size]

def main():
    print("Starting ingestion...")

    chunks = build_chunks(settings.DOCS_DIR)
    print(f"Loaded {len(chunks)} chunks")

    collection = get_collection()

    for batch in batch_chunks(chunks, BATCH_SIZE):
        ids = [chunk["id"] for chunk in batch]
        documents = [chunk["text"] for chunk in batch]
        embeddings = embed_text(documents)
        metadatas = [chunk["metadata"] for chunk in batch]

        collection.add(
            ids = ids,
            documents = documents,
            embeddings = embeddings,
            metadatas = metadatas,
        )

    print("Ingestion complete.")
    print("Chroma vector DB is ready.")


if __name__ == "__main__":
    main()