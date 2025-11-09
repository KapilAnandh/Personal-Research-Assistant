from src.utils.text import clean_text, chunk_text
from src.retrieval.vector_store import VectorStore
from typing import List, Dict


class Indexer:
    def __init__(self, store: VectorStore):
        self.store = store

    def add_document(self, doc_id: str, text: str, meta: Dict):
        text = clean_text(text)
        chunks = chunk_text(text)
        ids = [f"{doc_id}::chunk::{i}" for i in range(len(chunks))]
        metas = [{**meta, "chunk": i} for i in range(len(chunks))]
        self.store.upsert(ids, chunks, metas)

    def search(self, query: str, k: int = 10):
        return self.store.query(query, k)