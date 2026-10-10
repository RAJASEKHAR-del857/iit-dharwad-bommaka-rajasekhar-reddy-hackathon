from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentinelrisk.pipeline import analyze_record
from sentinelrisk.config import DATA_DIR, DB_PATH
from sentinelrisk.ingestion.csv_source import load_csv_records
from sentinelrisk.portfolio.portfolio_loader import load_portfolio
from sentinelrisk.portfolio.stress_tester import run_stress_test
from sentinelrisk.storage.repository import SignalRepository

app = FastAPI(title="SentinelRisk AI API", version="1.0.0",
              description="Explainable financial event signals and scenario simulations.")
repo = SignalRepository(DB_PATH)

class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    source_type: str = "manual"
    source_name: str = "API input"
    is_synthetic: bool = True

class StressRequest(BaseModel):
    event_type: str
    impact_score: int = Field(ge=1, le=10)
    threshold: int = Field(default=7, ge=1, le=10)

@app.get("/health")
def health():
    return {"status": "ok", "service": "sentinelrisk-api"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        signal = analyze_record(request.model_dump())
        repo.save_many([signal])
        return signal.model_dump(mode="json")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/signals")
def signals(limit: int = 100):
    if not 1 <= limit <= 1000:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 1000")
    return repo.list_signals(limit)

@app.post("/stress-test")
def stress_test(request: StressRequest):
    try:
        portfolio = load_portfolio(DATA_DIR / "synthetic_portfolio.csv")
        result = run_stress_test(portfolio, request.event_type, request.impact_score, request.threshold)
        positions = result.pop("positions")
        result["positions"] = positions.to_dict(orient="records")
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/demo/analyze-samples")
def analyze_samples():
    records = load_csv_records(DATA_DIR / "sample_news.csv", "financial_news")
    records += load_csv_records(DATA_DIR / "sample_social_posts.csv", "social_post")
    return [analyze_record(record).model_dump(mode="json") for record in records]
