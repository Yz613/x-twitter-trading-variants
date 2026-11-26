"""Variant K-TW · Tweets Only (Zero Market Filters) (Top-3 Ablation · Tweets-Only (No Market Filters))

Why it trades: Inverse test of K-MKT: takes all 41 raw directional tweets with zero market filters and holds to Nov 25.
Reported benchmark: +$8,888 (+4.34% ROC) · 61.0% WR · PF 2.01 · -5.02% DD · 41 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_k_tw",
    "name": "Variant K-TW \u00b7 Tweets Only",
    "group": "ablation",
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant K-TW · Tweets Only (Zero Market Filters) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
