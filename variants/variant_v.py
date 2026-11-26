"""Variant V · 0.25x Quarter-Kelly Live Engine (No Hard rho Cap) (Stage 5 · Champion (Live Rules))

Why it trades: Removes Variant S's overly tight rho <= 0.45 cap so live Quarter-Kelly compounding can capture clustered theme shocks.
Reported benchmark: +$2,365 (+9.46% / 30d) · 75.0% WR · -2.99% DD · 4.66 Sharpe · PF 17.86 · 8 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_v",
    "name": "Variant V \u00b7 Q-Kelly Live",
    "group": "core",
    "window_start": "2026-10-26",
    "direct_only": True,
    "min_tier": 4,
    "min_atr_pct": 3.2,
    "crypto_exempt": True,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "ban_bear_longs": True,
    "sizing_mode": "fractional_kelly",
    "kelly_fraction_t5": 0.16,
    "kelly_fraction_t4": 0.12,
    "cash_cap": 25000.0,
    "leverage": 1.0,
    "profit_target_pct": 0.2,
    "catastrophe_stop_pct": 0.15,
    "max_hold_days": 15,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant V · 0.25x Quarter-Kelly Live Engine (No Hard rho Cap) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
