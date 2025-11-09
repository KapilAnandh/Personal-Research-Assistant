from pydantic import BaseModel
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


class Settings(BaseModel):
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
    gen_model: str = os.getenv("GEN_MODEL", "gemma3:270m")
    emb_model: str = os.getenv("EMB_MODEL", "nomic-embed-text")
    data_dir: str = os.getenv("DATA_DIR", "./data")
    cache_dir: str = os.getenv("CACHE_DIR", "./data/cache")
    chroma_dir: str = os.getenv("CHROMA_DIR", "./data/chroma")
    memory_file: str = os.getenv("MEMORY_FILE", "./data/memory.yaml")

    def ensure_dirs(self):
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.chroma_dir).mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_dirs()
