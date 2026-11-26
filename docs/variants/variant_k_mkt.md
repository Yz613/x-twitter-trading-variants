# Variant K-MKT · Market Factors Only (Zero Tweets)

- **ID:** `variant_k_mkt`
- **Stage / Group:** Top-3 Ablation · Market-Only (No Tweets) (`ablation`)
- **Verdict:** Ablation · No Tweets
- **Reported Study Benchmark:** +$3,542 (+2.62% ROC) · 59.3% WR · PF 1.42 · -3.20% DD · 27 trades
- **Executable Code:** [`variants/variant_k_mkt.py`](../../variants/variant_k_mkt.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests Variant K's SPY 20-SMA regime gate and all-ATR book on pure technical breakdowns with zero tweets.
- **How It Trades:** Scans all 70 tickers (any ATR) for red breakdown bars (-8% to -28%, >=2x vol) sized via SPY 20-SMA.
- **When It Buys / Shorts:** Shorts at breakdown-day close across all ATRs (max 1 per ticker; zero tweets checked).
- **How Much It Bets:** $5,000 in bear tape / $2,500 in bull tape, uncapped 1x cash ($135,000 peak cash).
- **When It Sells / Exits:** No stops/targets; holds to Nov 25 close (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_k_mkt` |
| `name` | `Variant K-MKT · Market Only` |
| `group` | `ablation` |
| `signal_source` | `market_only` |
| `min_atr_pct` | `0.0` |
| `sizing_mode` | `regime_fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_k_mkt.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_k_mkt
python3 run_backtest.py --variant variant_k_mkt --capital 10000
```
