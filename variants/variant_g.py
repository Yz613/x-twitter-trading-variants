"""Variant G · Fast Fills + Stops & Add-On Bundle (Stage 2 · Fast Fills + Tiers)

Why it trades: Tested adding 12% close stop + 10% trailing stop + 1 profitable add-on on top of Variant F.
Reported benchmark: Oct +$6,334 / Nov +$3,137 · 39 trades (20 Oct / 19 Nov)
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_g",
    "name": "Variant G \u00b7 Stops + Add-On",
    "group": "core",
    "direct_only": True,
    "skip_long_gap_gt_3": True,
    "catastrophe_stop_pct": 0.12,
    "trailing_stop_pct": 0.1,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant G · Fast Fills + Stops & Add-On Bundle on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
