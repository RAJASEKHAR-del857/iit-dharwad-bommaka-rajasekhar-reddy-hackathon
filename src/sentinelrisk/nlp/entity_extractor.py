import re

COMPANY_ALIASES = {
    "Apple": ["apple", "aapl"],
    "Microsoft": ["microsoft", "msft"],
    "NVIDIA": ["nvidia", "nvda"],
    "JPMorgan": ["jpmorgan", "jpm"],
    "Bank of America": ["bank of america", "bac"],
    "Tesla": ["tesla", "tsla"],
    "Amazon": ["amazon", "amzn"],
    "Alphabet": ["alphabet", "google", "googl"],
    "Reliance Industries": ["reliance industries", "reliance"],
    "HDFC Bank": ["hdfc bank", "hdfcbank"],
    "Infosys": ["infosys"],
    "Tata Consultancy Services": ["tcs", "tata consultancy services"],
    "Example Corp": ["example corp"]
}
SECTORS = {
    "technology": ["software", "semiconductor", "cloud", "technology", "chip", "ai"],
    "financials": ["bank", "lender", "credit", "loan", "financial", "bond"],
    "energy": ["oil", "gas", "energy", "crude"],
    "healthcare": ["drug", "pharma", "hospital", "healthcare", "clinical"],
    "consumer": ["retail", "consumer", "sales", "product", "automotive", "car"],
    "industrials": ["manufacturing", "industrial", "shipping", "supply chain"]
}

def extract_entities(text: str, hint: str = "") -> list[str]:
    lower = text.lower()
    found = []
    if hint:
        found.extend([part.strip() for part in str(hint).split(";") if part.strip()])
    for canonical, aliases in COMPANY_ALIASES.items():
        if any(re.search(r"\b" + re.escape(alias) + r"\b", lower) for alias in aliases):
            if canonical not in found:
                found.append(canonical)
    return found

def extract_sectors(text: str) -> list[str]:
    lower = text.lower()
    return [sector for sector, terms in SECTORS.items() if any(term in lower for term in terms)]
