"""Variant Q · $30k Unlevered Velocity Recycler (Stage 4 · Small-Bankroll Velocity)

Why it trades: Runs the strategy on a realistic $30,000 unlevered cash account by requiring fast movers (ATR >= 3.2% or crypto) and recycling cash at +20%.
Reported benchmark: +$3,778 net (+12.59% ROC) · 85.7% WR · PF 5.74 · 7 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_q",
    "name": "Variant Q \u00b7 $30k 1x Recycler",
    "group": "core",
    "direct_only": True,
    "min_tier": 4,
    "min_atr_pct": 3.2,
    "crypto_exempt": True,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "ban_bear_longs": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "cash_cap": 30000.0,
    "leverage": 1.0,
    "profit_target_pct": 0.2,
    "day5_dead_money_cut": True,
    "max_hold_days": 20,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant Q · $30k Unlevered Velocity Recycler on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
