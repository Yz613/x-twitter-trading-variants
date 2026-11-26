"""Variant I · 50/50 Scale-In & 15% Scale-Out (Stage 3 · Surgical Filters & Regime)

Why it trades: Tested whether easing in 50/50 and trimming at +15% smoothed risk; cost -$857 vs. Variant H.
Reported benchmark: +$12,662 (+8.36% ROC) · 69.2% WR · PF 6.53 · 39 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_i",
    "name": "Variant I \u00b7 50/50 Scale",
    "group": "core",
    "direct_only": True,
    "skip_long_gap_gt_3": True,
    "profit_target_pct": 0.15,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant I · 50/50 Scale-In & 15% Scale-Out on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
