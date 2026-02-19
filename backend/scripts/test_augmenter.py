from app.rag.augmenter import augment_prompt_with_context

query = "I am asking a question"

context = ["Context Block 1", "Context Block 2", "Context Block 3"]

print(augment_prompt_with_context(query, context))