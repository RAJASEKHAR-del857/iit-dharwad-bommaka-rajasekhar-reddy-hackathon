import os
import re
from functools import lru_cache

POSITIVE = {
    "beat", "beats", "growth", "grew", "profit", "profits", "surge", "surged",
    "upgrade", "upgraded", "strong", "record", "approval", "approved", "gain",
    "gains", "recovery", "recovered", "launch", "launched", "partnership",
    "exceeded", "improved", "positive", "expansion", "acquire", "acquisition"
}
NEGATIVE = {
    "loss", "losses", "decline", "declined", "drop", "dropped", "fall", "fell",
    "fraud", "default", "defaults", "bankruptcy", "lawsuit", "fine", "penalty",
    "downgrade", "downgraded", "missed", "weak", "warning", "crisis", "attack",
    "sanction", "sanctions", "recession", "layoffs", "cuts", "recall", "breach",
    "investigation", "risk", "risks", "negative", "collapse", "halted"
}
NEGATIONS = {"not", "no", "never", "without", "fails", "failed", "failure"}
NEGATORS_WINDOW = 3

def _lexicon_sentiment(text: str) -> dict:
    tokens = re.findall(r"[a-z]+", text.lower())
    if not tokens:
        return {"label": "neutral", "score": 0.0, "confidence": 0.5, "model": "offline_lexicon"}
    pos = neg = 0
    for i, token in enumerate(tokens):
        window = tokens[max(0, i-NEGATORS_WINDOW):i]
        flipped = any(t in NEGATIONS for t in window)
        if token in POSITIVE:
            if flipped: neg += 1
            else: pos += 1
        if token in NEGATIVE:
            if flipped: pos += 1
            else: neg += 1
    total = pos + neg
    if total == 0:
        return {"label": "neutral", "score": 0.0, "confidence": 0.52, "model": "offline_lexicon"}
    score = max(-1.0, min(1.0, (pos-neg) / max(2.0, total + 1.0)))
    label = "positive" if score > 0.12 else "negative" if score < -0.12 else "neutral"
    confidence = min(0.90, 0.52 + 0.12 * total + 0.10 * abs(score))
    return {"label": label, "score": round(score, 4), "confidence": round(confidence, 4), "model": "offline_lexicon"}

@lru_cache(maxsize=1)
def _load_finbert():
    from transformers import pipeline
    return pipeline("text-classification", model="ProsusAI/finbert", tokenizer="ProsusAI/finbert", top_k=None)

def analyze_sentiment(text: str, use_finbert: bool | None = None) -> dict:
    """Use FinBERT when explicitly enabled and available; always fall back safely."""
    if use_finbert is None:
        use_finbert = os.getenv("SENTINELRISK_USE_FINBERT", "0").lower() in ("1", "true", "yes")
    if use_finbert:
        try:
            outputs = _load_finbert()(text[:4000], truncation=True)
            # Transformers versions may return either a list of dicts or a list containing a list.
            if outputs and isinstance(outputs[0], list):
                outputs = outputs[0]
            probs = {str(item["label"]).lower(): float(item["score"]) for item in outputs}
            pos, neg, neu = probs.get("positive", 0.0), probs.get("negative", 0.0), probs.get("neutral", 0.0)
            score = max(-1.0, min(1.0, pos - neg))
            label = "positive" if score > 0.12 else "negative" if score < -0.12 else "neutral"
            return {"label": label, "score": round(score, 4), "confidence": round(max(pos, neg, neu), 4), "model": "ProsusAI/finbert"}
        except Exception:
            pass
    return _lexicon_sentiment(text)
