### Project Overview

The Personal Research Assistant Agent is a smart end-to-end research system that:
Accepts a user query (e.g., "graph neural networks for recommender systems")
Fetches recent papers and articles from free public sources (arXiv, Crossref, and optional RSS feeds)
Optionally scrapes additional text content from paper URLs
Generates embeddings locally using Ollama’s nomic-embed-text
Stores all chunks in a vector database (ChromaDB)
Retrieves the most relevant text segments
Summarizes everything using Ollama LLM (gemma3:270m)
Produces a structured research report (JSON + Markdown)

* Entirely offline, free, and privacy-preserving
* Built with clean, modular, and maintainable code
* Easily reproducible on any Windows/Linux system

System Architecture

Agents and Flow:
      ```
      User Query
         ↓
      Researcher Agent → arXiv + Crossref + RSS → Fetch Data
         ↓
      Web Scraper → Clean Text → Indexer → Embeddings (Ollama)
         ↓
      Chroma Vector Store → Retrieve Relevant Chunks
         ↓
      Summarizer Agent → Generate JSON + Markdown Report
         ↓
      Final Output (Saved Locally)
      ---

### Technologies Used:
Python 3.10+
Ollama (for LLM + embeddings)
ChromaDB (local vector store)
FastAPI (REST API interface)
Typer (CLI interface)
Rich (logging UI)

### Installation & Setup
1. Clone the Repository
git clone https://github.com/<your-username>/personal-research-assistant.git
cd personal-research-assistant

2. Create a Virtual Environment
python -m venv pra_env
pra_env\Scripts\activate     # On Windows
# or
source pra_env/bin/activate  # On Linux/Mac

3. Install Dependencies
pip install -r requirements.txt

4. Setup Ollama (Free & Local)

Install Ollama from: https://ollama.ai/download
Then pull the required models:
ollama pull gemma3:270m
ollama pull nomic-embed-text


Confirm:
ollama list


You should see:

gemma3:270m
nomic-embed-text

5. Environment Variables (.env)

Edit .env :
OLLAMA_HOST=http://127.0.0.1:11434
GEN_MODEL=gemma3:270m
EMB_MODEL=nomic-embed-text
DATA_DIR=./data

### How to Run (CLI Mode)
## Generate a Research Report
python src/main.py report "graph neural networks for recommender systems" --max-results 5 --days 180 --top-k 5 --out data/samples/gnn_report.json


Flags Explained:
Flag	Meaning
* --max-results	Number of results to fetch from APIs
* --days	Filter papers published in the last N days
* --top-k	Top-K most relevant passages to summarize
* --out	File path to save final JSON/Markdown report
* Trafilatura, Requests, Feedparser (scraping & feeds)

### How to Run (FastAPI + Postman)
Start the Local API
python src/main.py api
You’ll see:
INFO:     Uvicorn running on http://0.0.0.0:8000

### POSTMAN Example

## Endpoint:
POST http://127.0.0.1:8000/report
Headers:
Content-Type: application/json

Body (JSON):
{
  "query": "large language models in education",
  "max_results": 5,
  "days": 180,
  "top_k": 5
}
Response Example:
{
  "query": "large language models in education",
  "report": "{\n  'key_findings': [...],\n  'evidence': [...]\n}"
}

Video Walkthrough Link : https://youtu.be/msvWoU8bwso
