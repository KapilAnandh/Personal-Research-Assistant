import chromadb
from chromadb.config import Settings as ChromaSettings
from src.utils.config import settings
from src.retrieval.embedding_ollama import OllamaEmbedding


class VectorStore:
    def __init__(self, collection_name: str = "papers"):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_dir,
            settings=ChromaSettings(allow_reset=True)
        )
        self.embed = OllamaEmbedding()
        self.col = self.client.get_or_create_collection(
            collection_name,
            embedding_function=self.embed
        )

    def upsert(self, ids, texts, metadatas):
        self.col.upsert(ids=ids, documents=texts, metadatas=metadatas)

    def query(self, text: str, k: int = 8):
        return self.col.query(query_texts=[text], n_results=k)