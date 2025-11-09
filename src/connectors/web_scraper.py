import requests
import trafilatura
from pathlib import Path
from typing import Tuple
from src.utils.config import settings
from src.utils.logging import info, warn, error

CACHE_DIR = Path(settings.cache_dir)
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def fetch_and_extract(url: str) -> Tuple[str, str]:
    """
    Downloads and extracts readable text content from a webpage.

    Args:
        url (str): Web page URL.

    Returns:
        Tuple[str, str]: (cleaned_text, saved_file_path)
    """
    try:
        fname = (url.replace("://", "_").replace("/", "_").replace("?", "_")[:150]) + ".html"
        fpath = CACHE_DIR / fname

        if not fpath.exists():
            info(f"Downloading {url}")
            resp = requests.get(url, timeout=60, headers={"User-Agent": "research-assistant/1.0"})
            resp.raise_for_status()
            fpath.write_bytes(resp.content)

        # Compatible with all modern trafilatura versions
        text = trafilatura.extract_file(str(fpath), include_comments=False, include_tables=False) or ""
        if not text:
            warn(f"No text extracted from {url}")
        return text.strip(), str(fpath)
    except Exception as e:
        error(f"Web scrape failed for {url}: {e}")
        return "", ""