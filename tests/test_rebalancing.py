import pandas as pd
from sentinelrisk.config import DATA_DIR
from sentinelrisk.rebalancing.index_rebalancer import rebalance_index

def test_weights_sum_to_one_and_respect_bounds():
    index_df = pd.read_csv(DATA_DIR / "synthetic_index.csv")
    signals = [
        {"sentiment_score": 0.8, "entities": ["NVIDIA"]},
        {"sentiment_score": -0.8, "entities": ["Tesla"]}
    ]
    result = rebalance_index(index_df, signals, min_weight=0.02, max_weight=0.20)
    assert abs(result.new_weight.sum() - 1.0) < 1e-8
    assert (result.new_weight >= 0.02 - 1e-8).all()
    assert (result.new_weight <= 0.20 + 1e-8).all()
