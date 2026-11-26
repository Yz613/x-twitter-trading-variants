"""Variant R-MKT · Market Factors Only (Zero Tweets) (Top-3 Ablation · Market-Only (No Tweets))

Why it trades: Tests how much of Variant R's +31.26% came from market factors alone without reading any tweets.
Reported benchmark: +$3,781 (+15.12% ROC) · 62.5% WR · PF 2.02 · -9.34% DD · 8 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_r_mkt",
    "name": "Variant R-MKT \u00b7 Market Only",
    "group": "ablation",
    "signal_source": "market_only",
    "min_atr_pct": 3.2,
    "crypto_exempt": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "cash_cap": 25000.0,
    "leverage": 2.0,
    "profit_target_pct": 0.2,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant R-MKT · Market Factors Only (Zero Tweets) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
