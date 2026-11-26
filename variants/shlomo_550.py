"""Shlomo-5.50 · Precision Floor >= 5.50 (1x 5d) (Shlomo Suite · Peak Shlomo Win Rate)

Why it trades: Pushes rubric selectivity to 5.50 / 10 for maximum hit rate and tiny worst-case loss (-$285) on $30k unlevered cash.
Reported benchmark: +$3,648 (+12.16% ROC) · 83.3% WR · PF 10.09 · 12 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "shlomo_550",
    "name": "Shlomo-5.50 \u00b7 Precision 1x",
    "group": "shlomo",
    "shlomo_min_score": 5.5,
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "leverage": 1.0,
    "max_hold_days": 5,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Shlomo-5.50 · Precision Floor >= 5.50 (1x 5d) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
