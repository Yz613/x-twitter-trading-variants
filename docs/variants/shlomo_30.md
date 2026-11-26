# Shlomo · Original Floor >= 3.0 (5-Day Hold)

- **ID:** `shlomo_30`
- **Stage / Group:** Shlomo Suite · 8-Metric Rubric (`shlomo`)
- **Verdict:** Shlomo Baseline
- **Reported Study Benchmark:** +$8,032 (+10.71% ROC) · 58.5% WR · PF 3.01 · 41 trades
- **Executable Code:** [`variants/shlomo_30.py`](../../variants/shlomo_30.py)

---

## Plain-English Breakdown

- **Why It Trades:** Applies Shlomo's 8-metric ticket-quality rubric (0-10 equal weight, publish floor >= 3.0) with his recommended 5-session fixed hold.
- **How It Trades:** Scores clarity, specificity, trigger, evidence, horizon, invalidation, objective entry_quality, and objective conflict_check.
- **When It Buys / Shorts:** Enters Long or Short at next open on every tweet clearing >= 3.0 / 10 (all 41 tweets passed).
- **How Much It Bets:** Flat $5,000 cash (1x; $75,000 peak cash on 5d hold).
- **When It Sells / Exits:** Exits strictly at close of the 5th trading session (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `shlomo_30` |
| `name` | `Shlomo · Floor >= 3.0` |
| `group` | `shlomo` |
| `shlomo_min_score` | `3.0` |
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
python3 variants/shlomo_30.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant shlomo_30
python3 run_backtest.py --variant shlomo_30 --capital 10000
```
