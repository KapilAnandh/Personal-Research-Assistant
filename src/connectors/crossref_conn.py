import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from src.utils.logging import info, warn, error

BASE = "https://api.crossref.org/works"


def search_crossref(
    query: str,
    max_results: int = 20,
    days: int = 365
) -> List[Dict[str, Any]]:
    """
    Search recent academic works from Crossref API.

    Args:
        query (str): Research topic or keyword string.
        max_results (int): Maximum number of results to return (default=20).
        days (int): Only include works published within this number of days.

    Returns:
        List[Dict[str, Any]]: Each dict includes:
            {
              "id": str (DOI),
              "title": str,
              "url": str,
              "pdf_url": Optional[str],
              "published": Optional[str],
              "source": "crossref",
              "type": Optional[str]
            }
    """
    from_dt = (datetime.utcnow() - timedelta(days=days)).date().isoformat()
    params = {
        "query": query,
        "rows": max_results,
        "filter": f"from-pub-date:{from_dt}",
        "sort": "published",
        "order": "desc"
    }

    try:
        info(f"Fetching Crossref results for '{query}' (since {from_dt}) ...")
        r = requests.get(BASE, params=params, timeout=60)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        error(f"Crossref request failed: {e}")
        return []

    data = r.json()
    items = data.get("message", {}).get("items", [])
    out: List[Dict[str, Any]] = []

    for it in items:
        title = "; ".join(it.get("title", [])) if it.get("title") else "Untitled"
        url = it.get("URL") or ""
        pub = (
            it.get("created", {}).get("date-time")
            or it.get("published-print", {}).get("date-time")
            or it.get("published-online", {}).get("date-time")
        )
        out.append({
            "id": it.get("DOI"),
            "title": title,
            "url": url,
            "pdf_url": None, 
            "published": pub,
            "source": "crossref",
            "type": it.get("type"),
        })

    info(f"Crossref returned {len(out)} results.")
    return out


if __name__ == "__main__":
    # Example manual test
    results = search_crossref("graph neural networks", max_results=5, days=180)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']} ({r.get('published')})\n   {r['url']}\n")
