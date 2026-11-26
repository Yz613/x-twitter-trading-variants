# Variant B · Core Guardrails (Rules 1-3)

- **ID:** `variant_b`
- **Stage / Group:** Stage 1 · Core Guardrails (`core`)
- **Verdict:** Stage 1 Winner
- **Reported Study Benchmark:** Nov OOS: +$7,132 (+4.20% ROC) · 64.7% WR · 41 trades (24 Oct / 17 Nov)
- **Executable Code:** [`variants/variant_b.py`](../../variants/variant_b.py)

---

## Plain-English Breakdown

- **Why It Trades:** Fixes Variant A's three worst leaks: chasing >3% overnight long gaps, trading noisy proxy ETFs, and stacking accidental duplicates.
- **How It Trades:** Trades only directly named companies/assets, caps at 1 open position per ticker, and flips/closes on opposite headlines.
- **When It Buys / Shorts:** Next-day 9:30 a.m. open if direct stock/crypto, not already held same-side, and (for Longs) gap <= +3%.
- **How Much It Bets:** Flat $10,000 per trade (1x cash, uncapped; $170,000 gross in Nov OOS).
- **When It Sells / Exits:** Opposite tweet closes/flips position; otherwise hold to Nov 25 close (no price stops).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_b` |
| `name` | `Variant B · Core Guardrails` |
| `group` | `core` |
| `direct_only` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `10000.0` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_b.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_b
python3 run_backtest.py --variant variant_b --capital 10000
```
