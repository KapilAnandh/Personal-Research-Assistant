from typing import List, Dict
from src.connectors.arxiv_conn import search_arxiv
from src.connectors.crossref_conn import search_crossref
from src.connectors.rss_conn import fetch_rss_feed
from src.connectors.web_scraper import fetch_and_extract
from src.retrieval.indexer import Indexer
from src.utils.logging import info, warn


class ResearcherAgent:
    """
    The Researcher Agent collects research materials from multiple sources
    (arXiv, Crossref, RSS) and indexes them into the vector store.
    """

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    def harvest(
        self,
        query: str,
        max_results: int = 20,
        days: int = 365,
        rss_feeds: List[str] | None = None
    ) -> List[Dict]:
        info(f"Harvesting data for query: '{query}'")

        arxiv_results = search_arxiv(query, max_results=max_results, days=days)
        crossref_results = search_crossref(query, max_results=max_results, days=days)

        rss_results = []
        if rss_feeds:
            for feed in rss_feeds:
                rss_results.extend(fetch_rss_feed(feed, days=days, max_items=max_results))

        combined = arxiv_results + crossref_results + rss_results
        info(f"Total combined results before dedup: {len(combined)}")

        # Deduplicate by URL or ID
        seen = set()
        deduped = []
        for item in combined:
            key = item.get("url") or item.get("id")
            if key and key not in seen:
                seen.add(key)
                deduped.append(item)

        info(f"Deduplicated total: {len(deduped)}")
        return deduped

    def ingest(self, items: List[Dict]):
        """
        For each research item, fetches its summary or scrapes text,
        and indexes into ChromaDB.
        """
        for it in items:
            text = it.get("summary", "")
            url = it.get("url")
            if url and (not text or len(text) < 500):
                try:
                    scraped, path = fetch_and_extract(url)
                    if scraped and len(scraped) > len(text):
                        text = scraped
                except Exception as e:
                    warn(f"Failed scraping {url}: {e}")

            if not text:
                continue

            doc_id = (it.get("id") or it.get("url") or it.get("title"))[:128]
            meta = {
                "title": it.get("title"),
                "url": it.get("url"),
                "pdf_url": it.get("pdf_url"),
                "published": it.get("published"),
                "source": it.get("source"),
                "type": it.get("type"),
            }
            self.indexer.add_document(doc_id, text, meta)
        info("Ingestion completed.")