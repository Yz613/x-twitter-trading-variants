# Variant J · Tape Confirmation, IPO & Tier-1 Fixes

- **ID:** `variant_j`
- **Stage / Group:** Stage 3 · Surgical Filters & Regime (`core`)
- **Verdict:** Kept Filters
- **Reported Study Benchmark:** +$14,392 (+9.44% ROC) · 76.5% WR · PF 9.66 · 34 trades
- **Executable Code:** [`variants/variant_j.py`](../../variants/variant_j.py)

---

## Plain-English Breakdown

- **Why It Trades:** Plugged three loopholes in H: vague Tier 1 noise, Day-1 IPO hype (ANT), and shorting stocks rallying through bad news (TSLA).
- **How It Trades:** Requires Tier >= 2, tape confirmation (no shorting >+1% green stocks), and skips Day-1 IPOs >3% above offer.
- **When It Buys / Shorts:** +10m/+20m fills on T2-T5 signals passing tape & IPO checks.
- **How Much It Bets:** Full Tier 2-5 sizing ($500-$10k) + 1 profitable add-on ($152,500 deployed).
- **When It Sells / Exits:** No price stops. Exits on opposite tweet or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_j` |
| `name` | `Variant J · Tape & IPO Fixes` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `2` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_j.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_j
python3 run_backtest.py --variant variant_j --capital 10000
```
