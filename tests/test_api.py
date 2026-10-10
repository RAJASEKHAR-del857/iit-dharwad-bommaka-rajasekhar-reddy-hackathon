from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze_endpoint():
    response = client.post("/analyze", json={
        "text": "NVIDIA reports strong revenue growth.",
        "source_type": "financial_news",
        "source_name": "pytest",
        "is_synthetic": True
    })
    assert response.status_code == 200
    body = response.json()
    assert "sentiment_score" in body and "event_type" in body and "impact_score" in body

def test_stress_endpoint():
    response = client.post("/stress-test", json={"event_type":"geopolitical","impact_score":9,"threshold":7})
    assert response.status_code == 200
    assert response.json()["triggered"] is True
