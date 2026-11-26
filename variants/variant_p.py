"""Variant P · Tier 4-5 Sniper Only (Uncapped) (Stage 4 · Concentration & Velocity)

Why it trades: Isolates purely Tier 4-5 hard shocks across all ATRs before imposing a small-account cash cap.
Reported benchmark: +$12,342 net (+9.49% ROC) · 86.7% WR · PF 16.82 · 15 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_p",
    "name": "Variant P \u00b7 T4-5 Uncapped",
    "group": "core",
    "direct_only": True,
    "min_tier": 4,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "ban_bear_longs": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant P · Tier 4-5 Sniper Only (Uncapped) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
