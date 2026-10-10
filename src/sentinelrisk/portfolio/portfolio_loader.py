from pathlib import Path
import pandas as pd

REQUIRED = {"asset_id", "asset_name", "asset_type", "sector", "market_value", "duration", "credit_spread_sensitivity", "equity_beta"}

def load_portfolio(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Portfolio missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Portfolio dataset is empty")
    if (df["market_value"] < 0).any():
        raise ValueError("market_value must be non-negative")
    return df
