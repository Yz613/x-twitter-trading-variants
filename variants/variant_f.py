"""Variant F · Fast 10-20m Fills + 5 Conviction Tiers (Stage 2 · Fast Fills + Tiers)

Why it trades: Waiting until 9:30 a.m. missed initial news drift, and flat $10k bets treated vague sentiment the same as concrete SEC probes and hacks.
Reported benchmark: +$10,133 (+7.31% ROC) · 65.7% WR · PF 4.93 · 35 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_f",
    "name": "Variant F \u00b7 Fast Fills + Tiers",
    "group": "core",
    "direct_only": True,
    "skip_long_gap_gt_3": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": False
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant F · Fast 10-20m Fills + 5 Conviction Tiers on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
