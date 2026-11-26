"""Variant Q-MKT · Market Factors Only (Zero Tweets) (Top-3 Ablation · Market-Only (No Tweets))

Why it trades: Tests Variant Q's $30k 1x recycler + ATR >= 3.2% + Day-5 cut on pure technical breakdowns without tweets.
Reported benchmark: -$1,312 (-4.37% ROC) · 53.3% WR · PF 0.83 · -17.52% DD · 15 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_q_mkt",
    "name": "Variant Q-MKT \u00b7 Market Only",
    "group": "ablation",
    "signal_source": "market_only",
    "min_atr_pct": 3.2,
    "crypto_exempt": True,
    "sizing_mode": "fixed_cash",
    "cash_per_trade": 5000.0,
    "cash_cap": 30000.0,
    "leverage": 1.0,
    "profit_target_pct": 0.2,
    "day5_dead_money_cut": True,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant Q-MKT · Market Factors Only (Zero Tweets) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
