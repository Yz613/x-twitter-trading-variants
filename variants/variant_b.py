"""Variant B · Core Guardrails (Rules 1-3) (Stage 1 · Core Guardrails)

Why it trades: Fixes Variant A's three worst leaks: chasing >3% overnight long gaps, trading noisy proxy ETFs, and stacking accidental duplicates.
Reported benchmark: Nov OOS: +$7,132 (+4.20% ROC) · 64.7% WR · 41 trades (24 Oct / 17 Nov)
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_b",
    "name": "Variant B \u00b7 Core Guardrails",
    "group": "core",
    "direct_only": True,
    "skip_long_gap_gt_3": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 10000.0,
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant B · Core Guardrails (Rules 1-3) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
