import re, requests
from bs4 import BeautifulSoup

def fetch_url_text(url: str) -> str:
    """Very simple article text fetcher (good enough for v1)."""
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        # Drop script/style
        for tag in soup(["script","style","noscript"]): tag.decompose()
        # Heuristic: main article text
        candidates = [soup.find('article'), soup.find('main'), soup.body]
        text = " ".join([c.get_text(" ", strip=True) for c in candidates if c])
        return clean_text(text)
    except Exception:
        return ""

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text