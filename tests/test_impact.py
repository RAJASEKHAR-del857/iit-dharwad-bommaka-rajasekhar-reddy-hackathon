from sentinelrisk.pipeline import analyze_record

def test_signal_has_required_fields():
    signal = analyze_record({
        "text": "NVIDIA reports strong profit growth after beating revenue expectations.",
        "source_type": "financial_news",
        "source_name": "test",
        "is_synthetic": True
    }, use_finbert=False)
    assert -1 <= signal.sentiment_score <= 1
    assert 1 <= signal.impact_score <= 10
    assert signal.event_type in {"geopolitical","macroeconomic","credit_event","merger_acquisition","product_launch","regulatory_legal","earnings_business","other"}
    assert signal.entities
