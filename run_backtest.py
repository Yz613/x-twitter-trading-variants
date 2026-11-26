"""CLI runner to execute any single variant, group, or all 32 trading variants."""
import argparse
import json

from engine.simulator import run_variant_backtest
from variants import ALL_VARIANTS


def main():
    parser = argparse.ArgumentParser(description="Run backtests for X/Twitter & Shlomo trading variants.")
    parser.add_argument("--variant", default="all", help="Variant ID (e.g. variant_r, shlomo_sniper, all, core, shlomo, ablation)")
    parser.add_argument("--capital", type=float, default=None, help="Optional custom bankroll cap in USD (e.g. 10000)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    key = args.variant.lower().strip()
    if key == "all":
        selected = list(ALL_VARIANTS.values())
    elif key in ("core", "shlomo", "ablation"):
        selected = [v for v in ALL_VARIANTS.values() if v["group"] == key]
    elif key in ALL_VARIANTS:
        selected = [ALL_VARIANTS[key]]
    else:
        raise SystemExit(f"Unknown variant '{args.variant}'. Available: {', '.join(ALL_VARIANTS.keys())}")

    shared_cache = {}
    results = []
    for cfg in selected:
        res = run_variant_backtest(cfg, capital_override=args.capital, ohlc_cache=shared_cache)
        results.append(res)

    if args.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "positions"} for r in results], indent=2))
        return

    print(f"{'Variant':<26} {'Trades':>6} {'WR %':>7} {'Capital':>10} {'Net P&L':>11} {'ROC %':>9} {'PF':>7}")
    print("-" * 82)
    for r in sorted(results, key=lambda x: x["roc_pct"], reverse=True):
        print(
            f"{r['id']:<26} {r['trades']:>6} {r['win_rate_pct']:>6.1f}% "
            f"${r['capital_base']:>9,.0f} ${r['net_pnl']:>+10,.0f} {r['roc_pct']:>+8.2f}% {str(r['profit_factor']):>7}"
        )


if __name__ == "__main__":
    main()
