import re
from typing import List

def clean_text(text: str) -> str:
    """
    Cleans the raw document by removing extra spaces and newlines.
    """
    text = re.sub(r'\s+', ' ', text)      # Replace multiple spaces/newlines with single space
    return text.strip()                   # Remove spaces at beginning/end


def chunk_text(text: str, chunk_size: int = 180, overlap: int = 40) -> List[str]:
    """
    Splits the cleaned text into overlapping chunks.
    chunk_size = number of words per chunk
    overlap = repeated words between chunks for smooth continuity
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        
        start += chunk_size - overlap  # move forward with overlap

    return chunks
