# Variant Q-MKT · Market Factors Only (Zero Tweets)

- **ID:** `variant_q_mkt`
- **Stage / Group:** Top-3 Ablation · Market-Only (No Tweets) (`ablation`)
- **Verdict:** Ablation · No Tweets
- **Reported Study Benchmark:** -$1,312 (-4.37% ROC) · 53.3% WR · PF 0.83 · -17.52% DD · 15 trades
- **Executable Code:** [`variants/variant_q_mkt.py`](../../variants/variant_q_mkt.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests Variant Q's $30k 1x recycler + ATR >= 3.2% + Day-5 cut on pure technical breakdowns without tweets.
- **How It Trades:** Scans 70 tickers for pure high-volume red breakdown bars (-8% to -28%, >=2x vol) with ATR >= 3.2% or IBIT.
- **When It Buys / Shorts:** Shorts at breakdown-day close whenever one of 6 unlevered $5k slots is open.
- **How Much It Bets:** Flat $5,000 cash (1x), capped at $30,000 cash.
- **When It Sells / Exits:** +20% daily close target, Day-5 <+2% cut, or Nov 25 close (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_q_mkt` |
| `name` | `Variant Q-MKT · Market Only` |
| `group` | `ablation` |
| `signal_source` | `market_only` |
| `min_atr_pct` | `3.2` |
| `crypto_exempt` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `cash_cap` | `30000.0` |
| `leverage` | `1.0` |
| `profit_target_pct` | `0.2` |
| `day5_dead_money_cut` | `True` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_q_mkt.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_q_mkt
python3 run_backtest.py --variant variant_q_mkt --capital 10000
```
