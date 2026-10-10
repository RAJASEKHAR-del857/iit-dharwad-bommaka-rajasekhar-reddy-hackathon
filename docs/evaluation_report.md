# Evaluation Report — SentinelRisk AI

## Run configuration
- Engine: offline lexicon sentiment + deterministic event taxonomy
- Evaluation data: `data/labelled_eval.csv`
- Records: 16 synthetic, manually labelled examples
- Purpose: reproducible smoke-check of the pipeline, not a statistically meaningful benchmark

## Measured results
- Offline sentiment accuracy: **0.750**
- Offline sentiment macro-F1: **0.730**
- Event classification accuracy: **0.938**
- Event classification macro-F1: **0.933**

These numbers were produced by running `python scripts/evaluate.py` in the generated project environment on the included 16-record synthetic dataset. The set is very small, synthetic, and not independent of the hand-authored keyword taxonomy. Do not present these metrics as evidence of real-world model quality. A proper evaluation needs a larger, independently labelled and representative holdout set.

## End-to-end demo smoke test
- Unique risk signals processed: **18**
- Highest-impact sample event: **geopolitical, 7/10**
- Portfolio stress test: **triggered**
- Synthetic portfolio before stress: **100.00**
- Synthetic portfolio after stress: **91.09**
- Rebalanced index weights sum: **1.000000**

All portfolio values are synthetic units (the dashboard labels them as millions for display); they are not actual assets or market data.

## Reproduce
```powershell
python scripts/evaluate.py
python scripts/run_demo.py
python -m pytest -q
```
