# Variant S · 0.25x Quarter-Kelly + Strict Correlation Gate (rho <= 0.45)

- **ID:** `variant_s`
- **Stage / Group:** Stage 5 · Live 30-Day Rules (`core`)
- **Verdict:** Too Restrictive
- **Reported Study Benchmark:** +$742 (+2.97% / 30d) · 75.0% WR · -1.65% DD · 3.32 Sharpe · 4 trades
- **Executable Code:** [`variants/variant_s.py`](../../variants/variant_s.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests protecting a live $25k compounding account from correlated sector squeezes using a strict 60-day rho <= 0.45 cap.
- **How It Trades:** Restricted strictly to liquid hours (8:30am-4pm ET), 0.25x Quarter-Kelly sizing, rho <= 0.45 gate, and 4 automated exits.
- **When It Buys / Shorts:** +10m/+20m fills between 8:30am-4pm ET if 60d correlation <= 0.45 with open book.
- **How Much It Bets:** 0.25x Quarter-Kelly (~16% live equity/trade; $8,432 peak notional).
- **When It Sells / Exits:** +20% target, -15% closing catastrophe stop, Day-5 <+2% cut, opposite tweet, or 15-20d max.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_s` |
| `name` | `Variant S · Q-Kelly + Corr` |
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
| `day5_dead_money_cut` | `True` |
| `max_hold_days` | `15` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_s.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_s
python3 run_backtest.py --variant variant_s --capital 10000
```
