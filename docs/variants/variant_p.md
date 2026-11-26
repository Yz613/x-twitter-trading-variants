# Variant P · Tier 4-5 Sniper Only (Uncapped)

- **ID:** `variant_p`
- **Stage / Group:** Stage 4 · Concentration & Velocity (`core`)
- **Verdict:** Precursor to R
- **Reported Study Benchmark:** +$12,342 net (+9.49% ROC) · 86.7% WR · PF 16.82 · 15 trades
- **Executable Code:** [`variants/variant_p.py`](../../variants/variant_p.py)

---

## Plain-English Breakdown

- **Why It Trades:** Isolates purely Tier 4-5 hard shocks across all ATRs before imposing a small-account cash cap.
- **How It Trades:** Waits strictly for undeniable hard catalysts (SEC probes, hacks, earnings misses) across all velocities.
- **When It Buys / Shorts:** +10m/+20m fills on Tier 4-5 shocks only.
- **How Much It Bets:** T4=$5k / T5=$10k, uncapped cash ($130,000 peak cash).
- **When It Sells / Exits:** Opposite tweet or Nov 25 close, net of slippage and short borrow.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_p` |
| `name` | `Variant P · T4-5 Uncapped` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `4` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `ban_bear_longs` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_p.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_p
python3 run_backtest.py --variant variant_p --capital 10000
```
