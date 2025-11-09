import requests
from chromadb.utils.embedding_functions import EmbeddingFunction
from src.utils.logging import info
from src.utils.config import settings


class OllamaEmbedding(EmbeddingFunction):
    def __init__(self, model: str | None = None):
        self.model = model or settings.emb_model
        self.base = settings.ollama_host

    def __call__(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        out = []
        for t in texts:
            resp = requests.post(
                f"{self.base}/api/embeddings",
                json={"model": self.model, "prompt": t},
                timeout=120,
            )
            resp.raise_for_status()
            out.append(resp.json()["embedding"])

        return out
