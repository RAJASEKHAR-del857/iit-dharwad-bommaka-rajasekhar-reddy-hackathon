# SentinelRisk AI — Methodology

## Scope
This is an educational prototype that converts unstructured text into structured risk signals and demonstrates two downstream simulations. It is not a trading system or a production risk model.

## Ingestion and provenance
The prototype supports public RSS retrieval and CSV/manual text. Bundled datasets are synthetic and labelled as such. RSS is optional because network access and feed availability vary.

## Sentiment
The default is an explainable word-lexicon baseline with simple negation handling. Optional FinBERT inference is enabled with `SENTINELRISK_USE_FINBERT=1` after installing the `nlp` extra and downloading model files. If model loading fails, the code falls back to the lexicon. Lexicon output is not equivalent to a trained financial language model.

## Event classification
Event classes are selected using a transparent keyword taxonomy. It is deterministic and easy to inspect, but may miss context, sarcasm, implicit events, and unseen wording. A labelled test set is needed to assess generalization.

## Impact score
The score is a weighted heuristic combining event baseline severity, sentiment magnitude, entity/sector relevance, and a small novelty proxy. It is a prioritization score from 1 to 10, not a calibrated probability or forecast of market losses.

## Stress testing
Portfolio values and shocks are synthetic. Equities and equity-like derivatives use configured equity shocks and beta. Loans and bonds use a first-order duration approximation with configured rate and spread shocks. This omits convexity, cash flows, default probabilities, recovery, collateral, netting, option greeks, liquidity, and cross-asset dependencies.

## Index rebalancing
Weights are adjusted by aggregated sentiment and projected into configured bounds. This is a simulation, not investment advice. It does not use live prices, backtesting, or real transaction costs unless those are separately supplied.

## Responsible interpretation
Always disclose data provenance, model version, scenario assumptions, and known limitations. Do not use this prototype as the basis for real financial decisions.
