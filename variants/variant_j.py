"""Variant J · Tape Confirmation, IPO & Tier-1 Fixes (Stage 3 · Surgical Filters & Regime)

Why it trades: Plugged three loopholes in H: vague Tier 1 noise, Day-1 IPO hype (ANT), and shorting stocks rallying through bad news (TSLA).
Reported benchmark: +$14,392 (+9.44% ROC) · 76.5% WR · PF 9.66 · 34 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_j",
    "name": "Variant J \u00b7 Tape & IPO Fixes",
    "group": "core",
    "direct_only": True,
    "min_tier": 2,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant J · Tape Confirmation, IPO & Tier-1 Fixes on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
