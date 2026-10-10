# SentinelRisk AI — S&P Global & Crisil Campus Hackathon 2026

**Candidate:** Bommaka Rajasekhar Reddy  
**College email:** cs23bt065@iitdh.ac.in  
**College / campus:** IIT Dharwad  
**Project:** Explainable Financial Event Intelligence and Portfolio Risk Simulation  
**Demo video:** Add the public/unlisted video URL after recording.  
**Presentation:** [PDF](docs/presentation.pdf) and [PowerPoint](docs/presentation.pptx)

> **Important:** This is an educational prototype. All bundled portfolio holdings and example text are synthetic. Stress scenarios are illustrative and are not financial forecasts or investment advice.

## 1. Problem and approach

Financial news and social text are unstructured, fast-moving, and difficult to connect directly to portfolio exposures. SentinelRisk AI ingests text from public RSS feeds and CSV/manual input, produces structured sentiment/event/impact signals, and exposes them through an API and dashboard.

Two downstream modules consume the same risk engine:
- **Strategic portfolio stress testing:** applies configurable event-specific hypothetical shocks to a synthetic banking portfolio and reports position-level loss contributions.
- **Tactical index rebalancing:** adjusts synthetic constituent weights using sentiment, then enforces configured weight limits and a 100% total-weight constraint.

## 2. Architecture

```text
Public RSS ─┐
CSV data ───┼─> Normalize/deduplicate -> Sentiment -> Event classifier
Manual text ┘                                  |
                                               v
                                 Explainable impact score
                                               |
                                     Validated risk signal
                                               |
                                  SQLite + FastAPI + Streamlit
                                     /                   \
                          Portfolio stress test     Index rebalancer
```

See `docs/architecture.png` for the diagram and `docs/methodology.md` for formulas and assumptions.

## 3. Features

- Sentiment score in `[-1, 1]`, label, and confidence.
- Event taxonomy: geopolitical, macroeconomic, credit event, M&A, product launch, regulatory/legal, earnings/business, other.
- Explainable impact score from 1 to 10.
- Entity and sector hints.
- Deduplication, provenance, JSON/CSV exports, SQLite persistence.
- Public RSS ingestion with network-failure handling.
- Synthetic portfolio stress testing and bounded index rebalancing.
- FastAPI endpoints and interactive Streamlit dashboard.
- Automated tests for core behavior and financial invariants.
- Offline-first demo that needs no API key or pretrained-model download.

## 4. Requirements

- Windows 10/11, PowerShell
- Python 3.11 recommended (Python 3.10+ supported)
- Internet is only needed to install dependencies or fetch public RSS feeds.
- No API credentials are required.

## 5. Quickstart — Windows PowerShell

Open PowerShell in the repository folder.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

If PowerShell blocks activation, run this in the current terminal, then activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Run the end-to-end offline demo

```powershell
python scripts/run_demo.py
```

Expected behavior: it prints the number of analyzed records, the highest-impact event, the stress-test outcome, the new index weight sum, and writes files under `results/`:
- `risk_signals.json`
- `risk_signals.csv`
- `stress_test_summary.json`
- `stress_test_positions.csv`
- `rebalanced_index.csv`
- `sentinelrisk.db`

The exact scores depend on the code and sample dataset. The index weight sum should be approximately `1.000000`.

### Launch the dashboard

```powershell
python -m streamlit run app/dashboard.py
```

Streamlit prints a local URL, normally `http://localhost:8501`. Open it in your browser. Use the sidebar to switch between risk intelligence, portfolio stress testing, index rebalancing, and methodology.

### Launch the API

Open a **second PowerShell terminal**, activate the virtual environment, and run:

```powershell
python -m uvicorn app.api:app --reload
```

- Health: `http://127.0.0.1:8000/health`
- Interactive API docs: `http://127.0.0.1:8000/docs`
- Sample signals: `http://127.0.0.1:8000/demo/analyze-samples`

Example request in PowerShell:

```powershell
$body = @{
  text = "NVIDIA reports strong revenue growth after beating expectations."
  source_type = "financial_news"
  source_name = "manual test"
  is_synthetic = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/analyze" -Method Post -ContentType "application/json" -Body $body
```

### Evaluate the bundled labelled examples

```powershell
python scripts/evaluate.py
```

This writes `results/evaluation_predictions.csv`. The bundled set is intentionally small and synthetic; its metrics are only a reproducible smoke-check.

### Run automated tests

```powershell
python -m pytest -q
```

### Optional FinBERT model

The default demo uses the lightweight offline sentiment baseline. To enable FinBERT, install the optional NLP dependencies and allow a one-time model download:

```powershell
pip install -e ".[nlp]"
$env:SENTINELRISK_USE_FINBERT = "1"
python scripts/run_demo.py
```

If the model cannot be downloaded or loaded, the sentiment module falls back to the offline baseline. First model load can be slow; for a time-limited demo, keep the default offline setting.

## 6. Data and assumptions

- `data/sample_news.csv` and `data/sample_social_posts.csv`: synthetic examples for reproducible tests and demo.
- `data/synthetic_portfolio.csv`: synthetic holdings and risk sensitivities.
- `data/synthetic_index.csv`: synthetic index constituents and starting weights.
- `data/scenarios.json`: illustrative scenario assumptions.
- `data/labelled_eval.csv`: small synthetic labelled set used by `python scripts/evaluate.py`; it is for reproducible demonstration only.
- RSS feeds: public internet sources, optional and subject to availability. Source URL is retained by the ingestion adapter; the demo database schema stores normalized signals, not a full raw-source archive.
- No live X/Twitter integration is included. The social source adapter uses a bundled CSV and accepts manually entered posts.

## 7. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze and persist one text item |
| GET | `/signals?limit=100` | Retrieve saved signals |
| POST | `/stress-test` | Run a scenario on the synthetic portfolio |
| GET | `/demo/analyze-samples` | Analyze bundled sample text |

## 8. Evaluation and results

Run `python scripts/run_demo.py`, `python scripts/evaluate.py`, and `python -m pytest -q`. The evaluation script reports metrics on a tiny synthetic labelled set; do not present these as evidence of real-world performance. A credible model claim requires a larger, independently labelled held-out dataset. See `docs/methodology.md` and `docs/evaluation_report.md`.

The bundled rule-based classifier and lexicon are transparent baselines. Their limitations include keyword ambiguity, negation/context handling, entity alias coverage, and limited generalization. FinBERT only replaces the sentiment component when explicitly enabled; it does not replace the event classifier or calibrate financial loss.

## 9. Financial model limitations

The portfolio and scenarios are synthetic. Bond and loan shocks use a simplified first-order duration/spread approximation. Derivatives use a beta-based proxy rather than full instrument valuation. The system does not model liquidity, collateral, default/recovery, convexity, options greeks, correlated market dynamics, or calibrated causal effects. Outputs are for demonstration and should not be used for real financial decisions.

## 10. Repository checklist before submission

- [ ] Push this repository to a **public** GitHub repository.
- [ ] Confirm a fresh Windows environment can install dependencies, run the demo, launch the dashboard/API, and pass tests.
- [ ] Inspect all data and make sure provenance and synthetic labels are clear.
- [ ] Generate/update the presentation and architecture image from the final code and actual results.
- [ ] Record the demo and replace the placeholder link above.
- [ ] Test repository and video links in a private/incognito browser.
- [ ] Ensure you can explain the impact formula, scenario shocks, evaluation, and limitations.

## 11. License

MIT. See `LICENSE`.
