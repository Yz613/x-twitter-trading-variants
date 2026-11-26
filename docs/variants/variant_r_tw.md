# Variant R-TW · Tweets Only (Zero Market Filters)

- **ID:** `variant_r_tw`
- **Stage / Group:** Top-3 Ablation · Tweets-Only (No Market Filters) (`ablation`)
- **Verdict:** Ablation · Tweets Only
- **Reported Study Benchmark:** -$2,162 (-8.65% ROC) · 40.0% WR · PF 0.40 · -14.36% DD · 5 trades
- **Executable Code:** [`variants/variant_r_tw.py`](../../variants/variant_r_tw.py)

---

## Plain-English Breakdown

- **Why It Trades:** Inverse test of R-MKT: strips away ALL market filters and feeds raw chronological tweets into Variant R's $25k 2x engine.
- **How It Trades:** Takes every chronological @KobeissiLetter directional tweet regardless of ATR, gap, tape, proxy ETF, or SPY regime.
- **When It Buys / Shorts:** Enters Long or Short at next open whenever one of 5 cash slots is open.
- **How Much It Bets:** $5,000 cash / $10,000 notional (2x margin), capped at $25,000 cash.
- **When It Sells / Exits:** +20% daily close target or Nov 25 close (net of slippage, 3% borrow, 6.5% margin).

## Exact Frozen Parameters

| Parameter | Value |
|---|---|
| `id` | `variant_r_tw` |
| `name` | `Variant R-TW · Tweets Only` |
| `group` | `ablation` |
| `bypass_market_filters` | `True` |
| `allow_duplicates` | `True` |
| `sizing_mode` | `fixed_cash` |
| `cash_per_trade` | `5000.0` |
| `cash_cap` | `25000.0` |
| `leverage` | `2.0` |
| `profit_target_pct` | `0.2` |
| `net_of_fees` | `True` |

## How to Run This Variant

```bash
# Run standalone
python3 variants/variant_r_tw.py

# Or via the unified CLI (with optional custom bankroll)
python3 run_backtest.py --variant variant_r_tw
python3 run_backtest.py --variant variant_r_tw --capital 10000
```
