from __future__ import annotations

from typing import Optional

import requests
from bs4 import BeautifulSoup

try:
    from newspaper import Article  # type: ignore
except Exception:  # newspaper3k might not be installed at runtime
    Article = None  # type: ignore


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def extract_text_from_url(url: str) -> str:
    if Article is not None:
        try:
            art = Article(url)
            art.download()
            art.parse()
            text = (art.text or "").strip()
            if text:
                return text
        except Exception:
            pass

    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    article_candidates = [
        "article",
        "div.article-body",
        "div#main-content",
        "div.post-content",
        "div.entry-content",
    ]

    for selector in article_candidates:
        node = soup.select_one(selector)
        if node and node.get_text(strip=True):
            return node.get_text(separator="\n", strip=True)

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    return "\n".join([p for p in paragraphs if p])
