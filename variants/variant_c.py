"""Variant C · Guardrails + 8% Intraday Stop (Stage 1 · Core Guardrails)

Why it trades: Tested whether an 8% intraday stop-loss and 10-day max hold would protect Variant B from blowups.
Reported benchmark: Nov OOS: +$3,592 (+2.11% ROC) · 47.1% WR · 41 trades (24 Oct / 17 Nov)
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_c",
    "name": "Variant C \u00b7 8% Intraday Stop",
    "group": "core",
    "direct_only": True,
    "skip_long_gap_gt_3": True,
    "intraday_stop_pct": 0.08,
    "max_hold_days": 10,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 10000.0,
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant C · Guardrails + 8% Intraday Stop on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
