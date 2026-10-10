from datetime import datetime, timezone
import feedparser
import requests
from .normalize import normalize_text, parse_timestamp

DEFAULT_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.cnbc.com/id/10001147/device/rss/rss.html",
]

def fetch_rss_records(feed_urls=None, timeout: int = 5, max_items: int = 20) -> list[dict]:
    """Fetch public RSS headlines. Network errors are isolated per feed."""
    records = []
    for url in (feed_urls or DEFAULT_FEEDS):
        try:
            response = requests.get(url, timeout=timeout, headers={"User-Agent": "SentinelRiskAI/1.0"})
            response.raise_for_status()
            parsed = feedparser.parse(response.content)
            for entry in parsed.entries[:max_items]:
                title = normalize_text(entry.get("title", ""))
                summary = normalize_text(entry.get("summary", ""))
                text = normalize_text(f"{title}. {summary}" if summary else title)
                if not text:
                    continue
                published = entry.get("published_parsed") or entry.get("updated_parsed")
                timestamp = datetime(*published[:6], tzinfo=timezone.utc) if published else datetime.now(timezone.utc)
                records.append({
                    "source_type": "financial_news",
                    "source_name": parsed.feed.get("title", url),
                    "timestamp": timestamp,
                    "text": text,
                    "entities_hint": "",
                    "is_synthetic": False,
                    "source_url": entry.get("link", url)
                })
        except Exception:
            # One inaccessible feed must not prevent other feeds or offline demo.
            continue
    return records
