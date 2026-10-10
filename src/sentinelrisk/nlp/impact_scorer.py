from .event_classifier import base_severity

def score_impact(event_type: str, sentiment_score: float, entities: list[str], sectors: list[str], text: str) -> tuple[int, list[str]]:
    severity = base_severity(event_type)
    sentiment_magnitude = 1 + 9 * min(1.0, abs(float(sentiment_score)))
    relevance = 7 if entities or sectors else 4
    novelty = 6 if any(word in text.lower() for word in ("unexpected", "emergency", "record", "first-ever", "halted")) else 4
    score = round(0.45 * severity + 0.25 * sentiment_magnitude + 0.20 * relevance + 0.10 * novelty)
    score = max(1, min(10, int(score)))
    reasons = [
        f"Event baseline severity: {severity}/10",
        f"Sentiment magnitude contribution: {sentiment_magnitude:.1f}/10",
        f"Portfolio/entity relevance: {relevance}/10",
        f"Novelty proxy: {novelty}/10"
    ]
    return score, reasons
