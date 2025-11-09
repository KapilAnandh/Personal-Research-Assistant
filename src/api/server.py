from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.orchestrator import Orchestrator
from src.utils.logging import info

app = FastAPI(
    title="Personal Research Assistant (Local Ollama)",
    description="Fully local, free research summarization API using Ollama + ChromaDB",
    version="1.0.0"
)

# Initialize once — lightweight reuse between requests
orch = Orchestrator()


class ReportRequest(BaseModel):
    query: str
    max_results: int = 20
    days: int = 365
    top_k: int = 10
    rss_feeds: list[str] | None = None


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"ok": True, "message": "Research Assistant API is running."}


@app.post("/report")
async def generate_report(req: ReportRequest):
    """Run the full pipeline and return a summarized report."""
    info(f"API request received for query: {req.query}")
    report = orch.run(
        query=req.query,
        max_results=req.max_results,
        days=req.days,
        top_k=req.top_k,
        rss_feeds=req.rss_feeds,
    )
    return {"query": req.query, "report": report}


@app.get("/")
async def root():
    """Root index info."""
    return {
        "message": "Welcome to the Local Research Assistant API. Use POST /report to generate summaries.",
        "endpoints": ["/health", "/report"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)