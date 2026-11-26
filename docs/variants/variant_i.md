# Variant I · 50/50 Scale-In & 15% Scale-Out

- **ID:** `variant_i`
- **Stage / Group:** Stage 3 · Surgical Filters & Regime (`core`)
- **Verdict:** Retired · Hurt P&L
- **Reported Study Benchmark:** +$12,662 (+8.36% ROC) · 69.2% WR · PF 6.53 · 39 trades
- **Executable Code:** [`variants/variant_i.py`](../../variants/variant_i.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tested whether easing in 50/50 and trimming at +15% smoothed risk; cost -$857 vs. Variant H.
- **How It Trades:** Same filters as Variant H, splitting entry 50/50 and taking partial profit at +15%.
- **When It Buys / Shorts:** 50% at +10m/+20m, remaining 50% scaled in later.
- **How Much It Bets:** Half initial tier size scaling up to full tier ($151,540 deployed).
- **When It Sells / Exits:** Trim partial size at +15% profit; hold rest to opposite tweet or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_i` |
| `name` | `Variant I · 50/50 Scale` |
| `group` | `core` |
| `direct_only` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `profit_target_pct` | `0.15` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_i.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_i
python3 run_backtest.py --variant variant_i --capital 10000
```
