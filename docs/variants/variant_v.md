# Variant V · 0.25x Quarter-Kelly Live Engine (No Hard rho Cap)

- **ID:** `variant_v`
- **Stage / Group:** Stage 5 · Champion (Live Rules) (`core`)
- **Verdict:** Stage 5 Champion
- **Reported Study Benchmark:** +$2,365 (+9.46% / 30d) · 75.0% WR · -2.99% DD · 4.66 Sharpe · PF 17.86 · 8 trades
- **Executable Code:** [`variants/variant_v.py`](../../variants/variant_v.py)

---

## Plain-English Breakdown

- **Why It Trades:** Removes Variant S's overly tight rho <= 0.45 cap so live Quarter-Kelly compounding can capture clustered theme shocks.
- **How It Trades:** 8:30am-4pm ET liquid hours, 0.25x Quarter-Kelly compounding, and a 4-trigger automated exit engine.
- **When It Buys / Shorts:** +10m/+20m fills between 8:30am-4pm ET on qualifying Stage 3-4 catalysts (8 trades in 30d).
- **How Much It Bets:** 0.25x Quarter-Kelly (~16% live equity/trade, max 80% deployed; $16,910 peak notional).
- **When It Sells / Exits:** +20% daily close target, -15% closing catastrophe stop, opposite tweet, or 15d max hold.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_v` |
| `name` | `Variant V · Q-Kelly Live` |
| `group` | `core` |
| `window_start` | `2026-10-26` |
| `direct_only` | `True` |
| `min_tier` | `4` |
| `min_atr_pct` | `3.2` |
| `crypto_exempt` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `ban_bear_longs` | `True` |
| `sizing_mode` | `fractional_kelly` |
| `kelly_fraction_t5` | `0.16` |
| `kelly_fraction_t4` | `0.12` |
| `cash_cap` | `25000.0` |
| `leverage` | `1.0` |
| `profit_target_pct` | `0.2` |
| `catastrophe_stop_pct` | `0.15` |
| `max_hold_days` | `15` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_v.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_v
python3 run_backtest.py --variant variant_v --capital 10000
```
