# Variant A · Raw Baseline (No Filters)

- **ID:** `variant_a`
- **Stage / Group:** Stage 0 · Unfiltered Baseline (`core`)
- **Verdict:** Baseline Control
- **Reported Study Benchmark:** +$1,402 (+0.45% ROC) · 54.8% WR · 31 trades (Oct)
- **Executable Code:** [`variants/variant_a.py`](../../variants/variant_a.py)

---

## Plain-English Breakdown

- **Why It Trades:** Zero-rule control test to see if raw @KobeissiLetter headlines have standalone alpha before adding guardrails.
- **How It Trades:** Reads every original October post, maps any directional headline to a stock or proxy ETF, and takes every single one including duplicates.
- **When It Buys / Shorts:** Next morning 9:30 a.m. ET open after every directional tweet. Never skips gaps, proxy ETFs, or repeat tickers.
- **How Much It Bets:** Flat $10,000 per trade (1x cash, uncapped; $310,000 gross exposure across 31 trades).
- **When It Sells / Exits:** No stops, no targets, no opposite-tweet flips — holds every trade to Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_a` |
| `name` | `Variant A · Raw Baseline` |
| `group` | `core` |
| `window_start` | `2026-10-09` |
| `window_end` | `2026-11-25` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `10000.0` |
| `leverage` | `1.0` |
| `allow_duplicates` | `True` |
| `bypass_market_filters` | `True` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_a.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_a
python3 run_backtest.py --variant variant_a --capital 10000
```
