# Demo Script

## Five-minute live demo
1. **0:00–0:30 — Overview:** Explain the problem: converting text into actionable, explainable risk signals.
2. **0:30–1:15 — Ingest:** Open Risk Intelligence and load bundled news and social-style examples. Explain that examples are synthetic and RSS is an optional live source.
3. **1:15–2:00 — Analyze:** Enter a headline about credit losses or geopolitical escalation. Show sentiment, event category, impact score, entities, and reasons.
4. **2:00–3:15 — Stress test:** Open Portfolio Stress Test, select a high-impact event, and show before/after portfolio values and position-level loss contributions.
5. **3:15–4:00 — Rebalance:** Open Index Rebalancer and show weight changes and the 100% total-weight invariant.
6. **4:00–4:40 — Evidence:** Run `python -m pytest -q` and show the evaluation outputs.
7. **4:40–5:00 — Limitations:** Explain that synthetic scenario shocks are not predictions and that a production system needs validated calibration and richer exposure data.

## Longer recording
Add the README quickstart, API `/docs`, output CSV/JSON files, methodology, test results, and known limitations. Do not claim a live social-media API or production-grade financial predictions.
