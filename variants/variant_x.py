"""Variant X · Hybrid Live Playbook (Synthesis of Stages 0-5) (Final Production Blueprint)

Why it trades: Synthesizes every edge-positive rule across Stages 0-5 while cutting every rule that leaked money.
Reported benchmark: Target Bankroll: $25k-$30k (Untested live blueprint; backtestable via simulator)
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_x",
    "name": "Variant X \u00b7 Hybrid Blueprint",
    "group": "core",
    "direct_only": True,
    "min_tier": 4,
    "min_atr_pct": 3.2,
    "crypto_exempt": True,
    "skip_long_gap_gt_3": True,
    "tape_confirm": True,
    "spy_regime_gate": True,
    "ban_bear_longs": True,
    "sizing_mode": "fractional_kelly",
    "kelly_fraction_t5": 0.2,
    "kelly_fraction_t4": 0.13,
    "cash_cap": 25000.0,
    "leverage": 1.0,
    "profit_target_pct": 0.2,
    "catastrophe_stop_pct": 0.15,
    "max_hold_days": 20,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant X · Hybrid Live Playbook (Synthesis of Stages 0-5) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
