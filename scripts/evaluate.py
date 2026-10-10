from pathlib import Path
import sys
import pandas as pd
from sentinelrisk.pipeline import analyze_record

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

def macro_f1(y_true, y_pred):
    labels = sorted(set(y_true) | set(y_pred))
    scores = []
    for label in labels:
        tp = sum(a == label and b == label for a, b in zip(y_true, y_pred))
        fp = sum(a != label and b == label for a, b in zip(y_true, y_pred))
        fn = sum(a == label and b != label for a, b in zip(y_true, y_pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores) if scores else 0.0

def main():
    path = ROOT / "data" / "labelled_eval.csv"
    df = pd.read_csv(path)
    predictions = [analyze_record({"text": row.text, "source_type": "evaluation", "is_synthetic": True}, use_finbert=False)
                   for row in df.itertuples()]
    expected_sent = df["expected_sentiment"].astype(str).tolist()
    pred_sent = [p.sentiment_label for p in predictions]
    expected_event = df["expected_event"].astype(str).tolist()
    pred_event = [p.event_type for p in predictions]
    sent_acc = sum(a == b for a, b in zip(expected_sent, pred_sent)) / len(df)
    event_acc = sum(a == b for a, b in zip(expected_event, pred_event)) / len(df)
    print(f"Evaluation records: {len(df)}")
    print(f"Offline sentiment accuracy: {sent_acc:.3f}")
    print(f"Offline sentiment macro-F1: {macro_f1(expected_sent, pred_sent):.3f}")
    print(f"Event classification accuracy: {event_acc:.3f}")
    print(f"Event classification macro-F1: {macro_f1(expected_event, pred_event):.3f}")
    print("WARNING: tiny synthetic evaluation set; these scores are for a reproducible demo only, not evidence of real-world performance.")
    out = pd.DataFrame([{
        "text": row.text, "expected_sentiment": row.expected_sentiment,
        "predicted_sentiment": pred.sentiment_label, "expected_event": row.expected_event,
        "predicted_event": pred.event_type, "impact_score": pred.impact_score
    } for row, pred in zip(df.itertuples(), predictions)])
    results = ROOT / "results"
    results.mkdir(exist_ok=True)
    out.to_csv(results / "evaluation_predictions.csv", index=False)

if __name__ == "__main__":
    main()
