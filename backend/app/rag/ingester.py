## Document ingestion logic 
#### Chunk document, embed, store in vDB

import os
from typing import List, Dict, Any
from pypdf import PdfReader
import logging
from app.core.config import settings
from app.core.exceptions import DocumentProcessingError

logger = logging.getLogger(__name__)

# ---------------
# Load .txt files
# ---------------

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


# ---------------
# Load .pdf files
# ---------------

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


# -------------------
# Chunk a file's text
# -------------------

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
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])

            if end == len(text):
                break

            start += chunk_size - overlap

        logger.info(f"Generated {len(chunks)} chunks")

        return chunks
    
    except Exception as e:
        logger.error("Chunking failed: %s", e)
        raise DocumentProcessingError("Text chunking failed") from e


# --------------
# Process a File
# --------------

def process_file(path: str, module: str) -> List[Dict[str, Any]]:
    """
    Load a file, chunk it, attach metadata

    Returned chunks have the form:
    {
        "text": chunk's raw text,
        "metadata": {
            "module": module name
            "source": file name
            "index": chunk number within file
        }
    }
    """

    try:
        filename = os.path.basename(path)

        if filename.endswith(".txt"):
            text = load_txt_file(path)
        elif filename.endswith(".pdf"):
            text = load_pdf_file(path)
        else:
            logger.warning("Unsupported file skipped: %s", filename)
            return []
        
        chunks = chunk_text(text)
        res = []

        for i, chunk in enumerate(chunks):
            res.append({
                "text": chunk,
                "metadata": {
                    "module": module,
                    "source": filename,
                    "index": i
                }
            })

        return res
    except Exception as e:
        logger.error("File processing failed: %s", e)
        raise DocumentProcessingError("File processing failed") from e


# ----------------
# Process a Module
# ----------------  

def process_module(module_dir: str) -> List[Dict[str, Any]]:
    """
    Processes all files within a module directory

    Returns list of all chunked files + metadata within directory
    """

    try:
        module = os.path.basename(module_dir)
        res = []

        for entry in os.listdir(module_dir):
            path = os.path.join(module_dir, entry)

            if os.path.isfile(path) and (entry.endswith(".txt") or entry.endswith(".pdf")):
                file_chunks = process_file(path, module)
                res.extend(file_chunks)
            else:
                logger.warning("Skipped unsupported entry: %s", entry)

        logger.info("Module %s produced %d chunks", module, len(res))
        return res
    
    except Exception as e:
        logger.error("Module processing failed: %s", e)
        raise DocumentProcessingError("Module processing failed for: %s", module_dir) from e


# -----------
# Entry point
# ----------- 

def build_chunks(root_dir: str = settings.DOCS_DIR) -> List[Dict[str, Any]]:
    """
    Load all supported files from a folder and convert them into chunked segments for ingestion to vector DB

    Returned chunks have the form:
    {
        "text": chunk's raw text,
        "metadata": {
            "module": module name
            "source": file name
            "index": chunk number within file
        }
    }

    Args:
        folder : path to the directory containing course docs
    """
    try:
        logger.info(f"Building chunks from directory: {root_dir}")   

        res = []

        for entry in os.listdir(root_dir):
            module_dir = os.path.join(root_dir, entry)

            # Ignore root level documents
            if not os.path.isdir(module_dir):
                continue
            else:
                module_chunks = process_module(module_dir)
                res.extend(module_chunks)
    
        logger.info(f"Total chunks created: {len(res)}")

        return res

    except Exception as e:
        logger.error("Chunk building failed: %s", e)
        raise DocumentProcessingError("Failed to build chunks") from e