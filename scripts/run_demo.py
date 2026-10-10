from pathlib import Path
import json
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sentinelrisk.config import DATA_DIR, RESULTS_DIR
from sentinelrisk.ingestion.csv_source import load_csv_records
from sentinelrisk.pipeline import analyze_records
from sentinelrisk.portfolio.portfolio_loader import load_portfolio
from sentinelrisk.portfolio.stress_tester import run_stress_test
from sentinelrisk.rebalancing.index_rebalancer import rebalance_index
from sentinelrisk.storage.repository import SignalRepository

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    records = load_csv_records(DATA_DIR / "sample_news.csv", "financial_news")
    records += load_csv_records(DATA_DIR / "sample_social_posts.csv", "social_post")
    signals = analyze_records(records, use_finbert=False)
    repo = SignalRepository(RESULTS_DIR / "sentinelrisk.db")
    repo.save_many(signals)
    signal_dicts = [s.model_dump(mode="json") for s in signals]
    (RESULTS_DIR / "risk_signals.json").write_text(json.dumps(signal_dicts, indent=2), encoding="utf-8")
    pd.DataFrame(signal_dicts).to_csv(RESULTS_DIR / "risk_signals.csv", index=False)

    portfolio = load_portfolio(DATA_DIR / "synthetic_portfolio.csv")
    high_impact = max(signals, key=lambda s: s.impact_score)
    stress = run_stress_test(portfolio, high_impact.event_type, high_impact.impact_score, threshold=7)
    stress_positions = stress.pop("positions")
    stress_positions.to_csv(RESULTS_DIR / "stress_test_positions.csv", index=False)
    stress_summary = {k: v for k, v in stress.items()}
    (RESULTS_DIR / "stress_test_summary.json").write_text(json.dumps(stress_summary, indent=2), encoding="utf-8")

    index_df = pd.read_csv(DATA_DIR / "synthetic_index.csv")
    rebalance = rebalance_index(index_df, signal_dicts)
    rebalance.to_csv(RESULTS_DIR / "rebalanced_index.csv", index=False)

    print("SentinelRisk AI demo completed.")
    print(f"Unique risk signals: {len(signals)}")
    print(f"Highest impact event: {high_impact.event_type} ({high_impact.impact_score}/10)")
    print(f"Stress test triggered: {stress['triggered']}")
    print(f"Portfolio before: {stress['portfolio_before']:.2f}")
    print(f"Portfolio after:  {stress['portfolio_after']:.2f}")
    print(f"New index weights sum: {rebalance['new_weight'].sum():.6f}")
    print(f"Outputs written to: {RESULTS_DIR}")

if __name__ == "__main__":
    main()
