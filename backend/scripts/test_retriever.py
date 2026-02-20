from app.rag.retriever import retrieve

docs, sources = retrieve("What is this course about?")

print("Retrieved Docs:")
for d in docs:
    print("- ", d[:100])

print("Sources: ", sources)