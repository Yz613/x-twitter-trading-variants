# Variant X · Hybrid Live Playbook (Synthesis of Stages 0-5)

- **ID:** `variant_x`
- **Stage / Group:** Final Production Blueprint (`core`)
- **Verdict:** Recommended Live Spec
- **Reported Study Benchmark:** Target Bankroll: $25k-$30k (Untested live blueprint; backtestable via simulator)
- **Executable Code:** [`variants/variant_x.py`](../../variants/variant_x.py)

---

## Plain-English Breakdown

- **Why It Trades:** Synthesizes every edge-positive rule across Stages 0-5 while cutting every rule that leaked money.
- **How It Trades:** Monitors @KobeissiLetter across extended hours (4am-8pm ET), focusing on Tier 4-5 fast movers with 0.30x Fractional Kelly + soft sector cap.
- **When It Buys / Shorts:** +10m (+20m if >2% spike) on Tier 4-5 direct shocks with ATR >= 3.2% (crypto exempt), no long gaps >3%, tape/IPO confirmed, SPY 20-SMA aligned.
- **How Much It Bets:** 0.30x Fractional Kelly (~20% cash on T5, ~13% on T4; optional 1.5-2x margin on T5) + 1 profitable add-on.
- **When It Sells / Exits:** +20% daily close target, -15% closing catastrophe stop, opposite tweet, or 15-20d max hold.

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_x` |
| `name` | `Variant X · Hybrid Blueprint` |
| `group` | `core` |
| `direct_only` | `True` |
| `min_tier` | `4` |
| `min_atr_pct` | `3.2` |
| `crypto_exempt` | `True` |
| `skip_long_gap_gt_3` | `True` |
| `tape_confirm` | `True` |
| `spy_regime_gate` | `True` |
| `ban_bear_longs` | `True` |
| `sizing_mode` | `fractional_kelly` |
| `kelly_fraction_t5` | `0.2` |
| `kelly_fraction_t4` | `0.13` |
| `cash_cap` | `25000.0` |
| `leverage` | `1.0` |
| `profit_target_pct` | `0.2` |
| `catastrophe_stop_pct` | `0.15` |
| `max_hold_days` | `20` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_x.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_x
python3 run_backtest.py --variant variant_x --capital 10000
```
