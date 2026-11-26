# Variant Q-TW · Tweets Only (Zero Market Filters)

- **ID:** `variant_q_tw`
- **Stage / Group:** Top-3 Ablation · Tweets-Only (No Market Filters) (`ablation`)
- **Verdict:** Ablation · Tweets Only
- **Reported Study Benchmark:** -$853 (-2.84% ROC) · 26.7% WR · PF 0.69 · -9.05% DD · 15 trades
- **Executable Code:** [`variants/variant_q_tw.py`](../../variants/variant_q_tw.py)

---

## Plain-English Breakdown

- **Why It Trades:** Inverse test of Q-MKT: runs Variant Q's $30k 1x cap + Day-5 cut on raw unfiltered tweets.
- **How It Trades:** Takes every chronological directional tweet with zero ATR, gap, tape, or SPY regime filtering.
- **When It Buys / Shorts:** Enters Long or Short at next open whenever one of 6 unlevered $5k slots is open.
- **How Much It Bets:** Flat $5,000 cash (1x), capped at $30,000 cash.
- **When It Sells / Exits:** +20% daily close target, Day-5 <+2% cut, or Nov 25 close (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_q_tw` |
| `name` | `Variant Q-TW · Tweets Only` |
| `group` | `ablation` |
| `bypass_market_filters` | `True` |
| `allow_duplicates` | `True` |
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
python3 variants/variant_q_tw.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_q_tw
python3 run_backtest.py --variant variant_q_tw --capital 10000
```
