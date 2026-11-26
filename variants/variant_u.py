"""Variant U · 0.25x Quarter-Kelly Liquid-Hours Sniper (Stage 5 · Live 30-Day Rules)

Why it trades: Tests Variant R's strict sniper rules inside Stage 5's 8:30am-4pm ET liquid-hours box.
Reported benchmark: +$755 (+3.02% / 30d) · 100.0% WR (1/1) · 3.57 Sharpe · 1 trade
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_u",
    "name": "Variant U \u00b7 Q-Kelly Sniper",
    "group": "core",
    "window_start": "2026-10-26",
    "direct_only": True,
    "min_tier": 5,
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
    """Execute Variant U · 0.25x Quarter-Kelly Liquid-Hours Sniper on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
