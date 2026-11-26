"""Variant K-MKT · Market Factors Only (Zero Tweets) (Top-3 Ablation · Market-Only (No Tweets))

Why it trades: Tests Variant K's SPY 20-SMA regime gate and all-ATR book on pure technical breakdowns with zero tweets.
Reported benchmark: +$3,542 (+2.62% ROC) · 59.3% WR · PF 1.42 · -3.20% DD · 27 trades
"""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.simulator import run_variant_backtest

CONFIG = {
    "id": "variant_k_mkt",
    "name": "Variant K-MKT \u00b7 Market Only",
    "group": "ablation",
    "signal_source": "market_only",
    "min_atr_pct": 0.0,
    "sizing_mode": "regime_fixed_cash",
    "cash_per_trade": 5000.0,
    "leverage": 1.0,
    "net_of_fees": True
}


def run(capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Execute Variant K-MKT · Market Factors Only (Zero Tweets) on real Yahoo Finance daily OHLC bars."""
    return run_variant_backtest(CONFIG, capital_override=capital_override, ohlc_cache=ohlc_cache)


if __name__ == "__main__":
    result = run()
    print(json.dumps({k: val for k, val in result.items() if k != "positions"}, indent=2))
