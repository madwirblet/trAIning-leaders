# Backend - RAG Chatbot API

This backend powers the Thinkific chatbot widget.

It provides a FastAPI server supporting:

- Document ingestion into a Chroma vector DB
- Retrieval-Augmented Generation (RAG) with LlamaIndex
- Chat responses via OpenAI (GPT-40-mini)

## Tech Stack

- **FastAPI** -- API framework
- **Uvicorn** -- ASGI server
- **ChromaDB** -- local persistent vector database
- **LlamaIndex** -- RAG orchestration
- **OpenAI API**
    - Embeddings: 'text-embedding-3-small'
    - LLM: 'gpt-4o-mini;

## Directory Structure

backend/
├── app/
│ ├── api/
│ ├── core/
│ ├── models/
│ ├── rag/
│ │
│ └── main.py
│
├── docs/
├── data/chroma_db/
├── scripts/
│
├── requirements.txt
├── .env # Local environment variables (not committed)
└── README.md

## Setup Instructions

### Create / Activate Virtual Environment

```bash
# macOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

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

### Environemnt Variables

Create '.env' file in 'backend/' to store API keys

Do not commit this file

### Run the FastAPI Server

Start the FastAPI server (--reload to update when changes are made)
```bash
uvicorn app.main:app --reload
```

To test API endpoints
Go [HERE](http://127.0.0.1:8000/docs)

## Document Ingestion

### Course Content

Place '.txt' and '.pdf' files inside 'backend/docs/'

### Run Ingestion Script

Populate ChromaDB with document chunks:

'''
python scripts/ingest.py
'''

This builds the persistent vector store in 'data/chroma_db'


