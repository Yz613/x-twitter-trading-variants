# Variant K-TW · Tweets Only (Zero Market Filters)

- **ID:** `variant_k_tw`
- **Stage / Group:** Top-3 Ablation · Tweets-Only (No Market Filters) (`ablation`)
- **Verdict:** Ablation · Tweets Only
- **Reported Study Benchmark:** +$8,888 (+4.34% ROC) · 61.0% WR · PF 2.01 · -5.02% DD · 41 trades
- **Executable Code:** [`variants/variant_k_tw.py`](../../variants/variant_k_tw.py)

---

## Plain-English Breakdown

- **Why It Trades:** Inverse test of K-MKT: takes all 41 raw directional tweets with zero market filters and holds to Nov 25.
- **How It Trades:** Unfiltered tweet book taking both Longs and Shorts, including duplicates and proxy ETFs.
- **When It Buys / Shorts:** Enters Long or Short at next open on all 41 directional tweets.
- **How Much It Bets:** Flat $5,000 per tweet, uncapped 1x cash ($205,000 peak cash).
- **When It Sells / Exits:** No stops/targets; holds to Nov 25 close (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_k_tw` |
| `name` | `Variant K-TW · Tweets Only` |
| `group` | `ablation` |
| `bypass_market_filters` | `True` |
| `allow_duplicates` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_k_tw.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_k_tw
python3 run_backtest.py --variant variant_k_tw --capital 10000
```
