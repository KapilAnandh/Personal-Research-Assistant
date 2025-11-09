from src.retrieval.vector_store import VectorStore
from src.retrieval.indexer import Indexer
from src.agents.researcher import ResearcherAgent
from src.agents.summarizer import SummarizerAgent
from src.utils.logging import info


class Orchestrator:
    """
    Main pipeline orchestrator for the Personal Research Assistant Agent.
    """

    def __init__(self):
        self.store = VectorStore("papers")
        self.indexer = Indexer(self.store)
        self.researcher = ResearcherAgent(self.indexer)
        self.summarizer = SummarizerAgent()

    def run(
        self,
        query: str,
        max_results: int = 20,
        days: int = 365,
        top_k: int = 10,
        rss_feeds: list[str] | None = None
    ) -> str:
        """
        Executes the end-to-end pipeline:
        1. Fetches sources
        2. Indexes into Chroma
        3. Retrieves top-k relevant chunks
        4. Summarizes using LLM
        """
        info(f"Running pipeline for: {query}")

        items = self.researcher.harvest(query, max_results=max_results, days=days, rss_feeds=rss_feeds)
        self.researcher.ingest(items)

        info("Performing similarity retrieval...")
        hits = self.indexer.search(query, k=top_k)

        info("Summarizing results...")
        report = self.summarizer.summarize(query, hits)
        info("Pipeline completed.")
        return report