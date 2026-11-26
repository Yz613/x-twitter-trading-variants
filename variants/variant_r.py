"""Variant R · $25k 2x Margin Sniper (Stage 4 · Champion (Peak Cash Efficiency))

Why it trades: Combines Tier 4-5 hard shocks + ATR >= 3.2% velocity with 2x Reg-T margin on a $25k cash cap and drops the Day-5 cut.
Reported benchmark: +$7,816 net (+31.26% ROC) · 100.0% WR (5/5) · PF INF · 5 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_r",
    "name": "Variant R \u00b7 $25k 2x Sniper",
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
    "cash_cap": 25000.0,
    "leverage": 2.0,
    "profit_target_pct": 0.2,
    "max_hold_days": 20,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant R · $25k 2x Margin Sniper on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
