import requests
import json

URL = "http://localhost:8000/chat"

def test_chatbot(user_message, test_label=""):
    """Simulates the frontend sending a POST request to your backend."""
    payload = {"message": user_message}
    headers = {"Content-Type": "application/json"}

    print(f"\n{'='*60}")
    if test_label:
        print(f"[Test]    -> {test_label}")
    print(f"[Sending] -> {user_message}")

    try:
        response = requests.post(URL, json=payload, headers=headers)
        print(f"[Status]  -> {response.status_code}")
        print(f"[Reply]   -> {json.dumps(response.json(), indent=2)}")

    except requests.exceptions.ConnectionError:
        print("[Error]   -> Could not connect to the server. Is your backend running?")

if __name__ == "__main__":

    # --- RELEVANT QUERIES (should pass the filter and return RAG results) ---
    test_chatbot(
        "What are the key topics covered in this course?",
        "RELEVANT | Core course content query"
    )
    test_chatbot(
        "Can you summarize the main concepts from the lectures?",
        "RELEVANT | Lecture summary request"
    )
    test_chatbot(
        "How do I handle conflict resolution within my team?",
        "RELEVANT | Likely in-domain question"
    )

    # --- IRRELEVANT QUERIES (should be blocked by the relevance filter) ---
    test_chatbot(
        "What is the best recipe for baking chocolate chip cookies?",
        "IRRELEVANT | Completely off-topic"
    )
    test_chatbot(
        "Who won the most recent FIFA World Cup?",
        "IRRELEVANT | Unrelated domain"
    )
    test_chatbot(
        "Write me a poem about the ocean.",
        "IRRELEVANT | Creative task outside course scope"
    )

    # --- BORDERLINE QUERIES (good for tuning your RELEVANCE_THRESHOLD) ---
    test_chatbot(
        "How do I use Python to manage my schedule?",
        "BORDERLINE | Loosely related depending on course content"
    )
    test_chatbot(
        "What are some general tips for staying productive?",
        "BORDERLINE | Vague, may or may not overlap with course material"
    )

    # --- EDGE CASES ---
    test_chatbot(
        "",
        "EDGE CASE | Empty string"
    )
    test_chatbot(
        "   ",
        "EDGE CASE | Whitespace only"
    )
    test_chatbot(
        "a",
        "EDGE CASE | Single character"
    )
    test_chatbot(
        "x" * 2000,
        "EDGE CASE | Extremely long input (2000 chars)"
    )