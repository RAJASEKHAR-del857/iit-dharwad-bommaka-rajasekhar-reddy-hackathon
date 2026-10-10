import pandas as pd
from .scenario_engine import SCENARIOS

def run_stress_test(portfolio: pd.DataFrame, event_type: str, impact_score: int, threshold: int = 7) -> dict:
    if not 1 <= int(impact_score) <= 10:
        raise ValueError("impact_score must be between 1 and 10")
    before = float(portfolio["market_value"].sum())
    if int(impact_score) < int(threshold):
        return {
            "triggered": False, "event_type": event_type, "impact_score": int(impact_score),
            "threshold": int(threshold), "portfolio_before": before, "portfolio_after": before,
            "total_loss": 0.0, "loss_pct": 0.0, "scenario_name": "No stress triggered",
            "description": f"Impact score {impact_score} is below threshold {threshold}.",
            "positions": portfolio.assign(stress_return=0.0, value_after=portfolio["market_value"], loss=0.0)
        }
    scenario = SCENARIOS.get(event_type, SCENARIOS["other"])
    df = portfolio.copy()
    returns = []
    for _, row in df.iterrows():
        asset_type = str(row["asset_type"]).lower()
        sector = str(row["sector"]).lower()
        shock = 0.0
        if asset_type in ("equity", "stock"):
            shock += scenario["equity_shock"] * float(row.get("equity_beta", 1.0))
        elif asset_type in ("bond", "loan", "corporate_bond", "government_bond"):
            rate_change = scenario["rate_shock_bps"] / 10000.0
            spread_change = scenario["credit_spread_shock_bps"] / 10000.0
            duration = float(row.get("duration", 0.0))
            # First-order duration approximation; spread sensitivity is an explicit simplified proxy.
            shock += -duration * (rate_change + spread_change * float(row.get("credit_spread_sensitivity", 1.0)))
        elif asset_type == "derivative":
            shock += scenario["equity_shock"] * float(row.get("equity_beta", 1.0))
        if "energy" in sector and event_type == "geopolitical":
            shock -= 0.02
        # Keep simplified scenario returns bounded to avoid absurd values from input data.
        returns.append(max(-0.95, min(0.50, shock)))
    df["stress_return"] = returns
    df["value_after"] = df["market_value"].astype(float) * (1.0 + df["stress_return"])
    df["loss"] = df["market_value"].astype(float) - df["value_after"]
    after = float(df["value_after"].sum())
    loss = before - after
    return {
        "triggered": True, "event_type": event_type, "impact_score": int(impact_score),
        "threshold": int(threshold), "portfolio_before": before, "portfolio_after": after,
        "total_loss": loss, "loss_pct": (loss / before * 100.0) if before else 0.0,
        "scenario_name": scenario["name"], "description": scenario["description"],
        "positions": df
    }
