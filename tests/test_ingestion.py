from pathlib import Path
from sentinelrisk.ingestion.csv_source import load_csv_records
from sentinelrisk.config import DATA_DIR

def test_bundled_sources_load():
    news = load_csv_records(DATA_DIR / "sample_news.csv", "financial_news")
    social = load_csv_records(DATA_DIR / "sample_social_posts.csv", "social_post")
    assert len(news) >= 5
    assert len(social) >= 3
    assert all(r["text"].strip() for r in news + social)
