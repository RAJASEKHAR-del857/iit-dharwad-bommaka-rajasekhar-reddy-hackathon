import re

RULES = {
    "geopolitical": ["war", "invasion", "geopolitical", "sanction", "sanctions", "military", "conflict", "attack", "tariff"],
    "macroeconomic": ["inflation", "interest rate", "central bank", "gdp", "recession", "unemployment", "currency", "rate hike"],
    "credit_event": ["default", "credit loss", "bad loan", "non-performing", "bankruptcy", "debt restructuring", "downgrade", "liquidity crisis"],
    "merger_acquisition": ["merger", "acquisition", "acquire", "takeover", "buyout", "bids for", "to buy"],
    "product_launch": ["product launch", "launches a new", "unveils", "new product", "rolls out"],
    "regulatory_legal": ["regulator", "regulatory", "lawsuit", "investigation", "fine", "penalty", "court", "antitrust", "compliance"],
    "earnings_business": ["quarterly earnings", "revenue", "profit", "loss", "guidance", "earnings", "sales", "layoffs", "results"]
}

SEVERITY = {
    "geopolitical": 8, "macroeconomic": 7, "credit_event": 9,
    "merger_acquisition": 5, "product_launch": 3, "regulatory_legal": 7,
    "earnings_business": 5, "other": 3
}

def classify_event(text: str) -> tuple[str, list[str]]:
    lower = re.sub(r"\s+", " ", text.lower())
    scores = {}
    for event, terms in RULES.items():
        scores[event] = sum(1 for term in terms if term in lower)
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "other", ["No event keyword matched; classified as other"]
    matched = [term for term in RULES[best] if term in lower]
    return best, [f"Matched event terms: {', '.join(matched[:4])}"]

def base_severity(event_type: str) -> int:
    return SEVERITY.get(event_type, SEVERITY["other"])
