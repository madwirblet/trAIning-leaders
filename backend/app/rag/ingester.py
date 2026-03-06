## Document ingestion logic 
#### Chunk document, embed, store in vDB

import os
from typing import List, Dict
from pypdf import PdfReader
import logging
from app.core.config import settings
from app.core.exceptions import DocumentProcessingError

logger = logging.getLogger(__name__)

# ------------------
# 1. Load .txt files
# ------------------

def load_txt_file(path: str) -> str:
    try:
        logger.info(f"Loading TXT file: {path}")

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        logger.info(f"Loaded TXT file successfully: {path}")
        
        return text
    
    except Exception as e:
        logger.error("Failed to load TXT file %s: %s", path, e)
        raise DocumentProcessingError("Failed to load TXT document") from e

# ------------------
# 2. Load .pdf files
# ------------------

def load_pdf_file(path: str) -> str:
    try:
        logger.info(f"Loading PDF file: {path}")
        reader = PdfReader(path)

        full_text = ""
        for page in reader.pages:
            text = page.extract_text()

            if text:
                full_text += text + "\n"
        
        logger.info(f"Loaded PDF successfully: {path}")

        return full_text
    
    except Exception as e:
        logger.error("Failed to load PDF file %s: %s", path, e)
        raise DocumentProcessingError("Failed to load PDF document") from e


# ----------------------
# 3. Chunk a file's text
# ----------------------

def chunk_text(text: str, chunk_size: int = settings.CHUNK_SIZE, overlap: int = settings.CHUNK_OVERLAP) -> List[str]:
    """
    Split raw text into overlapping chunks for embedding and retrieval.

    Args:
        text : Full input document text to be chunked
        chunk_size : max number of characters in a chunk
        overlap : number of characters shared between consecutive chunks
    """
    try:
        logger.info("Chunking text")
        
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap

        logger.info(f"Generated {len(chunks)} chunks")

        return chunks
    
    except Exception as e:
        logger.error("Chunking failed: %s", e)
        raise DocumentProcessingError("Text chunking failed") from e

# ---------------------------------
# 4. Chunk all files in a directory
# ---------------------------------

def build_chunks(folder: str = settings.DOCS_DIR) -> List[Dict[str, str]]:
    """
    Load all supported files from a folder and convert them into chunked segments for ingestion to vector DB

    Returned chunks have the form:
    {
        "chunk" : "<text content>",
        "source" : "<filename>#<chunk<i>"
    }

    Args:
        folder : path to the directory containing course docs
    """
    try:
        logger.info(f"Building chunks from directory: {folder}")   

        all_chunks = []

        files = os.listdir(folder)

        logger.info(f"Found {len(files)} documents")

        for filename in files:
            path = os.path.join(folder, filename)

            # .txt files
            if filename.endswith(".txt"):
                text = load_txt_file(path)

            # .pdf files
            elif filename.endswith(".pdf"):
                text = load_pdf_file(path)

            # handle other files
            else:
                logger.warning(f"Unsupported file type skipped: {filename}")
                continue

            parts = chunk_text(text)

            for i, chunk in enumerate(parts):
                all_chunks.append({
                    "chunk": chunk,
                    "source": f"{filename}#chunk{i}"
                })
        
        logger.info(f"Total chunks created: {len(all_chunks)}")

        return all_chunks

    except Exception as e:
        logger.error("Chunk building failed: %s", e)
        raise DocumentProcessingError("Failed to build chunks") from e