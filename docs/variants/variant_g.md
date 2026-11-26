# Variant G · Fast Fills + Stops & Add-On Bundle

- **ID:** `variant_g`
- **Stage / Group:** Stage 2 · Fast Fills + Tiers (`core`)
- **Verdict:** Split · Stops Cut
- **Reported Study Benchmark:** Oct +$6,334 / Nov +$3,137 · 39 trades (20 Oct / 19 Nov)
- **Executable Code:** [`variants/variant_g.py`](../../variants/variant_g.py)

---

## Plain-English Breakdown

- **Why It Trades:** Tested adding 12% close stop + 10% trailing stop + 1 profitable add-on on top of Variant F.
- **How It Trades:** Bundled trailing/close stops with profitable pyramiding; stops cost -$4,048 while add-ons went 4-for-4 (+$3,386).
- **When It Buys / Shorts:** Same as Variant F, plus 1 add-on leg if a follow-up same-side tweet hits while trade is green.
- **How Much It Bets:** T1-T5 tier sizing ($20-$10k), capped at $10k per ticker.
- **When It Sells / Exits:** -12% daily close stop, 10% trailing stop (after +10% gain), opposite tweet, or Nov 25 close.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_g` |
| `name` | `Variant G · Stops + Add-On` |
| `group` | `core` |
| `direct_only` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `catastrophe_stop_pct` | `0.12` |
| `trailing_stop_pct` | `0.1` |
| `sizing_mode` | `tier_map` |
| `leverage` | `1.0` |
| `net_of_fees` | `False` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_g.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_g
python3 run_backtest.py --variant variant_g --capital 10000
```
