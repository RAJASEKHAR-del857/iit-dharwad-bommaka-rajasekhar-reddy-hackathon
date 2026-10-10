"""Regenerate deterministic synthetic data used by the offline demonstration."""
from pathlib import Path
import csv
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)

def write_csv(name, rows, fields):
    with (DATA / name).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

news = [
{"timestamp":"2026-10-10T09:00:00Z","source_name":"Synthetic Financial Wire","text":"HDFC Bank reports rising bad-loan provisions amid credit concerns.","entities":"HDFC Bank","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:05:00Z","source_name":"Synthetic Financial Wire","text":"NVIDIA beats quarterly revenue expectations as AI chip demand grows.","entities":"NVIDIA","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:10:00Z","source_name":"Synthetic Financial Wire","text":"Central bank signals a possible interest rate hike as inflation accelerates.","entities":"","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:15:00Z","source_name":"Synthetic Financial Wire","text":"Unexpected geopolitical escalation triggers new sanctions and threatens energy shipping routes.","entities":"","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:20:00Z","source_name":"Synthetic Financial Wire","text":"Regulator opens an antitrust investigation into a major technology company.","entities":"","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:25:00Z","source_name":"Synthetic Financial Wire","text":"Microsoft launches a new cloud security product with strong early demand.","entities":"Microsoft","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:30:00Z","source_name":"Synthetic Financial Wire","text":"Tesla shares fall after the company cuts its delivery outlook.","entities":"Tesla","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:35:00Z","source_name":"Synthetic Financial Wire","text":"Amazon announces acquisition of a logistics software startup.","entities":"Amazon","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:40:00Z","source_name":"Synthetic Financial Wire","text":"Apple reports record sales and improved operating profit.","entities":"Apple","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:45:00Z","source_name":"Synthetic Financial Wire","text":"Corporate bond issuer warns it may miss an upcoming debt payment.","entities":"","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:50:00Z","source_name":"Synthetic Financial Wire","text":"Oil prices rise sharply after a disruption to energy supply routes.","entities":"","is_synthetic":"true"},
{"timestamp":"2026-10-10T09:55:00Z","source_name":"Synthetic Financial Wire","text":"Bank of America faces a lawsuit alleging misleading disclosures.","entities":"Bank of America","is_synthetic":"true"}
]
social = [
{"timestamp":"2026-10-10T10:00:00Z","source_name":"Synthetic Social Stream","text":"$NVDA demand looks strong after another revenue beat.","entities":"NVIDIA","is_synthetic":"true"},
{"timestamp":"2026-10-10T10:02:00Z","source_name":"Synthetic Social Stream","text":"Worried about HDFC Bank credit quality after higher provisions.","entities":"HDFC Bank","is_synthetic":"true"},
{"timestamp":"2026-10-10T10:04:00Z","source_name":"Synthetic Social Stream","text":"Apple's product launch is getting positive early feedback.","entities":"Apple","is_synthetic":"true"},
{"timestamp":"2026-10-10T10:06:00Z","source_name":"Synthetic Social Stream","text":"Macro risk rising as inflation stays high and rates may increase.","entities":"","is_synthetic":"true"},
{"timestamp":"2026-10-10T10:08:00Z","source_name":"Synthetic Social Stream","text":"Tesla delivery warning creates downside risk for the stock.","entities":"Tesla","is_synthetic":"true"},
{"timestamp":"2026-10-10T10:10:00Z","source_name":"Synthetic Social Stream","text":"Microsoft cloud growth and strong profits improve the outlook.","entities":"Microsoft","is_synthetic":"true"}
]
portfolio = [
{"asset_id":"A01","asset_name":"Technology Equity Basket","asset_type":"equity","sector":"technology","market_value":25.0,"duration":0,"credit_spread_sensitivity":0,"equity_beta":1.15},
{"asset_id":"A02","asset_name":"Bank Equity Basket","asset_type":"equity","sector":"financials","market_value":15.0,"duration":0,"credit_spread_sensitivity":0,"equity_beta":1.20},
{"asset_id":"A03","asset_name":"Energy Equity Basket","asset_type":"equity","sector":"energy","market_value":10.0,"duration":0,"credit_spread_sensitivity":0,"equity_beta":1.10},
{"asset_id":"A04","asset_name":"Investment Grade Bonds","asset_type":"bond","sector":"financials","market_value":20.0,"duration":4.5,"credit_spread_sensitivity":0.65,"equity_beta":0},
{"asset_id":"A05","asset_name":"Government Bond Portfolio","asset_type":"bond","sector":"government","market_value":15.0,"duration":6.0,"credit_spread_sensitivity":0.05,"equity_beta":0},
{"asset_id":"A06","asset_name":"Corporate Loan Book","asset_type":"loan","sector":"financials","market_value":10.0,"duration":2.0,"credit_spread_sensitivity":0.80,"equity_beta":0},
{"asset_id":"A07","asset_name":"Equity Index Derivative","asset_type":"derivative","sector":"technology","market_value":5.0,"duration":0,"credit_spread_sensitivity":0,"equity_beta":1.50}
]
index = [
("AAPL","Apple",0.10),("MSFT","Microsoft",0.10),("NVDA","NVIDIA",0.10),
("AMZN","Amazon",0.08),("GOOGL","Alphabet",0.08),("TSLA","Tesla",0.07),
("JPM","JPMorgan",0.08),("BAC","Bank of America",0.07),("HDFCBANK","HDFC Bank",0.07),
("RELIANCE","Reliance Industries",0.07),("INFY","Infosys",0.06),("TCS","Tata Consultancy Services",0.06),
("EXM","Example Corp",0.06)
]
write_csv("sample_news.csv", news, ["timestamp","source_name","text","entities","is_synthetic"])
write_csv("sample_social_posts.csv", social, ["timestamp","source_name","text","entities","is_synthetic"])
write_csv("synthetic_portfolio.csv", portfolio, ["asset_id","asset_name","asset_type","sector","market_value","duration","credit_spread_sensitivity","equity_beta"])
write_csv("synthetic_index.csv", [{"ticker":t,"company":c,"weight":w} for t,c,w in index], ["ticker","company","weight"])
(DATA / "scenarios.json").write_text(__import__("json").dumps({
    "note":"All shocks are illustrative and synthetic.",
    "geopolitical":{"equity_shock":-0.10,"credit_spread_shock_bps":150,"rate_shock_bps":50,"fx_shock":-0.03},
    "macroeconomic":{"equity_shock":-0.08,"credit_spread_shock_bps":100,"rate_shock_bps":-50,"fx_shock":-0.01},
    "credit_event":{"equity_shock":-0.05,"credit_spread_shock_bps":250,"rate_shock_bps":25,"fx_shock":-0.01}
}, indent=2), encoding="utf-8")
print("Synthetic datasets generated in", DATA)

