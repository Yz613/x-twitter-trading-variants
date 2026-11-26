"""Variant A · Raw Baseline (No Filters) (Stage 0 · Unfiltered Baseline)

Why it trades: Zero-rule control test to see if raw @KobeissiLetter headlines have standalone alpha before adding guardrails.
Reported benchmark: +$1,402 (+0.45% ROC) · 54.8% WR · 31 trades (Oct)
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_a",
    "name": "Variant A \u00b7 Raw Baseline",
    "group": "core",
    "window_start": "2026-10-09",
    "window_end": "2026-11-25",
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 10000.0,
    "leverage": 1.0,
    "allow_duplicates": True,
    "bypass_market_filters": True,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant A · Raw Baseline (No Filters) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
