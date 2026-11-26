"""Shlomo-5.25 · Sweet-Spot Floor >= 5.25 (1x 5d) (Shlomo Suite · Best 1x ROC Overall)

Why it trades: Raises Shlomo's floor to the 5.25 inflection point that drops proxy/rumor noise without starving top winners.
Reported benchmark: +$7,641 (+16.98% ROC) · 77.8% WR · PF 10.37 · 18 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "shlomo_525",
    "name": "Shlomo-5.25 \u00b7 Sweet-Spot 1x",
    "group": "shlomo",
    "shlomo_min_score": 5.25,
    "bypass_market_filters": True,
    "allow_duplicates": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "leverage": 1.0,
    "max_hold_days": 5,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Shlomo-5.25 · Sweet-Spot Floor >= 5.25 (1x 5d) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
