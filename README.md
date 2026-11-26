# X/Twitter Event-Driven Trading Variants (All 32 Models)

Complete, reproducible, zero-dependency Python 3 repository containing the **exact executable code** and **separate documentation** for every trading variant tested across the `@KobeissiLetter` 6-Iteration Research Study, the Top-3 Market-Only vs. Tweets-Only Ablations, and the Shlomo 8-Metric Rubric Suite.

- **Interactive Web Report & Leaderboard:** https://x-twitter-trading-report.yehudazahler.workers.dev/#leaderboard
- **Live Paper Trading Monitor (PredX):** https://predx-monitor.yehudazahler.workers.dev

## Quickstart (Zero External Dependencies)

Uses only the Python 3 standard library + public Yahoo Finance daily OHLC bars (automatically cached in `.cache_ohlc/`):

```bash
git clone https://github.com/Yz613/x-twitter-trading-variants.git
cd x-twitter-trading-variants

# Run all 32 variants and print a ranked leaderboard
python3 run_backtest.py --variant all

# Run a single variant standalone
python3 variants/variant_r.py
python3 variants/shlomo_sniper.py

# Simulate any variant with a custom $10,000 bankroll cap
python3 run_backtest.py --variant shlomo --capital 10000

# Run the automated test suite
python3 -m unittest discover -s tests -v
```

## Repository Structure

```text
├── run_backtest.py           # Unified CLI runner (--variant all|core|shlomo|ablation|<id> --capital 10000)
├── variants/                 # 32 standalone Python files (1 file per variant, each runnable directly)
├── docs/variants/            # 32 separate Markdown docs (how/why/when each variant trades + exact params)
├── engine/                   # Shared Yahoo Finance loader, NYSE holiday calendar, Shlomo 8-metric scorer, simulator
├── data/                     # Exact Oct 9 – Nov 25, 2026 @KobeissiLetter dataset (reproducible with no X API key)
├── scripts/                  # Original verbatim research scripts from the study
└── tests/                    # Automated verification tests for all 32 variants
```

## All 32 Variants (Exact Code + Separate Docs)

| Code | Variant | Group | Reported Study Benchmark | Exact Code | Separate Docs |
|---|---|---|---|---|---|
| **A** | Variant A · Raw Baseline (No Filters) | `core` | +$1,402 (+0.45% ROC) · 54.8% WR · 31 trades (Oct) | [`variants/variant_a.py`](variants/variant_a.py) | [`docs/variants/variant_a.md`](docs/variants/variant_a.md) |
| **B** | Variant B · Core Guardrails (Rules 1-3) | `core` | Nov OOS: +$7,132 (+4.20% ROC) · 64.7% WR · 41 trades (24 Oct / 17 Nov) | [`variants/variant_b.py`](variants/variant_b.py) | [`docs/variants/variant_b.md`](docs/variants/variant_b.md) |
| **C** | Variant C · Guardrails + 8% Intraday Stop | `core` | Nov OOS: +$3,592 (+2.11% ROC) · 47.1% WR · 41 trades (24 Oct / 17 Nov) | [`variants/variant_c.py`](variants/variant_c.py) | [`docs/variants/variant_c.md`](docs/variants/variant_c.md) |
| **F** | Variant F · Fast 10-20m Fills + 5 Conviction Tiers | `core` | +$10,133 (+7.31% ROC) · 65.7% WR · PF 4.93 · 35 trades | [`variants/variant_f.py`](variants/variant_f.py) | [`docs/variants/variant_f.md`](docs/variants/variant_f.md) |
| **G** | Variant G · Fast Fills + Stops & Add-On Bundle | `core` | Oct +$6,334 / Nov +$3,137 · 39 trades (20 Oct / 19 Nov) | [`variants/variant_g.py`](variants/variant_g.py) | [`docs/variants/variant_g.md`](docs/variants/variant_g.md) |
| **H** | Variant H · Profitable Add-On Only (No Stops) | `core` | +$13,519 (+8.45% ROC) · 69.2% WR · PF 6.24 · 39 trades | [`variants/variant_h.py`](variants/variant_h.py) | [`docs/variants/variant_h.md`](docs/variants/variant_h.md) |
| **I** | Variant I · 50/50 Scale-In & 15% Scale-Out | `core` | +$12,662 (+8.36% ROC) · 69.2% WR · PF 6.53 · 39 trades | [`variants/variant_i.py`](variants/variant_i.py) | [`docs/variants/variant_i.md`](docs/variants/variant_i.md) |
| **J** | Variant J · Tape Confirmation, IPO & Tier-1 Fixes | `core` | +$14,392 (+9.44% ROC) · 76.5% WR · PF 9.66 · 34 trades | [`variants/variant_j.py`](variants/variant_j.py) | [`docs/variants/variant_j.md`](docs/variants/variant_j.md) |
| **K** | Variant K · SPY 20-SMA Regime Gate | `core` | +$15,184 (+10.35% ROC, 81.2% WR, PF 18.45, 32 trades; Net Cont: +$14,214 / +10.28%) | [`variants/variant_k.py`](variants/variant_k.py) | [`docs/variants/variant_k.md`](docs/variants/variant_k.md) |
| **L** | Variant L · ATR Inverse Volatility Down-Sizing | `core` | +$9,809 net (+8.79% ROC) · 81.2% WR · PF 12.61 · 32 trades | [`variants/variant_l.py`](variants/variant_l.py) | [`docs/variants/variant_l.md`](docs/variants/variant_l.md) |
| **M** | Variant M · Max Win Rate (Quality Floor + Bear Long Ban) | `core` | +$12,055 net (+9.57% ROC) · 90.5% WR · PF 22.32 · 21 trades | [`variants/variant_m.py`](variants/variant_m.py) | [`docs/variants/variant_m.md`](docs/variants/variant_m.md) |
| **N** | Variant N · Sure-Thing Tiers ($10k Max) | `core` | +$12,429 net (+9.38% ROC) · 87.5% WR · PF 16.93 · 16 trades | [`variants/variant_n.py`](variants/variant_n.py) | [`docs/variants/variant_n.md`](docs/variants/variant_n.md) |
| **O** | Variant O · Sure-Thing Stack ($15k Max) | `core` | +$13,604 net (+9.89% ROC) · 88.2% WR · PF 18.44 · 17 trades | [`variants/variant_o.py`](variants/variant_o.py) | [`docs/variants/variant_o.md`](docs/variants/variant_o.md) |
| **P** | Variant P · Tier 4-5 Sniper Only (Uncapped) | `core` | +$12,342 net (+9.49% ROC) · 86.7% WR · PF 16.82 · 15 trades | [`variants/variant_p.py`](variants/variant_p.py) | [`docs/variants/variant_p.md`](docs/variants/variant_p.md) |
| **Q** | Variant Q · $30k Unlevered Velocity Recycler | `core` | +$3,778 net (+12.59% ROC) · 85.7% WR · PF 5.74 · 7 trades | [`variants/variant_q.py`](variants/variant_q.py) | [`docs/variants/variant_q.md`](docs/variants/variant_q.md) |
| **R** | Variant R · $25k 2x Margin Sniper | `core` | +$7,816 net (+31.26% ROC) · 100.0% WR (5/5) · PF INF · 5 trades | [`variants/variant_r.py`](variants/variant_r.py) | [`docs/variants/variant_r.md`](docs/variants/variant_r.md) |
| **S** | Variant S · 0.25x Quarter-Kelly + Strict Correlation Gate (rho <= 0.45) | `core` | +$742 (+2.97% / 30d) · 75.0% WR · -1.65% DD · 3.32 Sharpe · 4 trades | [`variants/variant_s.py`](variants/variant_s.py) | [`docs/variants/variant_s.md`](docs/variants/variant_s.md) |
| **T** | Variant T · 0.50x Half-Kelly + Correlation Gate + ATR Runner | `core` | +$1,245 (+4.98% / 30d) · 75.0% WR · -3.27% DD · 2.41 Sharpe · 4 trades | [`variants/variant_t.py`](variants/variant_t.py) | [`docs/variants/variant_t.md`](docs/variants/variant_t.md) |
| **U** | Variant U · 0.25x Quarter-Kelly Liquid-Hours Sniper | `core` | +$755 (+3.02% / 30d) · 100.0% WR (1/1) · 3.57 Sharpe · 1 trade | [`variants/variant_u.py`](variants/variant_u.py) | [`docs/variants/variant_u.md`](docs/variants/variant_u.md) |
| **V** | Variant V · 0.25x Quarter-Kelly Live Engine (No Hard rho Cap) | `core` | +$2,365 (+9.46% / 30d) · 75.0% WR · -2.99% DD · 4.66 Sharpe · PF 17.86 · 8 trades | [`variants/variant_v.py`](variants/variant_v.py) | [`docs/variants/variant_v.md`](docs/variants/variant_v.md) |
| **X** | Variant X · Hybrid Live Playbook (Synthesis of Stages 0-5) | `core` | Target Bankroll: $25k-$30k (Untested live blueprint; backtestable via simulator) | [`variants/variant_x.py`](variants/variant_x.py) | [`docs/variants/variant_x.md`](docs/variants/variant_x.md) |
| **R-MKT** | Variant R-MKT · Market Factors Only (Zero Tweets) | `ablation` | +$3,781 (+15.12% ROC) · 62.5% WR · PF 2.02 · -9.34% DD · 8 trades | [`variants/variant_r_mkt.py`](variants/variant_r_mkt.py) | [`docs/variants/variant_r_mkt.md`](docs/variants/variant_r_mkt.md) |
| **Q-MKT** | Variant Q-MKT · Market Factors Only (Zero Tweets) | `ablation` | -$1,312 (-4.37% ROC) · 53.3% WR · PF 0.83 · -17.52% DD · 15 trades | [`variants/variant_q_mkt.py`](variants/variant_q_mkt.py) | [`docs/variants/variant_q_mkt.md`](docs/variants/variant_q_mkt.md) |
| **K-MKT** | Variant K-MKT · Market Factors Only (Zero Tweets) | `ablation` | +$3,542 (+2.62% ROC) · 59.3% WR · PF 1.42 · -3.20% DD · 27 trades | [`variants/variant_k_mkt.py`](variants/variant_k_mkt.py) | [`docs/variants/variant_k_mkt.md`](docs/variants/variant_k_mkt.md) |
| **R-TW** | Variant R-TW · Tweets Only (Zero Market Filters) | `ablation` | -$2,162 (-8.65% ROC) · 40.0% WR · PF 0.40 · -14.36% DD · 5 trades | [`variants/variant_r_tw.py`](variants/variant_r_tw.py) | [`docs/variants/variant_r_tw.md`](docs/variants/variant_r_tw.md) |
| **Q-TW** | Variant Q-TW · Tweets Only (Zero Market Filters) | `ablation` | -$853 (-2.84% ROC) · 26.7% WR · PF 0.69 · -9.05% DD · 15 trades | [`variants/variant_q_tw.py`](variants/variant_q_tw.py) | [`docs/variants/variant_q_tw.md`](docs/variants/variant_q_tw.md) |
| **K-TW** | Variant K-TW · Tweets Only (Zero Market Filters) | `ablation` | +$8,888 (+4.34% ROC) · 61.0% WR · PF 2.01 · -5.02% DD · 41 trades | [`variants/variant_k_tw.py`](variants/variant_k_tw.py) | [`docs/variants/variant_k_tw.md`](docs/variants/variant_k_tw.md) |
| **S-3.0** | Shlomo · Original Floor >= 3.0 (5-Day Hold) | `shlomo` | +$8,032 (+10.71% ROC) · 58.5% WR · PF 3.01 · 41 trades | [`variants/shlomo_30.py`](variants/shlomo_30.py) | [`docs/variants/shlomo_30.md`](docs/variants/shlomo_30.md) |
| **S-Sniper** | Shlomo-Sniper · >= 5.5 + Early/No-Conflict ($25k 2x 5d) | `shlomo` | +$5,943 (+23.77% ROC) · 77.8% WR · PF 8.29 · 9 trades | [`variants/shlomo_sniper.py`](variants/shlomo_sniper.py) | [`docs/variants/shlomo_sniper.md`](docs/variants/shlomo_sniper.md) |
| **S-5.25** | Shlomo-5.25 · Sweet-Spot Floor >= 5.25 (1x 5d) | `shlomo` | +$7,641 (+16.98% ROC) · 77.8% WR · PF 10.37 · 18 trades | [`variants/shlomo_525.py`](variants/shlomo_525.py) | [`docs/variants/shlomo_525.md`](docs/variants/shlomo_525.md) |
| **S-5.50** | Shlomo-5.50 · Precision Floor >= 5.50 (1x 5d) | `shlomo` | +$3,648 (+12.16% ROC) · 83.3% WR · PF 10.09 · 12 trades | [`variants/shlomo_550.py`](variants/shlomo_550.py) | [`docs/variants/shlomo_550.md`](docs/variants/shlomo_550.md) |
| **S-Tiered** | Shlomo-Tiered · Score-Sized Floor >= 5.0 | `shlomo` | +$14,272 (+10.57% ROC) · 75.0% WR · PF 5.74 · 24 trades | [`variants/shlomo_tiered.py`](variants/shlomo_tiered.py) | [`docs/variants/shlomo_tiered.md`](docs/variants/shlomo_tiered.md) |

## Disclaimer

All backtests and paper-trading simulations are for educational and research purposes only and do **not** constitute investment advice. Past hypothetical performance does not guarantee future results.
