import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------
# ✅ Ensure 'src' package is importable whether run as:
#     python src/main.py
#  or as:
#     python -m src.main
# ---------------------------------------------------------------------
CURRENT_DIR = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_DIR.parent.parent  # go up from src/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------
# Imports (after fixing sys.path)
# ---------------------------------------------------------------------
import typer
from rich.console import Console
from src.agents.orchestrator import Orchestrator
from src.connectors.arxiv_conn import search_arxiv
from src.connectors.crossref_conn import search_crossref
from src.utils.logging import info

# CLI setup
app = typer.Typer(add_completion=False)
console = Console()


# ---------------------------------------------------------------------
# SEARCH COMMAND
# ---------------------------------------------------------------------
@app.command()
def search(query: str, max_results: int = 20, days: int = 365):
    """
    Search papers and articles from arXiv + Crossref.
    Displays metadata but does not summarize.
    """
    info(f"Searching for: {query}")
    arxiv_results = search_arxiv(query, max_results=max_results, days=days)
    crossref_results = search_crossref(query, max_results=max_results, days=days)

    combined = arxiv_results + crossref_results
    console.print(f"\n[bold cyan]Found {len(combined)} results[/bold cyan]\n")

    for i, r in enumerate(combined, 1):
        console.print(
            f"[bold]{i}. {r.get('title')}[/bold]\n"
            f"    URL: {r.get('url')}\n"
            f"    Published: {r.get('published')}\n"
            f"    Source: {r.get('source', 'arxiv/crossref')}\n"
        )


# ---------------------------------------------------------------------
# REPORT COMMAND
# ---------------------------------------------------------------------
@app.command()
def report(
    query: str,
    max_results: int = 20,
    days: int = 365,
    top_k: int = 10,
    out: str | None = None,
):
    """
    Generate a summarized research report (JSON + Markdown)
    using local Ollama LLM.
    """
    info(f"Generating report for: {query}")
    orch = Orchestrator()
    result = orch.run(query=query, max_results=max_results, days=days, top_k=top_k)

    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(result)
        console.print(f"[green]Report saved to:[/green] {out}")
    else:
        console.print(result)


# ---------------------------------------------------------------------
# API COMMAND
# ---------------------------------------------------------------------
@app.command()
def api(port: int = 8000):
    """
    Launch the FastAPI server locally.
    """
    import uvicorn
    info("Starting API server...")
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=port, reload=True)


# ---------------------------------------------------------------------
# ENTRYPOINT
# ---------------------------------------------------------------------
if __name__ == "__main__":
    """
    Run as a standalone script:
        python src/main.py report "graph neural networks for recommender systems"
    or as a module:
        python -m src.main report "graph neural networks for recommender systems"
    """
    app()
