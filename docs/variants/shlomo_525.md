# Shlomo-5.25 · Sweet-Spot Floor >= 5.25 (1x 5d)

- **ID:** `shlomo_525`
- **Stage / Group:** Shlomo Suite · Best 1x ROC Overall (`shlomo`)
- **Verdict:** Best Unlevered 1x ROC
- **Reported Study Benchmark:** +$7,641 (+16.98% ROC) · 77.8% WR · PF 10.37 · 18 trades
- **Executable Code:** [`variants/shlomo_525.py`](../../variants/shlomo_525.py)

---

## Plain-English Breakdown

- **Why It Trades:** Raises Shlomo's floor to the 5.25 inflection point that drops proxy/rumor noise without starving top winners.
- **How It Trades:** Pure equal-weight 8-metric rubric >= 5.25 with zero leverage and a 5-session fixed hold.
- **When It Buys / Shorts:** Enters Long or Short at next open on tweets scoring >= 5.25 / 10 (18 trades).
- **How Much It Bets:** Flat $5,000 cash (1x, zero margin; $45,000 peak cash).
- **When It Sells / Exits:** Exits strictly at close of the 5th trading session (net of slippage & borrow).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `shlomo_525` |
| `name` | `Shlomo-5.25 · Sweet-Spot 1x` |
| `group` | `shlomo` |
| `shlomo_min_score` | `5.25` |
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
python3 variants/shlomo_525.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant shlomo_525
python3 run_backtest.py --variant shlomo_525 --capital 10000
```
