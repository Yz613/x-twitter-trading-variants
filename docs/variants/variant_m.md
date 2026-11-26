# Variant M · Max Win Rate (Quality Floor + Bear Long Ban)

- **ID:** `variant_m`
- **Stage / Group:** Stage 4 · Champion (Peak Win Rate) (`core`)
- **Verdict:** Stage 4 Peak WR Champion
- **Reported Study Benchmark:** +$12,055 net (+9.57% ROC) · 90.5% WR · PF 22.32 · 21 trades
- **Executable Code:** [`variants/variant_m.py`](../../variants/variant_m.py)

---

## Plain-English Breakdown

- **Why It Trades:** Eliminates remaining commodity chatter, slow bond ETFs, and all bear-tape longs to maximize precision.
- **How It Trades:** Variant K's continuous net-of-fees book with zero commodity/bond ETFs and a hard ban on Longs when SPY < 20-SMA.
- **When It Buys / Shorts:** +10m/+20m fills on clean equity/crypto catalysts; zero Longs in bear tape.
- **How Much It Bets:** Tier 2-5 sizing, uncapped cash ($126,000 peak cash).
- **When It Sells / Exits:** Opposite tweet or Nov 25 close, net of 0.10%/leg slippage and 3% short borrow.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_m` |
| `name` | `Variant M · Max Win Rate` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `2` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `ban_bear_longs` | `True` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_m.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_m
python3 run_backtest.py --variant variant_m --capital 10000
```
