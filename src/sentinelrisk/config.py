from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
DB_PATH = RESULTS_DIR / "sentinelrisk.db"
EVENT_TYPES = [
    "geopolitical", "macroeconomic", "credit_event", "merger_acquisition",
    "product_launch", "regulatory_legal", "earnings_business", "other"
]
