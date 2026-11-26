"""
Shlomo's 8-Metric Rubric — Multi-Variant Optimization Sweep (Oct 9 - Nov 25, 2026)
===================================================================================
Tests floors (3.0 to 5.75), Shlomo's weighted rubric (clarity/invalidation/entry/conflict),
score-tiered sizing, fixed holds (5d, 10d, Nov 25), and a $25k 2x Sniper cap on real
Yahoo Finance daily OHLC data (net of 0.10%/leg slippage, 3% borrow, 6.5% margin).
"""
import json
from datetime import datetime
import backtest_shlomo_variant as base


def eval_path(bars, entry_idx, side, max_sessions=None, target=None):
    entry = bars[entry_idx]["open"]
    end_idx = len(bars) - 1
    while end_idx > entry_idx and bars[end_idx]["date"] > base.WIN_END:
        end_idx -= 1
    limit_idx = min(entry_idx + max_sessions, end_idx) if max_sessions else end_idx
    exit_idx = limit_idx
    exit_price = bars[limit_idx]["close"]
    for k in range(entry_idx + 1, limit_idx + 1):
        c = bars[k]["close"]
        ret = (entry - c) / entry if side == "short" else (c - entry) / entry
        if target is not None and ret >= target:
            exit_idx, exit_price = k, c
            break
    cal_days = max(
        1,
        (
            datetime.strptime(bars[exit_idx]["date"], "%Y-%m-%d")
            - datetime.strptime(bars[entry_idx]["date"], "%Y-%m-%d")
        ).days,
    )
    gross_ret = (entry - exit_price) / entry if side == "short" else (exit_price - entry) / entry
    return {
        "entry_date": bars[entry_idx]["date"],
        "exit_date": bars[exit_idx]["date"],
        "cal_days": cal_days,
        "gross_ret": gross_ret,
    }


def run_sim(items, max_sessions=5, target=None, cash_cap=None, leverage=1.0, score_sized=False):
    open_pos = []
    taken = []
    peak_cash = 0.0
    for it in items:
        p = eval_path(it["bars"], it["idx"], it["side"], max_sessions=max_sessions, target=target)
        still = [op for op in open_pos if op["exit_date"] > p["entry_date"]]
        open_pos = still
        if cash_cap is not None and any(op["ticker"] == it["ticker"] for op in open_pos):
            continue
        if score_sized:
            sc = it["score"]
            cash = 10000.0 if sc >= 5.75 else (5000.0 if sc >= 5.25 else 2500.0)
        else:
            cash = 5000.0
        cur_cash = sum(op["cash"] for op in open_pos)
        if cash_cap is not None and cur_cash + cash > cash_cap:
            continue
        notional = cash * leverage
        margin_borrowed = notional - cash
        slip = notional * 0.0020
        borrow = (notional * 0.03 * (p["cal_days"] / 365.0)) if it["side"] == "short" else 0.0
        mint = margin_borrowed * 0.065 * (p["cal_days"] / 365.0)
        net_pnl = notional * p["gross_ret"] - slip - borrow - mint
        rec = {
            "ticker": it["ticker"],
            "side": it["side"],
            "score": it["score"],
            "entry_date": p["entry_date"],
            "exit_date": p["exit_date"],
            "cash": cash,
            "notional": notional,
            "net_pnl": round(net_pnl, 2),
        }
        open_pos.append(rec)
        taken.append(rec)
        peak_cash = max(peak_cash, sum(op["cash"] for op in open_pos))

    wins = [t for t in taken if t["net_pnl"] > 0]
    losses = [t for t in taken if t["net_pnl"] <= 0]
    gw = sum(t["net_pnl"] for t in wins)
    gl = abs(sum(t["net_pnl"] for t in losses))
    pf = round(gw / gl, 2) if gl > 0 else "INF"
    total_net = round(sum(t["net_pnl"] for t in taken), 2)
    denom = cash_cap if cash_cap is not None else peak_cash
    roc = round(total_net / denom * 100.0, 2) if denom > 0 else 0.0
    best = max(taken, key=lambda t: t["net_pnl"]) if taken else None
    worst = min(taken, key=lambda t: t["net_pnl"]) if taken else None
    return {
        "trades": len(taken),
        "wins": len(wins),
        "losses": len(losses),
        "wr_pct": round(len(wins) / len(taken) * 100.0, 1) if taken else 0.0,
        "capital_base": denom,
        "net_pnl": total_net,
        "roc_pct": roc,
        "pf": pf,
        "best": f"{best['ticker']} (+${best['net_pnl']:.0f})" if best else None,
        "worst": f"{worst['ticker']} (${worst['net_pnl']:.0f})" if worst else None,
    }


def main():
    syms = sorted(set(t[1] for t in base.TWEETS))
    cache = {s: base.fetch_daily(s) for s in syms}

    rows = []
    for i, (post_dt, sym, side, note, c1, c2, c3, c4, c5, c6) in enumerate(base.TWEETS):
        bars = cache[sym]
        idx = next((k for k, b in enumerate(bars) if b["date"] >= post_dt), None)
        if idx is None or idx >= len(bars) - 1:
            continue
        c7 = base.score_entry_quality(bars, idx, side)
        c8 = base.score_conflict_check(base.TWEETS, i)
        eq = round((c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8) / 8.0, 3)
        # Shlomo's weighted rubric: clarity(2.0), entry_quality(2.0), conflict(1.5),
        # trigger(1.5), evidence(1.5), invalidation(1.5), specificity(1.0), horizon(1.0) -> /12
        wt = round((2.0*c1 + 1.0*c2 + 1.5*c3 + 1.5*c4 + 1.0*c5 + 1.5*c6 + 2.0*c7 + 1.5*c8) / 12.0, 3)
        rows.append({
            "date": post_dt, "ticker": sym, "side": side, "note": note,
            "bars": bars, "idx": idx,
            "c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5, "c6": c6, "c7": c7, "c8": c8,
            "eq": eq, "wt": wt,
        })

    results = {}

    # 1. Equal-weight floor sweep (5-session hold & Nov 25 hold)
    for fl in [3.0, 4.5, 5.0, 5.25, 5.5, 5.75]:
        sub = [{**r, "score": r["eq"]} for r in rows if r["eq"] >= fl]
        results[f"Eq>={fl:.2f} | 5d Hold"] = run_sim(sub, max_sessions=5)
        results[f"Eq>={fl:.2f} | 10d Hold"] = run_sim(sub, max_sessions=10)
        results[f"Eq>={fl:.2f} | Nov25 Hold"] = run_sim(sub, max_sessions=None)

    # 2. Shlomo Weighted Rubric + Conflict/Entry Gate (entry_quality>=4.5, conflict>=5.0)
    for fl in [4.75, 5.0, 5.25, 5.5]:
        sub = [{**r, "score": r["wt"]} for r in rows if r["wt"] >= fl and r["c7"] >= 4.5 and r["c8"] >= 5.0]
        results[f"Weighted>={fl:.2f} + NoConflict/Early | 5d Hold"] = run_sim(sub, max_sessions=5)
        results[f"Weighted>={fl:.2f} + NoConflict/Early | Nov25 Hold"] = run_sim(sub, max_sessions=None)

    # 3. Shlomo Score-Tiered Sizing (Eq >= 5.0, bet $2.5k / $5k / $10k by score)
    sub5 = [{**r, "score": r["eq"]} for r in rows if r["eq"] >= 5.0]
    results["Shlomo Tiered-Size (Eq>=5.0) | 5d Hold"] = run_sim(sub5, max_sessions=5, score_sized=True)
    results["Shlomo Tiered-Size (Eq>=5.0) | Nov25 Hold"] = run_sim(sub5, max_sessions=None, score_sized=True)

    # 4. Shlomo $25k 2x Sniper (Eq >= 5.5 + Entry>=4.5 + Conflict>=5.0, $25k cap, 2x margin, +20% target)
    sub_sniper = [{**r, "score": r["eq"]} for r in rows if r["eq"] >= 5.5 and r["c7"] >= 4.5 and r["c8"] >= 5.0]
    results["Shlomo Sniper-2x (Eq>=5.5, $25k, +20% tgt)"] = run_sim(
        sub_sniper, max_sessions=None, target=0.20, cash_cap=25000.0, leverage=2.0
    )
    results["Shlomo Sniper-1x (Eq>=5.5, $25k, 5d hold)"] = run_sim(
        sub_sniper, max_sessions=5, target=0.20, cash_cap=25000.0, leverage=1.0
    )
    results["Shlomo Sniper-2x-5d (Eq>=5.5, $25k, 5d hold)"] = run_sim(
        sub_sniper, max_sessions=5, target=0.20, cash_cap=25000.0, leverage=2.0
    )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
