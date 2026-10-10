import pandas as pd

def rebalance_index(index_df: pd.DataFrame, signals: list[dict], alpha: float = 0.35,
                    min_weight: float = 0.02, max_weight: float = 0.20) -> pd.DataFrame:
    if index_df.empty:
        raise ValueError("Index constituents cannot be empty")
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between 0 and 1")
    if min_weight < 0 or max_weight <= 0 or min_weight > max_weight:
        raise ValueError("Invalid weight bounds")
    if len(index_df) * min_weight > 1 + 1e-9 or len(index_df) * max_weight < 1 - 1e-9:
        raise ValueError("Weight bounds cannot sum to 100% for this number of constituents")
    df = index_df.copy()
    if "ticker" not in df or "weight" not in df:
        raise ValueError("Index must contain ticker and weight columns")
    if (df["weight"] < 0).any() or df["weight"].sum() <= 0:
        raise ValueError("Starting weights must be non-negative with a positive sum")
    sentiment_map = {}
    for signal in signals:
        score = float(signal.get("sentiment_score", 0.0))
        for entity in signal.get("entities", []):
            sentiment_map[entity.lower()] = score
    df["sentiment_score"] = df.apply(
        lambda row: sentiment_map.get(str(row.get("company", row["ticker"])).lower(),
                                      sentiment_map.get(str(row["ticker"]).lower(), 0.0)), axis=1)
    base = df["weight"].astype(float) / df["weight"].sum()
    raw = (base * (1.0 + alpha * df["sentiment_score"])).clip(lower=1e-12).tolist()
    # Project onto bounded simplex using iterative proportional adjustment and clipping.
    raw = [x / sum(raw) for x in raw]
    weights = raw
    for _ in range(1000):
        clipped = [min(max_weight, max(min_weight, w)) for w in weights]
        diff = 1.0 - sum(clipped)
        if abs(diff) < 1e-10:
            weights = clipped
            break
        free = [i for i, w in enumerate(clipped) if min_weight + 1e-12 < w < max_weight - 1e-12]
        if not free:
            free = [i for i, w in enumerate(clipped) if (diff > 0 and w < max_weight) or (diff < 0 and w > min_weight)]
        if not free:
            raise ValueError("Unable to normalize weights under provided bounds")
        denom = sum(max(weights[i], 1e-12) for i in free)
        for i in free:
            clipped[i] += diff * max(weights[i], 1e-12) / denom
        weights = clipped
    else:
        raise ValueError("Weight normalization did not converge")
    df["old_weight"] = base
    df["new_weight"] = weights
    df["weight_change"] = df["new_weight"] - df["old_weight"]
    df["estimated_turnover_contribution"] = df["weight_change"].abs() / 2.0
    return df
