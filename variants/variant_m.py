"""Variant M · Max Win Rate (Quality Floor + Bear Long Ban) (Stage 4 · Champion (Peak Win Rate))

Why it trades: Eliminates remaining commodity chatter, slow bond ETFs, and all bear-tape longs to maximize precision.
Reported benchmark: +$12,055 net (+9.57% ROC) · 90.5% WR · PF 22.32 · 21 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_m",
    "name": "Variant M \u00b7 Max Win Rate",
    "group": "core",
    "direct_only": True,
    "min_tier": 2,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "ban_bear_longs": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant M · Max Win Rate (Quality Floor + Bear Long Ban) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
