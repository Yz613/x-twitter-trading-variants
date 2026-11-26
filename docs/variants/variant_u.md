# Variant U · 0.25x Quarter-Kelly Liquid-Hours Sniper

- **ID:** `variant_u`
- **Stage / Group:** Stage 5 · Live 30-Day Rules (`core`)
- **Verdict:** Starved of Trades
- **Reported Study Benchmark:** +$755 (+3.02% / 30d) · 100.0% WR (1/1) · 3.57 Sharpe · 1 trade
- **Executable Code:** [`variants/variant_u.py`](../../variants/variant_u.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tests Variant R's strict sniper rules inside Stage 5's 8:30am-4pm ET liquid-hours box.
- **How It Trades:** Tier 4-5 + ATR >= 3.2% + 0.25x Kelly + zero after-hours entries.
- **When It Buys / Shorts:** +10m/+20m fills strictly during 8:30am-4pm ET on Tier 5 high-velocity shocks.
- **How Much It Bets:** 0.25x Quarter-Kelly ($4,219 peak notional).
- **When It Sells / Exits:** +20% target, -15% catastrophe stop, opposite tweet, or 15-20d max hold.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_u` |
| `name` | `Variant U · Q-Kelly Sniper` |
| `group` | `core` |
| `window_start` | `2026-10-26` |
| `direct_only` | `True` |
| `min_tier` | `5` |
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
python3 variants/variant_u.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_u
python3 run_backtest.py --variant variant_u --capital 10000
```
