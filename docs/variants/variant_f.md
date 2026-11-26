# Variant F · Fast 10-20m Fills + 5 Conviction Tiers

- **ID:** `variant_f`
- **Stage / Group:** Stage 2 · Fast Fills + Tiers (`core`)
- **Verdict:** Stage 2 Winner
- **Reported Study Benchmark:** +$10,133 (+7.31% ROC) · 65.7% WR · PF 4.93 · 35 trades
- **Executable Code:** [`variants/variant_f.py`](../../variants/variant_f.py)

---

## Plain-English Breakdown

- **Why It Trades:** Waiting until 9:30 a.m. missed initial news drift, and flat $10k bets treated vague sentiment the same as concrete SEC probes and hacks.
- **How It Trades:** Grades catalysts from Tier 1 (vague) to Tier 5 (hard shock) and enters +10m after tweet (+20m if >2% spike) including extended hours.
- **When It Buys / Shorts:** +10m (+20m cooldown if >2% initial spike) after direct catalyst passing Rules 1-3.
- **How Much It Bets:** Tier-mapped: T5=$10k, T4=$5k, T3=$2k, T2=$500, T1=$20 ($138,540 deployed across 35 trades).
- **When It Sells / Exits:** No price stops. Exits on opposite tweet or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_f` |
| `name` | `Variant F · Fast Fills + Tiers` |
| `group` | `core` |
| `direct_only` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_f.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_f
python3 run_backtest.py --variant variant_f --capital 10000
```
