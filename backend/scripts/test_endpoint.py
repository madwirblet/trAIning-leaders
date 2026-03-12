import requests
import json

# Adjust the port (8000) if your local server runs on a different one (like 5000 for Flask)
# Adjust the path (/chat) to match your actual endpoint route in chat_request.py
URL = "http://localhost:8000/chat"

def test_chatbot(user_message):
    """Simulates the frontend sending a POST request to your backend."""
    
    # This payload structure MUST match what your FastAPI endpoint expects
    # For example, if your endpoint expects a Pydantic model with a "message" field:
    payload = {
        "message": user_message
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    print(f"\n[Sending] -> {user_message}")
    
    try:
        response = requests.post(URL, json=payload, headers=headers)
        
        # Print the HTTP status code (e.g., 200 OK, 400 Bad Request)
        print(f"[Status]  -> {response.status_code}")
        
        # Print the actual JSON response from your RAG pipeline or relevance filter
        print(f"[Reply]   -> {json.dumps(response.json(), indent=2)}")
        
    except requests.exceptions.ConnectionError:
        print("[Error]   -> Could not connect to the server. Is your backend running?")

if __name__ == "__main__":
    # Test 1: A highly relevant question (Should pass the filter)
    test_chatbot("How do I handle conflict resolution within my team?")
    
    # Test 2: A completely irrelevant question (Should be blocked by your new filter)
    test_chatbot("What is the best recipe for baking chocolate chip cookies?")
    
    # Test 3: A borderline question (Good for testing your 0.35 threshold)
    test_chatbot("How do I use Python to manage my schedule?")