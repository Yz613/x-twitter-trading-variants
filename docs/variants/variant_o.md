# Variant O · Sure-Thing Stack ($15k Max)

- **ID:** `variant_o`
- **Stage / Group:** Stage 4 · Concentration & Velocity (`core`)
- **Verdict:** Concentration Test
- **Reported Study Benchmark:** +$13,604 net (+9.89% ROC) · 88.2% WR · PF 18.44 · 17 trades
- **Executable Code:** [`variants/variant_o.py`](../../variants/variant_o.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests stacking up to $15k notional on top-conviction winners in the Sure-Thing book.
- **How It Trades:** Same filters as Variant N with larger $15k max stacking on winners.
- **When It Buys / Shorts:** +10m/+20m fills on Tier 4-5 catalysts + profitable add-on stacking.
- **How Much It Bets:** Up to $15,000 max per position ($137,500 peak cash).
- **When It Sells / Exits:** Opposite tweet or Nov 25 close, net of slippage and short borrow.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_o` |
| `name` | `Variant O · Sure-Thing $15k` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `4` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `ban_bear_longs` | `True` |
| `allow_duplicates` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_o.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_o
python3 run_backtest.py --variant variant_o --capital 10000
```
