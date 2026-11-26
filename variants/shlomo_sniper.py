"""Shlomo-Sniper · >= 5.5 + Early/No-Conflict ($25k 2x 5d) (Shlomo Suite · Best ROC (#2 Overall))

Why it trades: Pairs Shlomo's highest-conviction rubric gate (>= 5.5 + fresh entry >= 4.5 + no conflict >= 5.0) with a $25k 2x 5-day recycler.
Reported benchmark: +$5,943 (+23.77% ROC) · 77.8% WR · PF 8.29 · 9 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "shlomo_sniper",
    "name": "Shlomo-Sniper \u00b7 2x 5d",
    "group": "shlomo",
    "shlomo_min_score": 5.5,
    "min_entry_quality": 4.5,
    "min_conflict_check": 5.0,
    "bypass_market_filters": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "cash_cap": 25000.0,
    "leverage": 2.0,
    "profit_target_pct": 0.2,
    "max_hold_days": 5,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Shlomo-Sniper · >= 5.5 + Early/No-Conflict ($25k 2x 5d) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
