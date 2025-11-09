import arxiv
from datetime import datetime, timedelta


# Returns list of {id, title, url, pdf_url, published, summary, authors}
def search_arxiv(query: str, max_results: int = 20, days: int = 365):
    after = datetime.utcnow() - timedelta(days=days)
    results = []

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    for r in search.results():
        if r.published.replace(tzinfo=None) < after:
            continue

        results.append({
            "id": r.entry_id,
            "title": r.title,
            "url": r.entry_id,
            "pdf_url": r.pdf_url,
            "published": r.published.isoformat(),
            "summary": r.summary,
            "authors": [a.name for a in r.authors],
        })

    return results