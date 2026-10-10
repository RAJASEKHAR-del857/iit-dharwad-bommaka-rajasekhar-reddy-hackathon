# Jury Q&A Preparation

**Why a hybrid NLP approach?** FinBERT can improve financial-domain sentiment when available, while a deterministic fallback keeps the demo reproducible and offline-capable. The fallback is a baseline, not equivalent to FinBERT.

**How is impact score calculated?** It is a documented heuristic based on event severity, sentiment magnitude, relevance, and a novelty proxy. It is not a calibrated probability of loss.

**How do you prevent duplicate headlines inflating risk?** The pipeline deduplicates normalized text within a source type using a stable key. Production use should also cluster near-duplicates across sources.

**How does a text signal become a portfolio loss?** The event category selects a documented scenario; each position's type and sensitivities determine a simplified shock. The engine reports the assumptions and position-level contribution.

**Why synthetic data?** It avoids confidential data, makes the demo reproducible, and lets the evaluator inspect every input. The trade-off is that results do not establish real-world predictive power.

**What would you improve next?** Build a human-labelled dataset, evaluate per-class macro-F1, calibrate impact against documented outcomes, use a validated event-to-entity knowledge graph, add realistic instrument valuation, and backtest the rebalancer with transaction costs.

**Is it investment advice?** No. It is a research prototype demonstrating event intelligence and hypothetical scenarios.
