from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sentinelrisk.config import DATA_DIR, RESULTS_DIR
from sentinelrisk.ingestion.csv_source import load_csv_records
from sentinelrisk.ingestion.rss import fetch_rss_records
from sentinelrisk.pipeline import analyze_records, analyze_record
from sentinelrisk.portfolio.portfolio_loader import load_portfolio
from sentinelrisk.portfolio.stress_tester import run_stress_test
from sentinelrisk.rebalancing.index_rebalancer import rebalance_index
from sentinelrisk.storage.repository import SignalRepository

st.set_page_config(page_title="SentinelRisk AI", page_icon="🛡️", layout="wide")
st.title("🛡️ SentinelRisk AI")
st.caption("Explainable financial event intelligence · Synthetic portfolio stress testing · Tactical index rebalancing")
st.info("Research prototype only. Scenario shocks and sample holdings are synthetic; outputs are not investment advice.")

@st.cache_resource
def get_repo():
    return SignalRepository(RESULTS_DIR / "sentinelrisk.db")

repo = get_repo()
page = st.sidebar.radio("Workspace", ["Risk Intelligence", "Portfolio Stress Test", "Index Rebalancer", "About & Data"])

if page == "Risk Intelligence":
    st.subheader("Risk signal engine")
    col1, col2 = st.columns([2, 1])
    with col1:
        manual_text = st.text_area("Analyze a headline or post", placeholder="Example: HDFC Bank reports rising bad loans amid credit concerns.")
        source_type = st.selectbox("Input source type", ["manual", "financial_news", "social_post"])
        if st.button("Analyze text", type="primary"):
            if not manual_text.strip():
                st.error("Enter some text first.")
            else:
                sig = analyze_record({"text": manual_text, "source_type": source_type,
                                      "source_name": "Dashboard input", "is_synthetic": True})
                repo.save_many([sig])
                st.session_state["latest_signal"] = sig.model_dump(mode="json")
                st.success("Risk signal created and saved.")
    with col2:
        st.markdown("#### Ingest sample data")
        if st.button("Load bundled datasets", width="stretch"):
            records = load_csv_records(DATA_DIR / "sample_news.csv", "financial_news")
            records += load_csv_records(DATA_DIR / "sample_social_posts.csv", "social_post")
            signals = analyze_records(records)
            repo.save_many(signals)
            st.session_state["latest_batch_count"] = len(signals)
            st.success(f"Processed and saved {len(signals)} unique records.")
        if st.button("Fetch public RSS feeds", width="stretch"):
            with st.spinner("Fetching public feeds (may fail offline)..."):
                records = fetch_rss_records(timeout=4, max_items=10)
                signals = analyze_records(records)
                if signals:
                    repo.save_many(signals)
                    st.success(f"Fetched and analyzed {len(signals)} records.")
                else:
                    st.warning("No RSS records fetched. Try bundled datasets; this is normal if feeds are blocked or unavailable.")
    latest = st.session_state.get("latest_signal")
    if latest:
        st.markdown("#### Latest signal")
        a, b, c, d = st.columns(4)
        a.metric("Sentiment", latest["sentiment_label"].title(), f'{latest["sentiment_score"]:+.2f}')
        b.metric("Event type", latest["event_type"].replace("_", " ").title())
        c.metric("Impact", f'{latest["impact_score"]}/10')
        d.metric("Confidence", f'{latest["sentiment_confidence"]:.0%}')
        with st.expander("Why did the engine produce this result?"):
            st.write(latest["text"])
            st.write("Entities:", ", ".join(latest["entities"]) or "None detected")
            st.write("Sectors:", ", ".join(latest["affected_sectors"]) or "None detected")
            for reason in latest["impact_reasons"]:
                st.write("•", reason)
            st.caption(f'Model: {latest["model_used"]} · Synthetic example: {latest["is_synthetic"]}')
    signals = repo.list_signals(300)
    if signals:
        df = pd.DataFrame(signals)
        st.markdown("#### Recent risk signals")
        show_cols = ["timestamp", "source_type", "sentiment_label", "sentiment_score", "event_type", "impact_score", "entities"]
        st.dataframe(df[show_cols], width="stretch", hide_index=True)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Export signals CSV", csv, "risk_signals.csv", "text/csv")
        st.download_button("Export signals JSON", df.to_json(orient="records", indent=2).encode(), "risk_signals.json", "application/json")
        chart = px.histogram(df, x="event_type", color="sentiment_label", title="Detected event types")
        st.plotly_chart(chart, width="stretch")

elif page == "Portfolio Stress Test":
    st.subheader("Event-driven portfolio stress testing")
    portfolio = load_portfolio(DATA_DIR / "synthetic_portfolio.csv")
    st.caption("Synthetic asset values and scenario shocks are illustrative only.")
    c1, c2, c3 = st.columns(3)
    event_type = c1.selectbox("Scenario event", ["geopolitical", "macroeconomic", "credit_event", "regulatory_legal", "merger_acquisition", "product_launch", "earnings_business", "other"])
    impact = c2.slider("Event impact score", 1, 10, 8)
    threshold = c3.slider("Trigger threshold", 1, 10, 7)
    st.dataframe(portfolio, width="stretch", hide_index=True)
    result = run_stress_test(portfolio, event_type, impact, threshold)
    if result["triggered"]:
        a, b, c, d = st.columns(4)
        a.metric("Before", f'${result["portfolio_before"]:,.2f}M')
        b.metric("After", f'${result["portfolio_after"]:,.2f}M')
        c.metric("Simulated loss", f'${result["total_loss"]:,.2f}M')
        d.metric("Loss %", f'{result["loss_pct"]:.2f}%')
        st.write(f'**Scenario:** {result["scenario_name"]} — {result["description"]}')
        positions = result["positions"]
        st.plotly_chart(px.bar(positions, x="asset_name", y="loss", color="asset_type", title="Loss contribution by position"), width="stretch")
        st.dataframe(positions[["asset_name", "asset_type", "market_value", "stress_return", "value_after", "loss"]], width="stretch", hide_index=True)
        st.download_button("Export stress-test results", positions.to_csv(index=False).encode(), "stress_test_positions.csv", "text/csv")
    else:
        st.warning(result["description"])

elif page == "Index Rebalancer":
    st.subheader("Tactical index rebalancing")
    index_df = pd.read_csv(DATA_DIR / "synthetic_index.csv")
    signals = repo.list_signals(500)
    alpha = st.slider("Sentiment sensitivity", 0.0, 1.0, 0.35, 0.05)
    min_weight = st.slider("Minimum constituent weight", 0.0, 0.08, 0.02, 0.005)
    max_weight = st.slider("Maximum constituent weight", 0.08, 0.30, 0.20, 0.01)
    try:
        result = rebalance_index(index_df, signals, alpha=alpha, min_weight=min_weight, max_weight=max_weight)
        st.metric("Sum of new weights", f'{result["new_weight"].sum():.6f}')
        st.plotly_chart(px.bar(result, x="ticker", y="new_weight", color="sentiment_score", title="Rebalanced constituent weights"), width="stretch")
        st.dataframe(result, width="stretch", hide_index=True)
        st.metric("Estimated one-way turnover", f'{result["estimated_turnover_contribution"].sum():.2%}')
        st.download_button("Export rebalanced index", result.to_csv(index=False).encode(), "rebalanced_index.csv", "text/csv")
    except ValueError as exc:
        st.error(str(exc))
    st.caption("For a meaningful company-specific demo, first analyze text mentioning a constituent company or load the sample signals.")

else:
    st.subheader("Architecture & limitations")
    st.markdown("""
    **Flow:** RSS/CSV/manual text → normalization and deduplication → sentiment analysis → event classification → impact scoring → SQLite/API → portfolio stress test and index rebalancer.

    **NLP:** The deterministic offline lexicon is the default. FinBERT is optional and requires installing the NLP extra plus a one-time model download. If it fails, the offline pipeline continues.

    **Financial model:** All holdings and shocks are synthetic. Stress losses are scenario estimates, not predictions of real market outcomes. The duration/spread approximation is simplified and is not a substitute for instrument-level valuation.

    **Data sources:** Bundled sample records are synthetic. RSS ingestion requests public feeds and may be blocked by network restrictions. No live social-media API is used.
    """)
