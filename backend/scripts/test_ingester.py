from app.rag.ingester import build_chunks

chunks = build_chunks()

print(chunks[0])