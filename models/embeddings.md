# 🔢 Embedding Model — `nomic-embed-text`

## Overview
This agent uses **Ollama’s `nomic-embed-text`** model to generate vector embeddings for document chunks.
Embeddings are used for similarity search and retrieval in the **ChromaDB** vector database.

- **Provider**: [Ollama](https://ollama.com)
- **Model name**: `nomic-embed-text`
- **Size**: ~274 MB
- **License**: Apache 2.0 (Open-Source)
- **Local inference**: 100 % offline, no API keys needed.

---

## Architecture
| Step | Description |
|------|--------------|
| 1️⃣ | Text passages are cleaned and chunked (≈ 1200 chars, 200 overlap). |
| 2️⃣ | Each chunk is sent to Ollama’s `/api/embeddings` endpoint. |
| 3️⃣ | The resulting 768-dimensional vectors are stored in **ChromaDB**. |
| 4️⃣ | Later, queries are embedded the same way and matched by cosine similarity. |

---

## Example API Call
```python
import requests

payload = {
  "model": "nomic-embed-text",
  "prompt": "Graph neural networks improve link prediction in social networks."
}
resp = requests.post("http://127.0.0.1:11434/api/embeddings", json=payload)
print(len(resp.json()["embedding"]))  # e.g. 768
