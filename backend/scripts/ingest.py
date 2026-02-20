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

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk["chunk"])

        collection.add(
            ids = [str(i)],
            documents = [chunk["chunk"]],
            embeddings = [embedding],
            metadatas = [{"source" : chunk["source"]}],
        )

    print("Ingestion complete.")
    print("Chroma vector DB is ready.")


if __name__ == "__main__":
    main()