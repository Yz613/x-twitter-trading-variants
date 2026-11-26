"""Variant N · Sure-Thing Tiers ($10k Max) (Stage 4 · Concentration & Velocity)

Why it trades: Concentrates Variant M strictly into high-conviction Sure-Thing setups capped at $10k/trade.
Reported benchmark: +$12,429 net (+9.38% ROC) · 87.5% WR · PF 16.93 · 16 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_n",
    "name": "Variant N \u00b7 Sure-Thing $10k",
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
    """Execute Variant N · Sure-Thing Tiers ($10k Max) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
