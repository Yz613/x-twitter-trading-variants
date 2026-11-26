"""Shlomo-Tiered · Score-Sized Floor >= 5.0 (Shlomo Suite · Peak Shlomo Dollars)

Why it trades: Uses Shlomo's 8-metric score itself for position sizing — betting 4x larger on elite (>=5.75) tickets than borderline (5.00-5.24) tickets.
Reported benchmark: +$14,272 (+10.57% ROC) · 75.0% WR · PF 5.74 · 24 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "shlomo_tiered",
    "name": "Shlomo-Tiered \u00b7 >=5.0 Sized",
    "group": "shlomo",
    "shlomo_min_score": 5.0,
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "shlomo_tiered",
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Shlomo-Tiered · Score-Sized Floor >= 5.0 on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
