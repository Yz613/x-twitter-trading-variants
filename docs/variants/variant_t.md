# Variant T · 0.50x Half-Kelly + Correlation Gate + ATR Runner

- **ID:** `variant_t`
- **Stage / Group:** Stage 5 · Live 30-Day Rules (`core`)
- **Verdict:** Lower Sharpe vs. S
- **Reported Study Benchmark:** +$1,245 (+4.98% / 30d) · 75.0% WR · -3.27% DD · 2.41 Sharpe · 4 trades
- **Executable Code:** [`variants/variant_t.py`](../../variants/variant_t.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests doubling Kelly sizing to 0.50x (Half-Kelly); doubled drawdown and lowered Sharpe vs. Quarter-Kelly.
- **How It Trades:** Same 8:30-4:00 ET liquid hours and rho <= 0.45 gate as S, with 2x larger bets.
- **When It Buys / Shorts:** Identical to Variant S (4 trades in 30d).
- **How Much It Bets:** 0.50x Half-Kelly (~32% live equity/trade; $16,852 peak notional).
- **When It Sells / Exits:** ATR runner exit, -15% catastrophe stop, Day-5 cut, opposite tweet, or max hold.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_t` |
| `name` | `Variant T · Half-Kelly` |
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
| `kelly_fraction_t5` | `0.32` |
| `kelly_fraction_t4` | `0.24` |
| `cash_cap` | `25000.0` |
| `leverage` | `1.0` |
| `catastrophe_stop_pct` | `0.15` |
| `day5_dead_money_cut` | `True` |
| `max_hold_days` | `20` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_t.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_t
python3 run_backtest.py --variant variant_t --capital 10000
```
