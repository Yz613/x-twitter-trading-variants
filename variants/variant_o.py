"""Variant O · Sure-Thing Stack ($15k Max) (Stage 4 · Concentration & Velocity)

Why it trades: Tests stacking up to $15k notional on top-conviction winners in the Sure-Thing book.
Reported benchmark: +$13,604 net (+9.89% ROC) · 88.2% WR · PF 18.44 · 17 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_o",
    "name": "Variant O \u00b7 Sure-Thing $15k",
    "group": "core",
    "direct_only": True,
    "min_tier": 4,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "ban_bear_longs": True,
    "allow_duplicates": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant O · Sure-Thing Stack ($15k Max) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
