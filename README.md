# SentinelRisk AI - S&P Global & Crisil Campus Hackathon 2026

**Candidate Name:** Bommaka Rajasekhar Reddy
**College Email ID:** cs23bt065@iitdh.ac.in
**College / Campus:** IIT Dharwad
**Demo Video Link:** ADD_YOUR_UNLISTED_YOUTUBE_LINK
**Slide Deck:** [Presentation PDF](docs/presentation.pdf)

## 1. Project Overview / Problem Statement & Approach

SentinelRisk AI converts financial news and text into structured risk
signals using sentiment analysis, event classification, and an
explainable impact score.

The prototype connects these signals to a synthetic portfolio stress
test and an index rebalancing module.

## 2. Architecture & Tech Stack

See [Architecture Diagram](docs/architecture.png).

Technologies: Python, pandas, NumPy, FastAPI, Streamlit, Plotly,
SQLite, and a transparent baseline NLP pipeline.

## 3. Dataset Used

The bundled news, social-style posts, portfolio holdings, index
constituents, and labelled evaluation examples are synthetic.
Optional RSS ingestion uses public sources when reachable.

## 4. Quickstart & Installation

See the tested setup commands below.

## 5. Key Results & Domain Impact

The bundled demo generated 18 unique risk signals. Its highest-impact
event was geopolitical with a score of 7/10. The illustrative
portfolio scenario changed the value from 100.00 to 91.09, and
rebalanced index weights summed to 1.000000.

These are synthetic demonstration results, not validated real-world
financial forecasts.
