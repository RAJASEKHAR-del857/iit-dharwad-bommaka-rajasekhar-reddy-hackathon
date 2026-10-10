# SentinelRisk AI — S&P Global & Crisil Campus Hackathon 2026

**Candidate Name:** Bommaka Rajasekhar Reddy  
**College Email ID:** cs23bt065@iitdh.ac.in  
**College / Campus:** IIT Dharwad  
**Project Title:** Explainable Financial Event Intelligence and Portfolio Risk Simulation  
**Demo Video Link:**   

> **Disclaimer:** SentinelRisk AI is an educational prototype. All bundled portfolio holdings, example text, and labelled evaluation examples are synthetic. Stress scenarios are illustrative and are not financial forecasts or investment advice.

## 1. Project Overview — Problem Statement and Approach

Financial news and social-style text are unstructured, fast-moving, and difficult to connect directly to portfolio exposures. Analysts may need to review information from multiple sources before identifying potentially important events and understanding their possible implications.

SentinelRisk AI processes text from public RSS feeds, bundled CSV files, and manual input. It normalizes and deduplicates records, estimates sentiment, classifies events, and generates structured risk signals with an explainable impact score. The results are available through a REST API and an interactive dashboard.

The same risk signals feed two downstream modules:

- **Strategic portfolio stress testing:** Applies configurable, event-specific hypothetical shocks to a synthetic banking portfolio and reports position-level loss contributions.
- **Tactical index rebalancing:** Adjusts synthetic constituent weights using sentiment-related signals while enforcing configured weight limits and a total portfolio weight of 100%.

The objective is to demonstrate an end-to-end workflow from unstructured financial text to structured risk intelligence and illustrative portfolio analysis.

## 2. Architecture and Technology Stack

### System architecture

The system follows a modular pipeline:

1. **Input ingestion:** Reads public RSS feeds, synthetic CSV datasets, and manually entered text.
2. **Preprocessing:** Normalizes text and removes duplicate records.
3. **Sentiment analysis:** Estimates sentiment polarity, label, and confidence.
4. **Event classification:** Assigns a category such as geopolitical, macroeconomic, credit, regulatory/legal, or earnings/business.
5. **Impact scoring:** Produces an explainable risk impact score from 1 to 10.
6. **Storage and serving:** Persists signals in SQLite and exposes functionality through FastAPI.
7. **Downstream analysis:** Runs portfolio stress testing and index rebalancing.
8. **Visualization and export:** Displays results in Streamlit and supports CSV/JSON exports.

### Technology stack

- **Language:** Python
- **Data processing:** pandas, NumPy
- **Validation:** Pydantic
- **API:** FastAPI, Uvicorn
- **Dashboard:** Streamlit, Plotly
- **Database:** SQLite
- **Testing:** pytest, HTTPX
- **Optional NLP:** Transformers and FinBERT

The default demo uses a lightweight offline sentiment baseline. FinBERT can be enabled separately for sentiment analysis when the model and its dependencies are available.

## 3. Dataset Used

The project uses synthetic datasets to provide a reproducible demonstration without relying on confidential client information or proprietary financial data.

| File | Description |
|---|---|
| `data/sample_news.csv` | Synthetic financial news examples |
| `data/sample_social_posts.csv` | Synthetic social-style text examples |
| `data/synthetic_portfolio.csv` | Synthetic portfolio holdings and risk sensitivities |
| `data/synthetic_index.csv` | Synthetic index constituents and initial weights |
| `data/scenarios.json` | Illustrative financial stress scenario assumptions |
| `data/labelled_eval.csv` | Small synthetic labelled dataset for evaluation |

Public RSS ingestion is optional and depends on internet connectivity and source availability. The social-style input adapter uses bundled CSV data and manually entered text; live X/Twitter integration is not included.

The labelled evaluation dataset is intentionally small and synthetic. Its metrics are useful for checking the evaluation pipeline, not for demonstrating validated real-world predictive performance.

## 4. Quickstart and Installation

### Requirements

- Python 3.10 or later; Python 3.11 is recommended.
- Windows PowerShell, or a compatible Python environment.
- Internet access for installing dependencies and optionally fetching public RSS feeds.
- No API credentials are required for the default offline demo.

### Installation — Windows PowerShell

Open PowerShell in the repository root.

Create a virtual environment:

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, run the following in the current PowerShell session and activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Upgrade the packaging tools and install the project with its test dependencies:

```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
-e .[test]
```

This installs the application dependencies declared in `pyproject.toml`, along with the optional testing dependencies. No second editable-install command is necessary.

### Run the end-to-end demo

```powershell
python scripts/run_demo.py
```

The demo processes the bundled synthetic data, generates risk signals, runs the portfolio stress test, and produces rebalanced index weights.

Expected output from the verified demo run:

```text
SentinelRisk AI demo completed.
Unique risk signals: 18
Highest impact event: geopolitical (7/10)
Stress test triggered: True
Portfolio before: 100.00
Portfolio after:  91.09
New index weights sum: 1.000000
```

The exact outputs may change if the code, datasets, or scenario assumptions are modified.

Generated files are written under `results/`, including risk signals, stress-test summaries, position-level outputs, rebalanced index weights, and the SQLite database.

### Launch the dashboard

```powershell
python -m streamlit run app/dashboard.py
```

Open the local URL printed by Streamlit, normally:

[http://localhost:8501](http://localhost:8501)

Use the dashboard to inspect risk signals, portfolio stress-test results, index rebalancing outputs, and methodology information.

Keep the terminal open while using the dashboard. Press `Ctrl+C` to stop the server.

### Launch the API

Open a second PowerShell terminal in the repository root and activate the same virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the API:

```powershell
python -m uvicorn app.api:app --reload
```

Available endpoints:

- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Interactive API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Demo sample analysis: [http://127.0.0.1:8000/demo/analyze-samples](http://127.0.0.1:8000/demo/analyze-samples)

Example request from PowerShell:

```powershell
$body = @{
    text = "NVIDIA reports strong revenue growth after beating expectations."
    source_type = "financial_news"
    source_name = "manual test"
    is_synthetic = $true
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/analyze" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Evaluate the bundled labelled examples

```powershell
python scripts/evaluate.py
```

The evaluation script writes predictions to `results/evaluation_predictions.csv` and reports classification metrics on the bundled synthetic examples.

These metrics should be interpreted as a reproducible evaluation-pipeline check, not as evidence of real-world financial prediction accuracy.

### Run automated tests

```powershell
python -m pytest -q
```

The previously verified project build passed 11 automated tests. Run the command again after making changes to confirm the status of your submitted version.

### Optional FinBERT sentiment analysis

The default demo uses the offline sentiment baseline. To enable the optional FinBERT component, install the NLP dependencies:

```powershell
python -m pip install ".[nlp]"
```

Then enable the feature for the current PowerShell session:

```powershell
$env:SENTINELRISK_USE_FINBERT = "1"
python scripts/run_demo.py
```

The optional model may require a one-time download and can take longer to initialize. For a time-limited demonstration, use the default offline configuration.

## 5. Key Results and Domain Impact

The bundled demo demonstrates the following outputs:

- **18 unique risk signals:** Structured records generated from the bundled synthetic inputs.
- **Highest-impact event:** A geopolitical event with an impact score of 7 out of 10 in the verified demo run.
- **Portfolio stress test:** The illustrative synthetic portfolio value changes from 100.00 to 91.09 under the configured scenario.
- **Index rebalancing:** The sum of the resulting constituent weights is 1.000000.

These outputs demonstrate the integration of text analysis, event classification, impact scoring, portfolio stress testing, and index rebalancing.

Potential domain value includes faster event triage, consistent signal representation, and a more traceable connection between an event and hypothetical portfolio exposure. The system is a decision-support prototype and does not make investment recommendations.

## 6. Features

- Sentiment score in the range `[-1, 1]`, label, and confidence.
- Event classification covering geopolitical, macroeconomic, credit, M&A, regulatory/legal, earnings/business, product launch, and other categories.
- Explainable impact score from 1 to 10.
- Entity and sector hints.
- Text normalization and deduplication.
- Source provenance and SQLite persistence.
- Public RSS ingestion with network-failure handling.
- CSV and JSON exports.
- Synthetic portfolio stress testing with position-level outputs.
- Bounded index rebalancing with a total-weight constraint.
- FastAPI endpoints and an interactive Streamlit dashboard.
- Automated tests for core behavior and financial invariants.
- Offline-first demo that does not require API credentials or a pretrained-model download.

## 7. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze and persist one text item |
| GET | `/signals?limit=100` | Retrieve saved signals |
| POST | `/stress-test` | Run a scenario on the synthetic portfolio |
| GET | `/demo/analyze-samples` | Analyze bundled sample text |

See the interactive API documentation at `http://127.0.0.1:8000/docs` when the API server is running.

## 8. Evaluation and Limitations

The evaluation pipeline uses a small synthetic labelled dataset. It is intended to verify that the pipeline executes and reports metrics consistently.

The default rule-based sentiment baseline and event classifier are transparent, but they have limitations:

- Keyword ambiguity and difficulty handling negation or context.
- Limited entity alias coverage.
- Limited generalization beyond the bundled examples.
- No independent validation on a large real-world labelled dataset.
- No calibration of impact scores against observed market outcomes.

FinBERT can replace the sentiment component when enabled, but it does not replace the event classifier or calibrate financial losses.

### Financial model limitations

The portfolio holdings and scenarios are synthetic. Bond and loan shocks use a simplified first-order duration/spread approximation. Derivative exposures use a beta-based proxy rather than full instrument valuation.

The prototype does not fully model liquidity, collateral, default and recovery, convexity, options Greeks, correlated market dynamics, or calibrated causal effects. Outputs should not be used for real financial decisions.

## 9. Repository Structure

```text
iit-dharwad-bommaka-rajasekhar-reddy-hackathon/
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── app/
│   ├── dashboard.py
│   └── api.py
├── src/
│   └── sentinelrisk/
├── data/
│   ├── sample_news.csv
│   ├── sample_social_posts.csv
│   ├── synthetic_portfolio.csv
│   ├── synthetic_index.csv
│   ├── scenarios.json
│   └── labelled_eval.csv
├── scripts/
│   ├── run_demo.py
│   ├── evaluate.py
│   └── generate_data.py
├── tests/
├── results/
└── docs/
    ├── presentation.pdf
    ├── presentation.pptx
    ├── architecture.png
    ├── methodology.md
    └── evaluation_report.md
```

Generated files and optional documentation may vary by the final repository version. Do not commit the virtual environment, Python cache files, or temporary build artifacts.

## 10. License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE) for the license text.
