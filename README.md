# trAIning leaders -- CIS4914

*By: Madelyne Wirbel, Chloe Fandino, Harper Fuchs, Matthew Hughes, Chris Enlow*

This is our repo for our Senior Design project. Completed in Spring 2026.

## Basics

### When working on the project on your local computer

#### 1. Make edits to the desired files

**In the `/frontend`**

- `index.html` --> embeds the chatbot into the Thinkific platform, shell of the chatbot
- `styles.css` --> styling sheet for the chatbot
- `script.js` --> handles chatbot behaviors (open/ close chat, display messages, etc.), API calls to the backend

When you have completed editing the files in the frontend, run:
```bash
py ./bundle.py
```
This will create a new version of `thinkific_footer.html` to be pasted into the footer.


**In the `/backend`**

### When working on the project on your local computer

#### 1. Install necessary dependencies

Create / Activate a virtual environment (venv)
```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Upgrade pip, setuptools, wheel
```bash
pip install --upgrade pip setuptools wheel
```

Install dependencies
```bash
pip install -r requirements.txt
```

When installing new dependencies
```bash
pip install [package]
pip freeze > requirements.txt
```

#### 2. To locally run backend FastAPI Server
Start the FastAPI server (--reload to update when changes are made)
```bash
uvicorn app.main:app --reload
```

To test API endpoints
Go [HERE](http://127.0.0.1:8000/docs)


(Updated when we figure out LLM and API info)

## Important Information

## Major Change Log

- February 11th, 2026 --> project structure/ skeleton pushed to Main
