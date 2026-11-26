"""
Top-3 Champions (R, Q, K) Two-Way Ablation Backtest (Oct 9 - Nov 25, 2026)
=========================================================================
1. Market-Factors-Only (NO TWEETS): Variants R-MKT, Q-MKT, K-MKT
   - Scans the 70-ticker universe over Oct 9 - Nov 25, 2026 using ONLY market-factor
     signals (daily shock drop -8% to -28%, red close < open, volume >= 2.0x 20d avg)
     + each variant's exact ATR / SPY 20-SMA / cash cap / exit rules.
2. Tweets-Only (NO MARKET FACTORS): Variants R-TW, Q-TW, K-TW
   - Uses the chronological unfiltered @KobeissiLetter tweet stream over Oct 9 - Nov 25, 2026
     (including longs, gaps, proxy ETFs, slow ATRs, bear-tape longs) with ALL market-factor
     filters removed, run through each variant's exact sizing/budget/exit engine.
All P&L figures are strictly net of 0.10%/leg slippage, 3.0% short borrow, and 6.5% margin interest.
"""
import json
import re
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
    "BA", "JPM", "BAC", "DIS", "WMT", "TGT", "NKE", "SBUX", "CMG", "IBM",
    "USO", "QQQ", "SPY", "TLT", "HYG", "EWZ", "CIBR", "GDX", "ITB", "WEAT", "UAL",
]

START_FETCH = int(datetime(2026, 8, 1, tzinfo=timezone.utc).timestamp())
END_FETCH = int(datetime(2026, 11, 26, 23, 59, tzinfo=timezone.utc).timestamp())
WIN_START = "2026-10-09"
WIN_END = "2026-11-25"

# Chronological unfiltered @KobeissiLetter directional tweets (Oct 9 - Nov 20, 2026)
# Reconstructed directly from the research report's Stage 0 (unfiltered Oct) + Nov ledgers.
# Includes ALL raw tweet calls: longs, shorts, proxy ETFs, gaps, bear-tape longs, slow ATRs.
RAW_TWEETS = [
    # Oct unfiltered directional tweets (from Stage 0 + Variant K Oct)
    ("2026-10-11", "USO", "long", "Hormuz tanker strike"),
    ("2026-10-12", "WEAT", "long", "Grain blockade headline"),
    ("2026-10-12", "USO", "long", "Oil strike headline"),
    ("2026-10-14", "TLT", "short", "Hot 3.7% CPI print"),
    ("2026-10-14", "QQQ", "short", "Hot 3.7% CPI mapped to Nasdaq"),
    ("2026-10-14", "BAC", "short", "$1.2B AML fine"),
    ("2026-10-15", "ITB", "short", "Proxy ETF on pending home sales"),
    ("2026-10-16", "ORCL", "long", "Chased +10% FCF guide gap-up"),
    ("2026-10-19", "SPY", "long", "Overdone selloff sentiment call"),
    ("2026-10-20", "NFLX", "short", "Weak guidance"),
    ("2026-10-21", "GDX", "long", "Oversold breadth bounce setup"),
    ("2026-10-21", "IBM", "long", "AI-linked earnings beat"),
    ("2026-10-22", "TSLA", "long", "Flying Roadster premarket pop"),
    ("2026-10-22", "CMG", "short", "Starbucks buyout denial"),
    ("2026-10-23", "BA", "short", "Loss + guide cut"),
    ("2026-10-24", "IBIT", "short", "BTC < $80k liquidation flush"),
    ("2026-10-25", "USO", "short", "Trump no-strike comment"),
    ("2026-10-25", "HYG", "short", "CCC yields at 18%"),
    ("2026-10-26", "META", "short", "$95B stock sale for AI"),
    ("2026-10-26", "EWZ", "short", "Lula election upset"),
    ("2026-10-27", "MSFT", "long", "Earnings beat gap-up"),
    ("2026-10-28", "NOW", "short", "Weak quarter"),
    ("2026-10-28", "GOOGL", "short", "Weak quarter"),
    ("2026-10-29", "META", "long", "Beat overshadowed by $25B fine"),
    ("2026-10-29", "AMZN", "short", "Weak quarter"),
    ("2026-10-29", "INTC", "short", "PC-demand miss"),
    ("2026-10-29", "RDDT", "short", "Weak users & guide"),
    ("2026-10-29", "USO", "long", "Strike rumor duplicate"),
    ("2026-10-29", "IBIT", "short", "Binance hack (~$5.7B outflows)"),
    ("2026-10-30", "CIBR", "long", "Proxy ETF chase on Binance hack"),
    # Nov directional tweets (from Variant K Nov ledger)
    ("2026-11-02", "USO", "short", "Diplomatic end to Iran war"),
    ("2026-11-02", "ORCL", "short", "Major AI cloud/capex shock"),
    ("2026-11-03", "SHOP", "short", "Missed Q3 expectations"),
    ("2026-11-04", "USO", "short", "Oil fell below $93"),
    ("2026-11-05", "JPM", "short", "Senate probe headline"),
    ("2026-11-07", "NVDA", "short", "FT US officials China link report"),
    ("2026-11-12", "NVDA", "short", "SEC/regulatory shock"),
    ("2026-11-12", "SMCI", "short", "Accounting/guidance shock"),
    ("2026-11-12", "IBIT", "short", "BTC broke under $71,000"),
    ("2026-11-14", "IBIT", "short", "BTC broke under $66,000"),
    ("2026-11-16", "UAL", "short", "Widespread system outage"),
]


def fetch_daily(symbol):
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={START_FETCH}&period2={END_FETCH}&interval=1d&includeAdjustedClose=true"
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
            regime[b["date"]] = "bear" if b["close"] < sma20 else "bull"
    return regime


def compute_atr14_pct(bars, idx):
    if idx < 14:
        return None
    trs = []
    for j in range(idx - 13, idx + 1):
        h, l, pc = bars[j]["high"], bars[j]["low"], bars[j - 1]["close"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return (sum(trs) / 14.0) / bars[idx - 1]["close"] * 100.0


def eval_path(bars, entry_idx, side="short", target=0.20, day5_cut=False, entry_field="close"):
    entry = bars[entry_idx][entry_field]
    end_idx = len(bars) - 1
    # Cap at WIN_END
    while end_idx > entry_idx and bars[end_idx]["date"] > WIN_END:
        end_idx -= 1
    exit_idx = end_idx
    exit_price = bars[end_idx]["close"]
    reason = "Nov 25 close"

    for k in range(entry_idx + 1, end_idx + 1):
        c = bars[k]["close"]
        ret = (entry - c) / entry if side == "short" else (c - entry) / entry
        day_num = k - entry_idx
        if target is not None and ret >= target:
            exit_idx, exit_price, reason = k, c, f"+{int(target*100)}% target"
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


def simulate_portfolio(events, mode, allow_duplicates=False):
    if mode == "R":
        start_cash = 25000.0
    elif mode == "Q":
        start_cash = 30000.0
    else:
        start_cash = 100000.0

    equity = start_cash
    peak_eq = start_cash
    max_dd_pct = 0.0
    peak_cash_used = 0.0
    open_pos = []
    taken = []

    for ev in events:
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

        if not allow_duplicates and any(op["ticker"] == ev["ticker"] for op in open_pos):
            continue

        cur_cash_used = sum(op["cash"] for op in open_pos)
        is_short = ev["side"] == "short"

        if mode == "R":
            if cur_cash_used + 5000.0 > 25000.0:
                continue
            cash, notional, margin_borrowed = 5000.0, 10000.0, 5000.0
            p = ev["path_R"]
        elif mode == "Q":
            if cur_cash_used + 5000.0 > 30000.0:
                continue
            cash, notional, margin_borrowed = 5000.0, 5000.0, 0.0
            p = ev["path_Q"]
        else:  # K
            if ev.get("use_regime", False):
                size = 5000.0 if ev["regime"] == "bear" else 2500.0
            else:
                size = 5000.0
            cash, notional, margin_borrowed = size, size, 0.0
            p = ev["path_K"]

        gross_pnl = notional * p["gross_ret"]
        slippage = notional * 0.0020
        borrow = (notional * 0.03 * (p["cal_days"] / 365.0)) if is_short else 0.0
        margin_int = margin_borrowed * 0.065 * (p["cal_days"] / 365.0)
        net_pnl = gross_pnl - slippage - borrow - margin_int

        rec = {
            "ticker": ev["ticker"],
            "side": ev["side"],
            "entry_date": p["entry_date"],
            "exit_date": p["exit_date"],
            "cash": cash,
            "notional": notional,
            "net_pnl": round(net_pnl, 2),
            "ret_pct": round(p["gross_ret"] * 100.0, 2),
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
        "trades": len(taken),
        "wins": len(wins),
        "losses": len(losses),
        "wr_pct": round(len(wins) / len(taken) * 100.0, 1) if taken else 0.0,
        "capital_base": round(denom, 2),
        "net_pnl": total_net,
        "roc_pct": roc_pct,
        "pf": pf,
        "max_dd_pct": round(max_dd_pct, 2),
        "best": f"{best['ticker']} ({best['side']} {best['entry_date']} +${best['net_pnl']:.0f})" if best else None,
        "worst": f"{worst['ticker']} ({worst['side']} {worst['entry_date']} ${worst['net_pnl']:.0f})" if worst else None,
    }


def main():
    cache = {}
    for sym in set(TICKERS):
        try:
            cache[sym] = fetch_daily(sym)
        except Exception:
            pass

    spy_regime = compute_spy_regime(cache["SPY"])

    # --- TEST 1: MARKET-FACTORS-ONLY (NO TWEETS) in Oct 9 - Nov 25, 2026 ---
    mkt_high_atr = []
    mkt_all_atr = []
    for sym, bars in cache.items():
        if sym in ("SPY", "QQQ", "TLT", "HYG", "USO", "EWZ", "CIBR", "GDX", "ITB", "WEAT"):
            continue
        last_idx = -999
        for i in range(20, len(bars) - 1):
            d = bars[i]["date"]
            if d < WIN_START or d > "2026-11-20":
                continue
            if i - last_idx < 10:
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
                "side": "short",
                "entry_date": d,
                "atr_pct": round(atr_pct, 2),
                "regime": spy_regime.get(d, "bear"),
                "use_regime": True,
                "path_R": eval_path(bars, i, "short", target=0.20, day5_cut=False, entry_field="close"),
                "path_Q": eval_path(bars, i, "short", target=0.20, day5_cut=True, entry_field="close"),
                "path_K": eval_path(bars, i, "short", target=None, day5_cut=False, entry_field="close"),
            }
            mkt_all_atr.append(ev)
            if sym == "IBIT" or atr_pct >= 3.2:
                mkt_high_atr.append(ev)
            last_idx = i

    mkt_high_atr.sort(key=lambda e: (e["entry_date"], e["ticker"]))
    mkt_all_atr.sort(key=lambda e: (e["entry_date"], e["ticker"]))

    # --- TEST 2: TWEETS-ONLY (NO MARKET FACTORS / NO FILTERS) in Oct 9 - Nov 25, 2026 ---
    tw_events = []
    for post_dt, sym, side, note in RAW_TWEETS:
        bars = cache.get(sym)
        if not bars:
            continue
        # Find first trading day >= post_dt (next available open)
        idx = next((i for i, b in enumerate(bars) if b["date"] >= post_dt), None)
        if idx is None or idx >= len(bars) - 1:
            continue
        ev = {
            "ticker": sym,
            "side": side,
            "entry_date": bars[idx]["date"],
            "regime": "none",
            "use_regime": False,
            "path_R": eval_path(bars, idx, side, target=0.20, day5_cut=False, entry_field="open"),
            "path_Q": eval_path(bars, idx, side, target=0.20, day5_cut=True, entry_field="open"),
            "path_K": eval_path(bars, idx, side, target=None, day5_cut=False, entry_field="open"),
        }
        tw_events.append(ev)

    tw_events.sort(key=lambda e: (e["entry_date"], e["ticker"]))

    out = {
        "window": f"{WIN_START} to {WIN_END}",
        "market_signals_found": {"all_atr": len(mkt_all_atr), "high_atr": len(mkt_high_atr)},
        "tweet_signals_loaded": len(tw_events),
        "R-MKT (Market-Only, No Tweets)": simulate_portfolio(mkt_high_atr, "R", allow_duplicates=False),
        "Q-MKT (Market-Only, No Tweets)": simulate_portfolio(mkt_high_atr, "Q", allow_duplicates=False),
        "K-MKT (Market-Only, No Tweets)": simulate_portfolio(mkt_all_atr, "K", allow_duplicates=False),
        "R-TW (Tweets-Only, No Market Filters)": simulate_portfolio(tw_events, "R", allow_duplicates=True),
        "Q-TW (Tweets-Only, No Market Filters)": simulate_portfolio(tw_events, "Q", allow_duplicates=True),
        "K-TW (Tweets-Only, No Market Filters)": simulate_portfolio(tw_events, "K", allow_duplicates=True),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
