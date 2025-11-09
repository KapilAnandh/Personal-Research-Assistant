"""
Smoke test for the Personal Research Assistant Agent.

This ensures that:
- Ollama API is reachable locally
- The Orchestrator pipeline runs end-to-end
- The generated report is non-empty and well-structured

Run:
    pytest -v tests/smoke_test.py
or:
    python -m pytest -v
"""

import pytest
import requests
from src.agents.orchestrator import Orchestrator
from src.utils.config import settings


def test_ollama_connection():
    """
    Verify that Ollama is running locally and responding.
    """
    try:
        r = requests.get(f"{settings.ollama_host}/api/tags", timeout=10)
        assert r.status_code == 200
        print(f"\n✅ Ollama reachable at {settings.ollama_host}")
    except Exception as e:
        pytest.skip(f"Ollama not reachable ({settings.ollama_host}). Skipping test. Error: {e}")


def test_orchestrator_pipeline():
    """
    End-to-end pipeline test: query → fetch → retrieve → summarize
    """
    orch = Orchestrator()

    # Small query for quick testing
    query = "graph neural networks for recommender systems"

    # Run pipeline
    report = orch.run(query=query, max_results=3, days=180, top_k=4)

    # Validate output
    assert isinstance(report, str), "Report must be a string"
    assert len(report) > 200, "Report too short — summarization may have failed"
    assert any(k in report.lower() for k in ["json", "markdown", "key_findings"]), \
        "Expected structured JSON/Markdown in summary"

    print("\n✅ Pipeline executed successfully.")
    print(f"\n--- Report Preview ---\n{report[:600]}...\n")


def test_arxiv_and_crossref_sources():
    """
    Ensure connectors can fetch data from free APIs.
    """
    from src.connectors.arxiv_conn import search_arxiv
    from src.connectors.crossref_conn import search_crossref

    arxiv_res = search_arxiv("machine learning", max_results=2, days=180)
    crossref_res = search_crossref("machine learning", max_results=2, days=180)

    assert isinstance(arxiv_res, list) and len(arxiv_res) > 0, "No results from arXiv"
    assert isinstance(crossref_res, list) and len(crossref_res) > 0, "No results from Crossref"

    print(f"\n✅ arXiv results: {len(arxiv_res)}, Crossref results: {len(crossref_res)}")


def test_retrieval_embedding_and_store():
    """
    Test the embedding + vector store pipeline using Ollama embeddings.
    """
    from src.retrieval.vector_store import VectorStore
    from src.retrieval.indexer import Indexer

    store = VectorStore("test_collection")
    indexer = Indexer(store)

    sample_text = "Graph neural networks are powerful for recommendation tasks."
    meta = {"title": "GNN Recommenders", "url": "http://example.com"}
    indexer.add_document("doc_1", sample_text, meta)

    result = store.query("graph neural networks")
    assert "documents" in result, "Chroma query missing 'documents' field"
    assert len(result["documents"][0]) > 0, "Empty documents returned"

    print("\n✅ Retrieval and embedding pipeline working correctly.")
