SCENARIOS = {
    "geopolitical": {
        "name": "Geopolitical escalation",
        "equity_shock": -0.10,
        "credit_spread_shock_bps": 150,
        "rate_shock_bps": 50,
        "fx_shock": -0.03,
        "description": "Illustrative equity decline, credit-spread widening, rate and FX shocks."
    },
    "macroeconomic": {
        "name": "Macroeconomic slowdown",
        "equity_shock": -0.08,
        "credit_spread_shock_bps": 100,
        "rate_shock_bps": -50,
        "fx_shock": -0.01,
        "description": "Illustrative growth shock with spread widening and a rate decline."
    },
    "credit_event": {
        "name": "Credit deterioration",
        "equity_shock": -0.05,
        "credit_spread_shock_bps": 250,
        "rate_shock_bps": 25,
        "fx_shock": -0.01,
        "description": "Illustrative credit stress with spread widening."
    },
    "regulatory_legal": {
        "name": "Regulatory or legal shock",
        "equity_shock": -0.06,
        "credit_spread_shock_bps": 75,
        "rate_shock_bps": 0,
        "fx_shock": 0.0,
        "description": "Illustrative repricing of exposed equities and credit."
    },
    "merger_acquisition": {
        "name": "Merger or acquisition event",
        "equity_shock": -0.02,
        "credit_spread_shock_bps": 25,
        "rate_shock_bps": 0,
        "fx_shock": 0.0,
        "description": "Conservative generic event shock; deal-specific effects are not modelled."
    },
    "product_launch": {
        "name": "Product launch",
        "equity_shock": -0.01,
        "credit_spread_shock_bps": 0,
        "rate_shock_bps": 0,
        "fx_shock": 0.0,
        "description": "Small illustrative broad shock; positive or negative company-specific effects need richer data."
    },
    "earnings_business": {
        "name": "Earnings or business performance",
        "equity_shock": -0.04,
        "credit_spread_shock_bps": 50,
        "rate_shock_bps": 0,
        "fx_shock": 0.0,
        "description": "Illustrative earnings stress; not a forecast."
    },
    "other": {
        "name": "Generic event",
        "equity_shock": -0.02,
        "credit_spread_shock_bps": 25,
        "rate_shock_bps": 0,
        "fx_shock": 0.0,
        "description": "Small generic scenario for unclassified events."
    }
}
