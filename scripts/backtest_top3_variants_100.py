import json
import urllib.request
from datetime import datetime, timezone

TICKERS = [
    "NVDA", "META", "ORCL", "NOW", "RDDT", "AMD", "INTC", "SMCI", "PLTR",
    "TSLA", "SHOP", "NFLX", "AMZN", "GOOGL", "MSFT", "COIN", "MSTR", "IBIT",
    "HOOD", "APP", "SNOW", "DDOG", "NET", "CRWD", "PANW", "MDB", "ZS",
    "ARM", "AVGO", "MU", "MRVL", "UBER", "DASH", "ABNB", "PYPL", "SPOT",
    "RBLX", "DKNG", "SOFI", "AFRM", "CVNA", "CELH", "ANET", "DELL", "ESTC",
    "GTLB", "SNAP", "PINS", "ROKU", "TTD", "OKTA", "TWLO", "DOCU", "ZM",
    "U", "PATH", "CFLT", "BILL", "HUBS", "TEAM",
    # Add lower-ATR blue chips for Variant K (no ATR floor)
    "BA", "JPM", "BAC", "DIS", "WMT", "TGT", "NKE", "SBUX", "CMG", "IBM"
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
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return (sum(trs) / 14.0) / bars[idx - 1]["close"] * 100.0


def eval_path(bars, entry_idx, side="short", target=0.20, max_hold=20, day5_cut=False, cat_stop=None):
    entry = bars[entry_idx]["close"]
    end_idx = min(entry_idx + max_hold, len(bars) - 1)
    exit_idx = end_idx
    exit_price = bars[end_idx]["close"]
    reason = f"{max_hold}d max"

    for k in range(entry_idx + 1, end_idx + 1):
        c = bars[k]["close"]
        ret = (entry - c) / entry if side == "short" else (c - entry) / entry
        day_num = k - entry_idx
        if target is not None and ret >= target:
            exit_idx, exit_price, reason = k, c, f"+{int(target*100)}% target"
            break
        if cat_stop is not None and ret <= -cat_stop:
            exit_idx, exit_price, reason = k, c, f"-{int(cat_stop*100)}% cat stop"
            break
        if day5_cut and day_num == 5 and ret < 0.02:
            exit_idx, exit_price, reason = k, c, "Day-5 <+2% cut"
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
        "entry": round(entry, 2),
        "exit": round(exit_price, 2),
        "cal_days": cal_days,
        "gross_ret": gross_ret,
        "reason": reason,
    }


def simulate_portfolio(events, mode):
    """
    mode:
      'Q': $30k 1x cash ($5k/trade, max 6 open), ATR>=3.2%, +20% target, Day-5 <+2% cut, 20d max
      'K': Uncapped 1x cash ($5k bear / $2.5k bull per SPY 20-SMA regime gate), ALL ATRs, no target cap, no stops, 20d max
      'V': $25k compounding, 0.25x Quarter-Kelly (~16% of live equity per trade, 1x cash, max 80% deployed), +20% target, 15d max, 15% cat stop
      'R': $25k 2x margin ($5k cash / $10k notional, max 5 open), ATR>=3.2%, +20% target, 20d max
      'LONG_FLIP': Sanity check — $25k 1x cash buying the same 100 shocks LONG (+20% target, 20d max)
    """
    if mode == "Q":
        start_cash = 30000.0
    elif mode in ("V", "R", "LONG_FLIP"):
        start_cash = 25000.0
    else:  # K
        start_cash = 100000.0  # track peak concurrent cash separately

    equity = start_cash
    peak_eq = start_cash
    max_dd_pct = 0.0
    peak_cash_used = 0.0
    open_pos = []
    taken = []

    for ev in events:
        # Close positions exited on or before entry_date
        still_open = []
        for op in open_pos:
            if op["exit_date"] <= ev["entry_date"]:
                equity += op["net_pnl"]
                peak_eq = max(peak_eq, equity)
                dd = (equity - peak_eq) / peak_eq * 100.0 if peak_eq > 0 else -100.0
                max_dd_pct = min(max_dd_pct, dd)
            else:
                still_open.append(op)
        open_pos = still_open

        if any(op["ticker"] == ev["ticker"] for op in open_pos):
            continue

        cur_cash_used = sum(op["cash"] for op in open_pos)

        if mode == "Q":
            if cur_cash_used + 5000.0 > 30000.0:
                continue
            cash, notional = 5000.0, 5000.0
            p = ev["path_Q"]
            is_short, margin_borrowed = True, 0.0
        elif mode == "K":
            # SPY 20-SMA regime gate: full $5k in bear tape, half ($2.5k) in bull tape
            size = 5000.0 if ev["regime"] == "bear" else 2500.0
            cash, notional = size, size
            p = ev["path_K"]
            is_short, margin_borrowed = True, 0.0
        elif mode == "V":
            if equity <= 2000.0:
                continue
            # 0.25x Quarter-Kelly (~16% of current equity per trade, capped so total deployed <= 80% equity)
            size = round(equity * 0.16, 2)
            if cur_cash_used + size > equity * 0.80:
                continue
            cash, notional = size, size
            p = ev["path_V"]
            is_short, margin_borrowed = True, 0.0
        elif mode == "R":
            if cur_cash_used + 5000.0 > 25000.0:
                continue
            cash, notional = 5000.0, 10000.0
            p = ev["path_R"]
            is_short, margin_borrowed = True, 5000.0
        elif mode == "LONG_FLIP":
            if cur_cash_used + 5000.0 > 25000.0:
                continue
            cash, notional = 5000.0, 5000.0
            p = ev["path_LONG"]
            is_short, margin_borrowed = False, 0.0

        gross_pnl = notional * p["gross_ret"]
        slippage = notional * 0.0020
        borrow = (notional * 0.03 * (p["cal_days"] / 365.0)) if is_short else 0.0
        margin_int = margin_borrowed * 0.065 * (p["cal_days"] / 365.0)
        net_pnl = gross_pnl - slippage - borrow - margin_int

        rec = {
            "ticker": ev["ticker"],
            "entry_date": p["entry_date"],
            "exit_date": p["exit_date"],
            "regime": ev["regime"],
            "cash": cash,
            "notional": notional,
            "net_pnl": round(net_pnl, 2),
            "reason": p["reason"],
        }
        open_pos.append(rec)
        taken.append(rec)
        peak_cash_used = max(peak_cash_used, sum(op["cash"] for op in open_pos))

    for op in sorted(open_pos, key=lambda x: x["exit_date"]):
        equity += op["net_pnl"]
        peak_eq = max(peak_eq, equity)
        dd = (equity - peak_eq) / peak_eq * 100.0 if peak_eq > 0 else -100.0
        max_dd_pct = min(max_dd_pct, dd)

    wins = [t for t in taken if t["net_pnl"] > 0]
    losses = [t for t in taken if t["net_pnl"] <= 0]
    gw = sum(t["net_pnl"] for t in wins)
    gl = abs(sum(t["net_pnl"] for t in losses))
    pf = round(gw / gl, 2) if gl > 0 else None
    total_net = round(sum(t["net_pnl"] for t in taken), 2)
    denom = peak_cash_used if mode == "K" else start_cash
    roc_pct = round(total_net / denom * 100.0, 2) if denom > 0 else 0.0
    worst = min(taken, key=lambda t: t["net_pnl"]) if taken else None
    best = max(taken, key=lambda t: t["net_pnl"]) if taken else None

    return {
        "variant": mode,
        "trades_taken": len(taken),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": round(len(wins) / len(taken) * 100.0, 1) if taken else 0.0,
        "capital_base": round(denom, 2),
        "net_pnl": total_net,
        "return_pct": roc_pct,
        "profit_factor": pf,
        "max_dd_pct": round(max_dd_pct, 2),
        "best": f"{best['ticker']} {best['entry_date']} (+${best['net_pnl']:.0f})" if best else None,
        "worst": f"{worst['ticker']} {worst['entry_date']} (${worst['net_pnl']:.0f})" if worst else None,
    }


def main():
    spy_bars = fetch_daily("SPY")
    spy_regime = compute_spy_regime(spy_bars)

    high_atr_events = []
    all_atr_events = []

    for sym in TICKERS:
        try:
            bars = fetch_daily(sym)
        except Exception:
            continue
        last_idx = -999
        for i in range(20, len(bars) - 21):
            if i - last_idx < 25:
                continue
            prev_c, o, c = bars[i - 1]["close"], bars[i]["open"], bars[i]["close"]
            drop_pct = (c - prev_c) / prev_c * 100.0
            if not (-28.0 <= drop_pct <= -8.0) or c >= o:
                continue
            atr_pct = compute_atr14_pct(bars, i - 1)
            if atr_pct is None:
                continue
            avg_vol = sum(b["volume"] for b in bars[i - 20 : i]) / 20.0
            if avg_vol > 0 and bars[i]["volume"] < 2.0 * avg_vol:
                continue

            ev = {
                "ticker": sym,
                "entry_date": bars[i]["date"],
                "drop_pct": round(drop_pct, 2),
                "atr_pct": round(atr_pct, 2),
                "regime": spy_regime.get(bars[i]["date"], "unknown"),
                "path_Q": eval_path(bars, i, "short", target=0.20, max_hold=20, day5_cut=True, cat_stop=None),
                "path_K": eval_path(bars, i, "short", target=None, max_hold=20, day5_cut=False, cat_stop=None),
                "path_V": eval_path(bars, i, "short", target=0.20, max_hold=15, day5_cut=False, cat_stop=0.15),
                "path_R": eval_path(bars, i, "short", target=0.20, max_hold=20, day5_cut=False, cat_stop=None),
                "path_LONG": eval_path(bars, i, "long", target=0.20, max_hold=20, day5_cut=False, cat_stop=None),
            }
            all_atr_events.append(ev)
            if sym == "IBIT" or atr_pct >= 3.2:
                high_atr_events.append(ev)
            last_idx = i

    high_atr_events.sort(key=lambda e: (e["entry_date"], e["ticker"]))
    all_atr_events.sort(key=lambda e: (e["entry_date"], e["ticker"]))

    sample_100_high = high_atr_events[-100:]
    sample_100_all = all_atr_events[-100:]

    results = {
        "high_atr_window": f"{sample_100_high[0]['entry_date']} to {sample_100_high[-1]['entry_date']}",
        "all_atr_window": f"{sample_100_all[0]['entry_date']} to {sample_100_all[-1]['entry_date']}",
        "Variant_R_25k_2x": simulate_portfolio(sample_100_high, "R"),
        "Variant_Q_30k_1x_Day5": simulate_portfolio(sample_100_high, "Q"),
        "Variant_K_AllATR_Regime": simulate_portfolio(sample_100_all, "K"),
        "Variant_V_25k_QKelly": simulate_portfolio(sample_100_high, "V"),
        "SanityCheck_LONG_DipBuy_25k_1x": simulate_portfolio(sample_100_high, "LONG_FLIP"),
    }
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
