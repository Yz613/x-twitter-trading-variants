"""Shlomo · Original Floor >= 3.0 (5-Day Hold) (Shlomo Suite · 8-Metric Rubric)

Why it trades: Applies Shlomo's 8-metric ticket-quality rubric (0-10 equal weight, publish floor >= 3.0) with his recommended 5-session fixed hold.
Reported benchmark: +$8,032 (+10.71% ROC) · 58.5% WR · PF 3.01 · 41 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "shlomo_30",
    "name": "Shlomo \u00b7 Floor >= 3.0",
    "group": "shlomo",
    "shlomo_min_score": 3.0,
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "leverage": 1.0,
    "max_hold_days": 5,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Shlomo · Original Floor >= 3.0 (5-Day Hold) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
