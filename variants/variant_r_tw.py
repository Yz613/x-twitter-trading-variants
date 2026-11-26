"""Variant R-TW · Tweets Only (Zero Market Filters) (Top-3 Ablation · Tweets-Only (No Market Filters))

Why it trades: Inverse test of R-MKT: strips away ALL market filters and feeds raw chronological tweets into Variant R's $25k 2x engine.
Reported benchmark: -$2,162 (-8.65% ROC) · 40.0% WR · PF 0.40 · -14.36% DD · 5 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_r_tw",
    "name": "Variant R-TW \u00b7 Tweets Only",
    "group": "ablation",
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "cash_cap": 25000.0,
    "leverage": 2.0,
    "profit_target_pct": 0.2,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant R-TW · Tweets Only (Zero Market Filters) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
