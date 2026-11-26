# Variant R · $25k 2x Margin Sniper

- **ID:** `variant_r`
- **Stage / Group:** Stage 4 · Champion (Peak Cash Efficiency) (`core`)
- **Verdict:** Stage 4 Champion (#1 ROC)
- **Reported Study Benchmark:** +$7,816 net (+31.26% ROC) · 100.0% WR (5/5) · PF INF · 5 trades
- **Executable Code:** [`variants/variant_r.py`](../../variants/variant_r.py)

---

## Plain-English Breakdown

- **Why It Trades:** Combines Tier 4-5 hard shocks + ATR >= 3.2% velocity with 2x Reg-T margin on a $25k cash cap and drops the Day-5 cut.
- **How It Trades:** Ultra-selective sniper: only top-tier shocks on fast movers/crypto, $5k cash -> $10k notional (2x), recycling cash at +20%.
- **When It Buys / Shorts:** +10m/+20m fills on Tier 4-5 catalysts with 14d ATR >= 3.2% (or crypto) when one of 5 slots is open.
- **How Much It Bets:** $5,000 cash / $10,000 notional (2x Reg-T margin), hard-capped at $25,000 peak cash.
- **When It Sells / Exits:** +20% daily close target, opposite tweet, or 20d max hold (net of 0.10%/leg slippage, 3% borrow, 6.5% margin).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_r` |
| `name` | `Variant R · $25k 2x Sniper` |
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
| `cash_cap` | `25000.0` |
| `leverage` | `2.0` |
| `profit_target_pct` | `0.2` |
| `max_hold_days` | `20` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_r.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_r
python3 run_backtest.py --variant variant_r --capital 10000
```
