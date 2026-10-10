import hashlib
import re
from datetime import datetime, timezone

def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()

def stable_id(source_type: str, text: str) -> str:
    digest = hashlib.sha256(f"{source_type}:{normalize_text(text).lower()}".encode("utf-8")).hexdigest()[:12]
    return f"sig_{digest}"

def parse_timestamp(value):
    if not value:
        return datetime.now(timezone.utc)
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)
