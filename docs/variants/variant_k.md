# Variant K · SPY 20-SMA Regime Gate

- **ID:** `variant_k`
- **Stage / Group:** Stage 3 · Champion (Peak Raw Dollars) (`core`)
- **Verdict:** Stage 3 Champion
- **Reported Study Benchmark:** +$15,184 (+10.35% ROC, 81.2% WR, PF 18.45, 32 trades; Net Cont: +$14,214 / +10.28%)
- **Executable Code:** [`variants/variant_k.py`](../../variants/variant_k.py)

---

## Plain-English Breakdown

- **Why It Trades:** Buying news in a bear tape gets faded. Gates direction and sizing using SPY vs. its 20-day moving average.
- **How It Trades:** Combines all Stage 1-3 filters with SPY 20-SMA regime sizing: slash longs when SPY < 20-SMA; halve T2-T3 shorts when SPY >= 20-SMA.
- **When It Buys / Shorts:** +10m/+20m fills on T2-T5 direct signals passing gap, tape, IPO, and SPY 20-SMA checks.
- **How Much It Bets:** Tier 2-5 sizing adjusted by SPY regime + 1 profitable add-on ($142k peak cash).
- **When It Sells / Exits:** No tight stops. Exits on opposite tweet or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_k` |
| `name` | `Variant K · SPY 20-SMA Regime` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `2` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_k.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_k
python3 run_backtest.py --variant variant_k --capital 10000
```
