"""Variant Q-TW · Tweets Only (Zero Market Filters) (Top-3 Ablation · Tweets-Only (No Market Filters))

Why it trades: Inverse test of Q-MKT: runs Variant Q's $30k 1x cap + Day-5 cut on raw unfiltered tweets.
Reported benchmark: -$853 (-2.84% ROC) · 26.7% WR · PF 0.69 · -9.05% DD · 15 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_q_tw",
    "name": "Variant Q-TW \u00b7 Tweets Only",
    "group": "ablation",
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "cash_cap": 30000.0,
    "leverage": 1.0,
    "profit_target_pct": 0.2,
    "day5_dead_money_cut": True,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant Q-TW · Tweets Only (Zero Market Filters) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
