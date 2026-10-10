from sentinelrisk.config import DATA_DIR
from sentinelrisk.portfolio.portfolio_loader import load_portfolio
from sentinelrisk.portfolio.stress_tester import run_stress_test

def test_high_impact_stress_reconciles():
    portfolio = load_portfolio(DATA_DIR / "synthetic_portfolio.csv")
    result = run_stress_test(portfolio, "geopolitical", 9, threshold=7)
    assert result["triggered"]
    assert abs(result["portfolio_before"] - float(portfolio.market_value.sum())) < 1e-8
    assert abs(result["portfolio_after"] - float(result["positions"].value_after.sum())) < 1e-8
    assert abs(result["total_loss"] - float(result["positions"].loss.sum())) < 1e-8

def test_below_threshold_does_not_trigger():
    portfolio = load_portfolio(DATA_DIR / "synthetic_portfolio.csv")
    result = run_stress_test(portfolio, "geopolitical", 3, threshold=7)
    assert not result["triggered"]
    assert result["total_loss"] == 0
