"""Variant L · ATR Inverse Volatility Down-Sizing (Stage 3 · Surgical Filters & Regime)

Why it trades: Tested risk-parity inverse-ATR sizing; backfired (-$4,928) because volatile stocks ARE the catalyst profit engine.
Reported benchmark: +$9,809 net (+8.79% ROC) · 81.2% WR · PF 12.61 · 32 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_l",
    "name": "Variant L \u00b7 ATR Down-Size",
    "group": "core",
    "direct_only": True,
    "min_tier": 2,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 3500.0,
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant L · ATR Inverse Volatility Down-Sizing on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
