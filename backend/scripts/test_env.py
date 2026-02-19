## Test Script to ensure OpenAI API key is loaded

import os
from app.core.config import settings

print("Current working directory: ", os.getcwd())
print("Env file exists: ", os.path.exists(".env"))
print("OPENAI_API_KEY loaded: ", settings.OPENAI_API_KEY is not None)
print("Key starts with: ", settings.OPENAI_API_KEY[:5])