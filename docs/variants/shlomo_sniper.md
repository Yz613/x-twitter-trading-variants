# Shlomo-Sniper · >= 5.5 + Early/No-Conflict ($25k 2x 5d)

- **ID:** `shlomo_sniper`
- **Stage / Group:** Shlomo Suite · Best ROC (#2 Overall) (`shlomo`)
- **Verdict:** Best Shlomo ROC (#2 Overall)
- **Reported Study Benchmark:** +$5,943 (+23.77% ROC) · 77.8% WR · PF 8.29 · 9 trades
- **Executable Code:** [`variants/shlomo_sniper.py`](../../variants/shlomo_sniper.py)

---

## Plain-English Breakdown

- **Why It Trades:** Pairs Shlomo's highest-conviction rubric gate (>= 5.5 + fresh entry >= 4.5 + no conflict >= 5.0) with a $25k 2x 5-day recycler.
- **How It Trades:** Requires 8-metric composite >= 5.5, fresh entry_quality >= 4.5, and conflict_check >= 5.0; recycles $5k slots every 5 days.
- **When It Buys / Shorts:** Enters Long or Short at next open when all 3 rubric gates pass and a slot is open (9 trades).
- **How Much It Bets:** $5,000 cash / $10,000 notional (2x Reg-T margin), hard-capped at $25,000 cash.
- **When It Sells / Exits:** First of +20% daily close target or 5 trading sessions (net of slippage, 3% borrow, 6.5% margin).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `shlomo_sniper` |
| `name` | `Shlomo-Sniper · 2x 5d` |
| `group` | `shlomo` |
| `shlomo_min_score` | `5.5` |
| `min_entry_quality` | `4.5` |
| `min_conflict_check` | `5.0` |
| `bypass_market_filters` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `cash_cap` | `25000.0` |
| `leverage` | `2.0` |
| `profit_target_pct` | `0.2` |
| `max_hold_days` | `5` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/shlomo_sniper.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant shlomo_sniper
python3 run_backtest.py --variant shlomo_sniper --capital 10000
```
