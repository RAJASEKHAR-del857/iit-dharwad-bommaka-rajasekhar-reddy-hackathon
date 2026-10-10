from datetime import datetime, timezone
from .ingestion.normalize import stable_id
from .nlp.sentiment import analyze_sentiment
from .nlp.event_classifier import classify_event
from .nlp.entity_extractor import extract_entities, extract_sectors
from .nlp.impact_scorer import score_impact
from .schemas import RiskSignal

def analyze_record(record: dict, use_finbert: bool | None = None) -> RiskSignal:
    text = str(record.get("text", "")).strip()
    if not text:
        raise ValueError("Cannot analyze empty text")
    sentiment = analyze_sentiment(text, use_finbert=use_finbert)
    event_type, event_reasons = classify_event(text)
    entities = extract_entities(text, record.get("entities_hint", ""))
    sectors = extract_sectors(text)
    impact, impact_reasons = score_impact(event_type, sentiment["score"], entities, sectors, text)
    timestamp = record.get("timestamp") or datetime.now(timezone.utc)
    if isinstance(timestamp, str):
        from .ingestion.normalize import parse_timestamp
        timestamp = parse_timestamp(timestamp)
    return RiskSignal(
        signal_id=stable_id(record.get("source_type", "manual"), text),
        source_type=record.get("source_type", "manual"),
        source_name=record.get("source_name", "Manual input"),
        timestamp=timestamp,
        text=text,
        entities=entities,
        sentiment_label=sentiment["label"],
        sentiment_score=sentiment["score"],
        sentiment_confidence=sentiment["confidence"],
        event_type=event_type,
        impact_score=impact,
        impact_reasons=event_reasons + impact_reasons,
        affected_sectors=sectors,
        model_used=sentiment["model"],
        is_synthetic=bool(record.get("is_synthetic", True))
    )

def analyze_records(records: list[dict], use_finbert: bool | None = None) -> list[RiskSignal]:
    seen = set()
    output = []
    for record in records:
        text = str(record.get("text", "")).strip()
        key = (record.get("source_type", "manual"), " ".join(text.lower().split()))
        if not text or key in seen:
            continue
        seen.add(key)
        output.append(analyze_record(record, use_finbert=use_finbert))
    return output
