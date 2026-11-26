# Variant N · Sure-Thing Tiers ($10k Max)

- **ID:** `variant_n`
- **Stage / Group:** Stage 4 · Concentration & Velocity (`core`)
- **Verdict:** Concentration Test
- **Reported Study Benchmark:** +$12,429 net (+9.38% ROC) · 87.5% WR · PF 16.93 · 16 trades
- **Executable Code:** [`variants/variant_n.py`](../../variants/variant_n.py)

---

## Plain-English Breakdown

- **Why It Trades:** Concentrates Variant M strictly into high-conviction Sure-Thing setups capped at $10k/trade.
- **How It Trades:** Drops lower-tier noise and focuses exclusively on top corporate/crypto shocks.
- **When It Buys / Shorts:** +10m/+20m fills on high-conviction Tier 4-5 catalysts passing Variant M filters.
- **How Much It Bets:** Up to $10,000 max per trade ($132,500 peak cash).
- **When It Sells / Exits:** Opposite tweet or Nov 25 close, net of slippage and short borrow.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_n` |
| `name` | `Variant N · Sure-Thing $10k` |
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
python3 variants/variant_n.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_n
python3 run_backtest.py --variant variant_n --capital 10000
```
