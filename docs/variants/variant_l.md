# Variant L · ATR Inverse Volatility Down-Sizing

- **ID:** `variant_l`
- **Stage / Group:** Stage 3 · Surgical Filters & Regime (`core`)
- **Verdict:** Retired · Hurt P&L
- **Reported Study Benchmark:** +$9,809 net (+8.79% ROC) · 81.2% WR · PF 12.61 · 32 trades
- **Executable Code:** [`variants/variant_l.py`](../../variants/variant_l.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tested risk-parity inverse-ATR sizing; backfired (-$4,928) because volatile stocks ARE the catalyst profit engine.
- **How It Trades:** Exact same 32 entries as Variant K, scaled down on high-ATR movers and audited net of slippage & borrow.
- **When It Buys / Shorts:** Identical to Variant K (32 trades).
- **How Much It Bets:** Tier size inversely scaled by 14d ATR ($111,535 deployed).
- **When It Sells / Exits:** Opposite tweet or Nov 25 close, net of 0.10%/leg slippage and 3% borrow.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_l` |
| `name` | `Variant L · ATR Down-Size` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `2` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `3500.0` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_l.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_l
python3 run_backtest.py --variant variant_l --capital 10000
```
