from pathlib import Path
import pandas as pd
from .normalize import normalize_text, parse_timestamp

def load_csv_records(path: str | Path, source_type: str, source_name: str | None = None) -> list[dict]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input dataset not found: {path}")
    df = pd.read_csv(path).fillna("")
    if "text" not in df.columns:
        raise ValueError(f"{path} must contain a 'text' column")
    records = []
    for _, row in df.iterrows():
        text = normalize_text(str(row.get("text", "")))
        if not text:
            continue
        records.append({
            "source_type": source_type,
            "source_name": str(row.get("source_name") or source_name or source_type),
            "timestamp": parse_timestamp(row.get("timestamp")),
            "text": text,
            "entities_hint": str(row.get("entities", "")),
            "is_synthetic": str(row.get("is_synthetic", "true")).lower() not in ("false", "0", "no")
        })
    return records
