# Variant Q · $30k Unlevered Velocity Recycler

- **ID:** `variant_q`
- **Stage / Group:** Stage 4 · Small-Bankroll Velocity (`core`)
- **Verdict:** Small-Cash 1x Winner
- **Reported Study Benchmark:** +$3,778 net (+12.59% ROC) · 85.7% WR · PF 5.74 · 7 trades
- **Executable Code:** [`variants/variant_q.py`](../../variants/variant_q.py)

---

## Plain-English Breakdown

- **Why It Trades:** Runs the strategy on a realistic $30,000 unlevered cash account by requiring fast movers (ATR >= 3.2% or crypto) and recycling cash at +20%.
- **How It Trades:** Skips slow stocks (<3.2% ATR), caps total cash at $30k ($5k/trade, max 6 open), takes profit at +20%, and cuts dead money on Day 5 (<+2%).
- **When It Buys / Shorts:** +10m/+20m fills on Tier 4-5 fast movers (ATR >= 3.2% or crypto) when a $5k slot is open.
- **How Much It Bets:** Flat $5,000 cash (1x, no margin), hard-capped at $30,000.
- **When It Sells / Exits:** +20% daily close target, Day-5 <+2% cut, opposite tweet, or 20d max hold (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_q` |
| `name` | `Variant Q · $30k 1x Recycler` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `4` |
| `min_atr_pct` | `3.2` |
| `crypto_exempt` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `ban_bear_longs` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `cash_cap` | `30000.0` |
| `leverage` | `1.0` |
| `profit_target_pct` | `0.2` |
| `day5_dead_money_cut` | `True` |
| `max_hold_days` | `20` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_q.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_q
python3 run_backtest.py --variant variant_q --capital 10000
```
