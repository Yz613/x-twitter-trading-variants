import json
import math
import time
import urllib.request
from datetime import datetime, timezone

TICKERS = [
    "NVDA", "META", "ORCL", "NOW", "RDDT", "AMD", "INTC", "SMCI", "PLTR",
    "TSLA", "SHOP", "NFLX", "AMZN", "GOOGL", "MSFT", "COIN", "MSTR", "IBIT",
    "HOOD", "APP", "SNOW", "DDOG", "NET", "CRWD", "PANW", "MDB", "ZS",
    "ARM", "AVGO", "MU", "MRVL", "UBER", "DASH", "ABNB", "PYPL", "SPOT",
    "RBLX", "DKNG", "SOFI", "AFRM", "CVNA", "CELH", "ANET", "DELL", "ESTC",
    "GTLB", "SNAP", "PINS", "ROKU", "TTD", "OKTA", "TWLO", "DOCU", "ZM",
    "U", "PATH", "CFLT", "BILL", "HUBS", "TEAM"
]

START_TS = int(datetime(2024, 1, 1, tzinfo=timezone.utc).timestamp())
END_TS = int(datetime(2026, 9, 30, 23, 59, tzinfo=timezone.utc).timestamp())


def fetch_daily(symbol):
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={START_TS}&period2={END_TS}&interval=1d&includeAdjustedClose=true"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    res = data["chart"]["result"][0]
    ts = res.get("timestamp", [])
    q = res["indicators"]["quote"][0]
    bars = []
    for i, t in enumerate(ts):
        o, h, l, c, v = q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i]
        if None in (o, h, l, c) or c <= 0 or o <= 0:
            continue
        dt = datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d")
        bars.append({"date": dt, "open": o, "high": h, "low": l, "close": c, "volume": v or 0})
    return bars


def compute_spy_regime(spy_bars):
    regime = {}
    closes = [b["close"] for b in spy_bars]
    for i, b in enumerate(spy_bars):
        if i >= 19:
            sma20 = sum(closes[i - 19 : i + 1]) / 20.0
            regime[b["date"]] = "bull" if b["close"] >= sma20 else "bear"
    return regime


def compute_atr14_pct(bars, idx):
    if idx < 14:
        return None
    trs = []
    for j in range(idx - 13, idx + 1):
        h, l, pc = bars[j]["high"], bars[j]["low"], bars[j - 1]["close"]
        tr = max(h - l, abs(h - pc), abs(l - pc))
        trs.append(tr)
    atr = sum(trs) / 14.0
    return (atr / bars[idx - 1]["close"]) * 100.0


def simulate_trade(bars, entry_idx, symbol, spy_regime, use_cat_stop=False):
    # Enter short at shock day close (mirroring after-hours / intraday post-shock fill)
    entry_bar = bars[entry_idx]
    entry = entry_bar["close"]
    notional = 10000.0
    cash = 5000.0
    max_hold = 20

    exit_idx = min(entry_idx + max_hold, len(bars) - 1)
    exit_price = bars[exit_idx]["close"]
    exit_reason = "20d max hold"

    for k in range(entry_idx + 1, min(entry_idx + max_hold, len(bars) - 1) + 1):
        c = bars[k]["close"]
        ret_short = (entry - c) / entry
        if ret_short >= 0.20:
            exit_idx = k
            exit_price = c
            exit_reason = "+20% target"
            break
        if use_cat_stop and ret_short <= -0.15:
            exit_idx = k
            exit_price = c
            exit_reason = "-15% cat stop"
            break

    cal_days = max(
        1,
        (
            datetime.strptime(bars[exit_idx]["date"], "%Y-%m-%d")
            - datetime.strptime(entry_bar["date"], "%Y-%m-%d")
        ).days,
    )
    gross_ret = (entry - exit_price) / entry
    gross_pnl = notional * gross_ret
    slippage = notional * 0.0020  # 0.10% each leg
    borrow = notional * 0.03 * (cal_days / 365.0)
    margin_int = (notional - cash) * 0.065 * (cal_days / 365.0)
    friction = slippage + borrow + margin_int
    net_pnl = gross_pnl - friction

    return {
        "ticker": symbol,
        "entry_date": entry_bar["date"],
        "exit_date": bars[exit_idx]["date"],
        "hold_days": exit_idx - entry_idx,
        "cal_days": cal_days,
        "shock_pct": round(((entry_bar["close"] - bars[entry_idx - 1]["close"]) / bars[entry_idx - 1]["close"]) * 100.0, 2),
        "atr_pct": round(compute_atr14_pct(bars, entry_idx - 1) or 0.0, 2),
        "regime": spy_regime.get(entry_bar["date"], "unknown"),
        "entry": round(entry, 2),
        "exit": round(exit_price, 2),
        "exit_reason": exit_reason,
        "gross_pnl": round(gross_pnl, 2),
        "friction": round(friction, 2),
        "net_pnl": round(net_pnl, 2),
        "net_roc_cash_pct": round((net_pnl / cash) * 100.0, 2),
    }


def summarize(trades, label):
    if not trades:
        return {"label": label, "n": 0}
    wins = [t for t in trades if t["net_pnl"] > 0]
    losses = [t for t in trades if t["net_pnl"] <= 0]
    gross_win = sum(t["net_pnl"] for t in wins)
    gross_loss = abs(sum(t["net_pnl"] for t in losses))
    pf = round(gross_win / gross_loss, 2) if gross_loss > 0 else None
    total_net = sum(t["net_pnl"] for t in trades)
    avg_net = total_net / len(trades)
    rets = sorted(t["net_roc_cash_pct"] for t in trades)
    med_ret = rets[len(rets) // 2]
    worst = min(trades, key=lambda t: t["net_pnl"])
    best = max(trades, key=lambda t: t["net_pnl"])
    targets = sum(1 for t in trades if t["exit_reason"] == "+20% target")
    cat_stops = sum(1 for t in trades if t["exit_reason"] == "-15% cat stop")
    return {
        "label": label,
        "n": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": round(len(wins) / len(trades) * 100.0, 1),
        "total_net_pnl": round(total_net, 2),
        "avg_net_pnl": round(avg_net, 2),
        "avg_roc_cash_pct": round((avg_net / 5000.0) * 100.0, 2),
        "median_roc_cash_pct": med_ret,
        "profit_factor": pf,
        "targets_hit": targets,
        "cat_stops_hit": cat_stops,
        "best": f"{best['ticker']} {best['entry_date']} (+${best['net_pnl']:.0f})",
        "worst": f"{worst['ticker']} {worst['entry_date']} (${worst['net_pnl']:.0f})",
    }


def run_capped_portfolio(all_trades, max_cash=25000.0):
    # Chronological $25k cash-capped simulation (max 5 concurrent $5k-cash / $10k-notional positions, 1 per ticker)
    ordered = sorted(all_trades, key=lambda t: (t["entry_date"], t["shock_pct"]))
    open_pos = []
    taken = []
    skipped_cap = 0
    skipped_dup = 0
    equity = max_cash
    peak_eq = max_cash
    max_dd_pct = 0.0
    equity_curve = []

    for tr in ordered:
        # Close positions whose exit_date <= tr.entry_date
        still_open = []
        for op in open_pos:
            if op["exit_date"] <= tr["entry_date"]:
                equity += op["net_pnl"]
                peak_eq = max(peak_eq, equity)
                dd = (equity - peak_eq) / peak_eq * 100.0
                max_dd_pct = min(max_dd_pct, dd)
                equity_curve.append((op["exit_date"], round(equity, 2)))
            else:
                still_open.append(op)
        open_pos = still_open

        if any(op["ticker"] == tr["ticker"] for op in open_pos):
            skipped_dup += 1
            continue
        if len(open_pos) * 5000.0 + 5000.0 > max_cash:
            skipped_cap += 1
            continue
        open_pos.append(tr)
        taken.append(tr)

    for op in sorted(open_pos, key=lambda x: x["exit_date"]):
        equity += op["net_pnl"]
        peak_eq = max(peak_eq, equity)
        dd = (equity - peak_eq) / peak_eq * 100.0
        max_dd_pct = min(max_dd_pct, dd)
        equity_curve.append((op["exit_date"], round(equity, 2)))

    s = summarize(taken, f"$25k Capped Portfolio ({len(taken)} trades)")
    s["ending_equity"] = round(equity, 2)
    s["total_return_on_25k_pct"] = round((equity - max_cash) / max_cash * 100.0, 2)
    s["max_dd_pct"] = round(max_dd_pct, 2)
    s["skipped_cap"] = skipped_cap
    s["skipped_dup"] = skipped_dup
    return s, taken


def main():
    spy_bars = fetch_daily("SPY")
    spy_regime = compute_spy_regime(spy_bars)

    candidates_no_stop = []
    candidates_cat_stop = []
    loaded = 0

    for sym in TICKERS:
        try:
            bars = fetch_daily(sym)
            loaded += 1
        except Exception as e:
            continue

        last_entry_idx = -999
        for i in range(20, len(bars) - 21):
            if i - last_entry_idx < 25:
                continue
            prev_c = bars[i - 1]["close"]
            c = bars[i]["close"]
            o = bars[i]["open"]
            drop_pct = (c - prev_c) / prev_c * 100.0
            # Hard negative shock signature: down >= 8% on the day (earnings miss / dilution / probe / crash),
            # not fighting a green tape (close < open and close < prev_close)
            if not (-28.0 <= drop_pct <= -8.0):
                continue
            if c >= o:
                continue
            atr_pct = compute_atr14_pct(bars, i - 1)
            if atr_pct is None:
                continue
            # Variant R velocity floor: ATR >= 3.2% (crypto ETF IBIT exempt)
            if sym != "IBIT" and atr_pct < 3.2:
                continue
            # Volume surge >= 2.0x 20-day avg (confirms genuine news/earnings shock)
            avg_vol = sum(b["volume"] for b in bars[i - 20 : i]) / 20.0
            if avg_vol > 0 and bars[i]["volume"] < 2.0 * avg_vol:
                continue

            tr0 = simulate_trade(bars, i, sym, spy_regime, use_cat_stop=False)
            tr1 = simulate_trade(bars, i, sym, spy_regime, use_cat_stop=True)
            candidates_no_stop.append(tr0)
            candidates_cat_stop.append(tr1)
            last_entry_idx = i

    # Take the most recent 100 out-of-sample trades (chronologically)
    candidates_no_stop.sort(key=lambda t: (t["entry_date"], t["ticker"]))
    candidates_cat_stop.sort(key=lambda t: (t["entry_date"], t["ticker"]))
    sample100_no_stop = candidates_no_stop[-100:]
    sample100_cat_stop = candidates_cat_stop[-100:]

    out = {
        "tickers_loaded": loaded,
        "total_shocks_found": len(candidates_no_stop),
        "sample_window": f"{sample100_no_stop[0]['entry_date']} to {sample100_no_stop[-1]['entry_date']}",
        "all_100_no_stop": summarize(sample100_no_stop, "All 100 Trades (Variant R Exact, No Cat Stop)"),
        "all_100_bear_no_stop": summarize([t for t in sample100_no_stop if t["regime"] == "bear"], "Bear Tape Only (SPY < 20-SMA)"),
        "all_100_bull_no_stop": summarize([t for t in sample100_no_stop if t["regime"] == "bull"], "Bull Tape Only (SPY >= 20-SMA)"),
        "all_100_cat_stop": summarize(sample100_cat_stop, "All 100 Trades (Variant R + 15% Cat Stop)"),
        "all_100_bear_cat_stop": summarize([t for t in sample100_cat_stop if t["regime"] == "bear"], "Bear Tape + 15% Cat Stop"),
        "all_100_bull_cat_stop": summarize([t for t in sample100_cat_stop if t["regime"] == "bull"], "Bull Tape + 15% Cat Stop"),
    }

    cap_no_stop, _ = run_capped_portfolio(sample100_no_stop, 25000.0)
    cap_cat_stop, _ = run_capped_portfolio(sample100_cat_stop, 25000.0)
    cap_bear_only, _ = run_capped_portfolio([t for t in sample100_no_stop if t["regime"] == "bear"], 25000.0)
    out["capped_25k_no_stop"] = cap_no_stop
    out["capped_25k_cat_stop"] = cap_cat_stop
    out["capped_25k_bear_only"] = cap_bear_only

    print(json.dumps(out, indent=2))
    with open("/tmp/variant_r_100_results.json", "w") as f:
        json.dump({"summary": out, "trades_no_stop": sample100_no_stop, "trades_cat_stop": sample100_cat_stop}, f, indent=2)


if __name__ == "__main__":
    main()
