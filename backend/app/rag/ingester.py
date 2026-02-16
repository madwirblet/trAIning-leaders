## Document ingestion logic 
#### Chunk document, embed, store in vDB

import os
from typing import List, Dict
from pypdf import PdfReader

# ------------------
# 1. Load .txt files
# ------------------

def load_txt_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ------------------
# 2. Load .pdf files
# ------------------

def load_pdf_file(path: str):
    reader = PdfReader(path)

    full_text = ""
    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text += text + "\n"
    
    return full_text


# ----------------------
# 3. Chunk a file's text
# ----------------------

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks

# ---------------------------------
# 4. Chunk all files in a directory
# ---------------------------------

def build_chunks(folder: str):
    all_chunks = []

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        # .txt files
        if filename.endswith(".txt"):
            text = load_txt_file(path)

        # .pdf files
        elif filename.endswith(".pdf"):
            text = load_pdf_file(path)

        # handle other files
        else:
            continue

        parts = chunk_text(text)

        for i, chunk in enumerate(parts):
            all_chunks.append({
                "chunk": chunk,
                "source": f"{filename}#chunk{i}"
            })
    
    return all_chunks