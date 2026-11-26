# Shlomo-5.50 · Precision Floor >= 5.50 (1x 5d)

- **ID:** `shlomo_550`
- **Stage / Group:** Shlomo Suite · Peak Shlomo Win Rate (`shlomo`)
- **Verdict:** Peak Shlomo WR (83.3%)
- **Reported Study Benchmark:** +$3,648 (+12.16% ROC) · 83.3% WR · PF 10.09 · 12 trades
- **Executable Code:** [`variants/shlomo_550.py`](../../variants/shlomo_550.py)

---

## Plain-English Breakdown

- **Why It Trades:** Pushes rubric selectivity to 5.50 / 10 for maximum hit rate and tiny worst-case loss (-$285) on $30k unlevered cash.
- **How It Trades:** Trades only the top ~30% of tweets by 8-metric quality with a 5-session fixed hold.
- **When It Buys / Shorts:** Enters Long or Short at next open on tweets scoring >= 5.50 / 10 (12 trades).
- **How Much It Bets:** Flat $5,000 cash (1x, zero margin; $30,000 peak cash).
- **When It Sells / Exits:** Exits strictly at close of the 5th trading session (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `shlomo_550` |
| `name` | `Shlomo-5.50 · Precision 1x` |
| `group` | `shlomo` |
| `shlomo_min_score` | `5.5` |
| `bypass_market_filters` | `True` |
| `allow_duplicates` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `leverage` | `1.0` |
| `max_hold_days` | `5` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/shlomo_550.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant shlomo_550
python3 run_backtest.py --variant shlomo_550 --capital 10000
```
