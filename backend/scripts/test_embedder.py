from app.rag.embedder import embed_text

vec = embed_text("Testing... 1... 2... 3...")

print("Embedding Length: ", len(vec))
print("First 5 values: ", vec[:5])