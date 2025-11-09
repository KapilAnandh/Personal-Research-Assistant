import re


def clean_text(t: str) -> str:
    t = t.replace("\r", " ").replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def chunk_text(t: str, chunk_size: int = 1200, overlap: int = 200):
    chunks = []
    i = 0
    while i < len(t):
        chunks.append(t[i:i + chunk_size])
        i += (chunk_size - overlap)
    return chunks
