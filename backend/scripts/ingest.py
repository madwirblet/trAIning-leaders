## Script to ingest course documents and repopulate vector database

from app.rag.ingester import build_chunks
from app.rag.vector_store import get_collection
from app.core.config import settings

def main():
    print("Starting ingestion...")

    chunks = build_chunks(settings.DOCS_DIR)
    print(f"Loaded {len(chunks)} chunks")

    collection = get_collection()

    for i, chunk in enumerate(chunks):
        collection.add(
            ids = [str(i)],
            documents = [chunk["chunk"]],
            metadatas = [{"source" : chunk["source"]}],
        )

    print("Ingestion complete.")
    print("Chroma vector DB is ready.")


if __name__ == "__main__":
    main()