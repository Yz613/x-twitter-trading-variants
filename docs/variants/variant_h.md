# Variant H · Profitable Add-On Only (No Stops)

- **ID:** `variant_h`
- **Stage / Group:** Stage 3 · Surgical Filters & Regime (`core`)
- **Verdict:** Kept Feature
- **Reported Study Benchmark:** +$13,519 (+8.45% ROC) · 69.2% WR · PF 6.24 · 39 trades
- **Executable Code:** [`variants/variant_h.py`](../../variants/variant_h.py)

---

## Plain-English Breakdown

- **Why It Trades:** Unbundled Variant G by deleting the losing stops while keeping the winning profitable add-on rule.
- **How It Trades:** Exact Variant F engine plus 1 pyramid add-on only when existing position is already in profit.
- **When It Buys / Shorts:** +10m/+20m fills on T1-T5 signals + 1 profitable add-on on follow-up same-side tweet.
- **How Much It Bets:** T1-T5 sizing ($20-$10k) + 1 profitable add-on ($160,040 deployed).
- **When It Sells / Exits:** No price stops. Exits on opposite tweet or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_h` |
| `name` | `Variant H · Profitable Add-On` |
| `group` | `core` |
| `direct_only` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `allow_duplicates` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_h.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_h
python3 run_backtest.py --variant variant_h --capital 10000
```
