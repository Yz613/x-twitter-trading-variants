"""Variant K · SPY 20-SMA Regime Gate (Stage 3 · Champion (Peak Raw Dollars))

Why it trades: Buying news in a bear tape gets faded. Gates direction and sizing using SPY vs. its 20-day moving average.
Reported benchmark: +$15,184 (+10.35% ROC, 81.2% WR, PF 18.45, 32 trades; Net Cont: +$14,214 / +10.28%)
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_k",
    "name": "Variant K \u00b7 SPY 20-SMA Regime",
    "group": "core",
    "direct_only": True,
    "min_tier": 2,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "sizing_mode": "tier_map",
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant K · SPY 20-SMA Regime Gate on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
