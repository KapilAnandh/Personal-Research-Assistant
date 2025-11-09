import requests
from src.utils.config import settings


class OllamaLLM:
    def __init__(self, model: str | None = None):
        self.model = model or settings.gen_model
        self.base = settings.ollama_host

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        resp = requests.post(
            f"{self.base}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
            },
            timeout=300,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")