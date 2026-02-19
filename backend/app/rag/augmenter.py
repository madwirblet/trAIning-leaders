from typing import List

def augment_prompt_with_context(query: str, context: List[str]) -> str:
    """
    Augments user's query, returning a prompt that specifies the LLM's role and provides contextually rich text. 
    """

    context_block = ""

    for i, c in enumerate(context):
        context_block += f"Example {i}: {c}\n\n"

    sRole = "---ROLE---\nYou are a teaching assistant for a leadership course, helping answer student questions about the course.\nUse ONLY the context below to answer the question\n\n"
    sContext = f"---CONTEXT---\n{context_block}"
    sQuestion = f"---QUESTION---\n{query}"

    sPrompt = sRole + sContext + sQuestion
    
    return sPrompt


