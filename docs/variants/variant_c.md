# Variant C · Guardrails + 8% Intraday Stop

- **ID:** `variant_c`
- **Stage / Group:** Stage 1 · Core Guardrails (`core`)
- **Verdict:** Retired · Hurt P&L
- **Reported Study Benchmark:** Nov OOS: +$3,592 (+2.11% ROC) · 47.1% WR · 41 trades (24 Oct / 17 Nov)
- **Executable Code:** [`variants/variant_c.py`](../../variants/variant_c.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tested whether an 8% intraday stop-loss and 10-day max hold would protect Variant B from blowups.
- **How It Trades:** Identical entry guardrails to Variant B, plus mechanical 8% intraday stop and 10-trading-day time exit.
- **When It Buys / Shorts:** Same as Variant B: direct ticker, <=3% long gap, max 1 per ticker at next 9:30 a.m. open.
- **How Much It Bets:** Flat $10,000 per trade (1x cash).
- **When It Sells / Exits:** First of: -8% intraday stop-loss, 10 trading days max hold, opposite tweet, or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_c` |
| `name` | `Variant C · 8% Intraday Stop` |
| `group` | `core` |
| `direct_only` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `intraday_stop_pct` | `0.08` |
| `max_hold_days` | `10` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `10000.0` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_c.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_c
python3 run_backtest.py --variant variant_c --capital 10000
```
