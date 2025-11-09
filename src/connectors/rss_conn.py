import feedparser
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.utils.logging import info, warn


def fetch_rss_feed(feed_url: str, days: int = 30, max_items: int = 20) -> List[Dict[str, Any]]:
    """
    Fetch recent items from an RSS feed.

    Args:
        feed_url (str): RSS feed URL.
        days (int): Only include posts within the last N days.
        max_items (int): Maximum number of results to return.

    Returns:
        List[Dict[str, Any]]: Each dict includes:
            {
                "id": str,
                "title": str,
                "url": str,
                "published": str,
                "summary": str,
                "source": "rss"
            }
    """
    info(f"Fetching RSS feed: {feed_url}")
    feed = feedparser.parse(feed_url)
    if feed.bozo:
        warn(f"RSS feed parse error: {feed.bozo_exception}")
        return []

    cutoff = datetime.utcnow() - timedelta(days=days)
    items = []

    for entry in feed.entries[:max_items]:
        try:
            published = None
            if hasattr(entry, "published_parsed"):
                published = datetime(*entry.published_parsed[:6]).isoformat()
                if datetime(*entry.published_parsed[:6]) < cutoff:
                    continue
            items.append({
                "id": entry.get("id", entry.get("link")),
                "title": entry.get("title", "Untitled"),
                "url": entry.get("link", ""),
                "published": published,
                "summary": entry.get("summary", ""),
                "source": "rss"
            })
        except Exception as e:
            warn(f"Skipping malformed RSS entry: {e}")

    info(f"RSS fetched {len(items)} valid items.")
    return items
