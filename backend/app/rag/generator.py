## RAG Pipeline driver
#### Accept query, embed, similarity search, augment query, generate response

from app.core.config import settings
from openai import OpenAI

client = OpenAI(api_key = settings.OPENAI_API_KEY)

def generate_answer(prompt: str) -> str:
    """
    Generate LLM response to an engineered prompt. Returns answer.
    """

    res = client.chat.completions.create(
        model = settings.LLM_MODEL,
        messages = [{"role" : "user", "content" : prompt}]
    )

    answer = res.choices[0].message.content

    return answer