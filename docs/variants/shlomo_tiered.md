# Shlomo-Tiered · Score-Sized Floor >= 5.0

- **ID:** `shlomo_tiered`
- **Stage / Group:** Shlomo Suite · Peak Shlomo Dollars (`shlomo`)
- **Verdict:** Peak Shlomo Dollars
- **Reported Study Benchmark:** +$14,272 (+10.57% ROC) · 75.0% WR · PF 5.74 · 24 trades
- **Executable Code:** [`variants/shlomo_tiered.py`](../../variants/shlomo_tiered.py)

---

## Plain-English Breakdown

- **Why It Trades:** Uses Shlomo's 8-metric score itself for position sizing — betting 4x larger on elite (>=5.75) tickets than borderline (5.00-5.24) tickets.
- **How It Trades:** Takes every tweet >= 5.0 / 10 and scales bet size across 3 score tiers without needing SPY 20-SMA or ATR filters.
- **When It Buys / Shorts:** Enters Long or Short at next open on all tweets scoring >= 5.0 / 10 (24 trades).
- **How Much It Bets:** Score >= 5.75 -> $10k · 5.25-5.74 -> $5k · 5.00-5.24 -> $2.5k ($135,000 peak cash).
- **When It Sells / Exits:** Holds to Nov 25 close (5d hold alternative: +$10,137 / +14.48% ROC / PF 7.77), net of slippage & borrow.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `shlomo_tiered` |
| `name` | `Shlomo-Tiered · >=5.0 Sized` |
| `group` | `shlomo` |
| `shlomo_min_score` | `5.0` |
| `bypass_market_filters` | `True` |
| `allow_duplicates` | `True` |
| `sizing_mode` | `shlomo_tiered` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/shlomo_tiered.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant shlomo_tiered
python3 run_backtest.py --variant shlomo_tiered --capital 10000
```
