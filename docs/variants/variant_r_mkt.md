# Variant R-MKT · Market Factors Only (Zero Tweets)

- **ID:** `variant_r_mkt`
- **Stage / Group:** Top-3 Ablation · Market-Only (No Tweets) (`ablation`)
- **Verdict:** Ablation · No Tweets
- **Reported Study Benchmark:** +$3,781 (+15.12% ROC) · 62.5% WR · PF 2.02 · -9.34% DD · 8 trades
- **Executable Code:** [`variants/variant_r_mkt.py`](../../variants/variant_r_mkt.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests how much of Variant R's +31.26% came from market factors alone without reading any tweets.
- **How It Trades:** Scans 70 tickers (Oct 9-Nov 25) for pure high-volume red breakdown bars (-8% to -28%, >=2x avg vol) on ATR >= 3.2% or IBIT.
- **When It Buys / Shorts:** Shorts at breakdown-day close whenever one of 5 cash slots is open (zero tweets checked).
- **How Much It Bets:** $5,000 cash / $10,000 notional (2x margin), capped at $25,000 cash.
- **When It Sells / Exits:** +20% daily close target or Nov 25 close (net of slippage, 3% borrow, 6.5% margin).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_r_mkt` |
| `name` | `Variant R-MKT · Market Only` |
| `group` | `ablation` |
| `signal_source` | `market_only` |
| `min_atr_pct` | `3.2` |
| `crypto_exempt` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `cash_cap` | `25000.0` |
| `leverage` | `2.0` |
| `profit_target_pct` | `0.2` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_r_mkt.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_r_mkt
python3 run_backtest.py --variant variant_r_mkt --capital 10000
```
