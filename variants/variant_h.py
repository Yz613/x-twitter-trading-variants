"""Variant H · Profitable Add-On Only (No Stops) (Stage 3 · Surgical Filters & Regime)

Why it trades: Unbundled Variant G by deleting the losing stops while keeping the winning profitable add-on rule.
Reported benchmark: +$13,519 (+8.45% ROC) · 69.2% WR · PF 6.24 · 39 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_h",
    "name": "Variant H \u00b7 Profitable Add-On",
    "group": "core",
    "direct_only": True,
    "skip_long_gap_gt_3": True,
    "allow_duplicates": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant H · Profitable Add-On Only (No Stops) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
