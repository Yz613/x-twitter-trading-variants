"""
Shlomo's Variant Backtest — 8-Metric Ticket-Quality Rubric (Oct 9 - Nov 25, 2026)
=================================================================================
Applies Shlomo's exact 8 equal-weight metrics (0.0-10.0, publish floor >= 3.0)
across the full chronological @KobeissiLetter directional tweet stream (41 posts,
Oct 9 - Nov 25, 2026) priced on real Yahoo Finance daily OHLC bars.

Metrics (equal weight):
  1. directional_clarity
  2. instrument_specificity
  3. level_and_trigger
  4. evidence
  5. horizon
  6. invalidation
  7. entry_quality   (computed objectively from Yahoo Finance pre-entry move)
  8. conflict_check  (computed objectively from same/adjacent-day opposite tweets)

Evaluated on BOTH:
  - 5-Session Fixed Hold (per Shlomo's set_improvements recommendation)
  - Hold to Nov 25 Close (apples-to-apples with Variants A-R)
All P&L strictly net of 0.10%/leg slippage and 3.0% annualized short borrow.
"""
import json
import urllib.request
from datetime import datetime, timezone

START_FETCH = int(datetime(2026, 9, 1, tzinfo=timezone.utc).timestamp())
END_FETCH = int(datetime(2026, 11, 26, 23, 59, tzinfo=timezone.utc).timestamp())
WIN_END = "2026-11-25"

# Each tweet: (date, ticker, side, note, clarity, specificity, trigger, evidence, horizon, invalidation)
# Scores 1-6 follow Shlomo's exact Nov 25 rubric calibration; 7 (entry_quality) & 8 (conflict_check)
# are computed objectively from Yahoo OHLC and the tweet stream.
TWEETS = [
    ("2026-10-11", "USO",   "long",  "Hormuz tanker strike",              5.0, 6.5, 4.5, 6.5, 3.0, 1.5),
    ("2026-10-12", "WEAT",  "long",  "Grain blockade headline",           3.5, 5.0, 2.5, 4.5, 2.5, 1.0),
    ("2026-10-12", "USO",   "long",  "Oil strike headline (duplicate)",   4.5, 6.5, 4.0, 5.5, 2.5, 1.0),
    ("2026-10-14", "TLT",   "short", "Hot 3.7% CPI print",                4.0, 5.5, 6.5, 8.0, 3.0, 1.0),
    ("2026-10-14", "QQQ",   "short", "Hot 3.7% CPI mapped to Nasdaq",     4.5, 6.0, 6.5, 8.0, 3.0, 1.0),
    ("2026-10-14", "BAC",   "short", "$1.2B AML fine",                    6.0, 9.0, 6.5, 7.5, 3.0, 1.5),
    ("2026-10-15", "ITB",   "short", "Proxy ETF on pending home sales",   3.0, 4.0, 3.5, 5.0, 2.5, 1.0),
    ("2026-10-16", "ORCL",  "long",  "Chased +10% FCF guide gap-up",      5.5, 9.0, 7.0, 7.0, 3.0, 1.5),
    ("2026-10-19", "SPY",   "long",  "Overdone selloff sentiment call",   2.5, 4.5, 2.0, 3.0, 2.0, 1.0),
    ("2026-10-20", "NFLX",  "short", "Weak guidance",                     6.5, 9.0, 6.5, 7.5, 3.0, 1.5),
    ("2026-10-21", "GDX",   "long",  "Oversold breadth bounce setup",     2.5, 4.5, 2.5, 3.5, 2.0, 1.0),
    ("2026-10-21", "IBM",   "long",  "AI-linked earnings beat",           5.5, 9.0, 6.0, 7.0, 3.0, 1.5),
    ("2026-10-22", "TSLA",  "long",  "Flying Roadster premarket pop",     3.0, 8.5, 2.0, 3.0, 1.5, 1.0),
    ("2026-10-22", "CMG",   "short", "Starbucks buyout denial",           4.5, 8.5, 4.0, 5.5, 2.0, 1.0),
    ("2026-10-23", "BA",    "short", "Loss + guide cut",                  6.5, 9.0, 6.5, 7.5, 3.0, 1.5),
    ("2026-10-24", "IBIT",  "short", "BTC < $80k liquidation flush",      6.0, 8.5, 7.5, 7.0, 2.5, 1.5),
    ("2026-10-25", "USO",   "short", "Trump no-strike comment",           4.0, 6.0, 3.0, 4.5, 2.0, 1.0),
    ("2026-10-25", "HYG",   "short", "CCC yields at 18%",                 3.5, 5.5, 6.0, 7.0, 3.5, 1.0),
    ("2026-10-26", "META",  "short", "$95B stock sale for AI",            6.5, 9.0, 7.5, 8.0, 3.0, 1.5),
    ("2026-10-26", "EWZ",   "short", "Lula election upset",               4.5, 5.5, 4.0, 6.0, 3.0, 1.0),
    ("2026-10-27", "MSFT",  "long",  "Earnings beat gap-up",              5.5, 9.0, 6.5, 7.5, 3.0, 1.5),
    ("2026-10-28", "NOW",   "short", "Weak quarter",                      6.5, 9.0, 7.0, 8.0, 3.0, 1.5),
    ("2026-10-28", "GOOGL", "short", "Weak quarter",                      6.0, 9.0, 6.5, 7.5, 3.0, 1.5),
    ("2026-10-29", "META",  "long",  "Beat overshadowed by $25B fine",    3.5, 9.0, 5.5, 7.0, 2.5, 1.0),
    ("2026-10-29", "AMZN",  "short", "Weak quarter",                      6.0, 9.0, 6.5, 7.5, 3.0, 1.5),
    ("2026-10-29", "INTC",  "short", "PC-demand miss",                    6.5, 9.0, 7.0, 8.0, 3.0, 1.5),
    ("2026-10-29", "RDDT",  "short", "Weak users & guide",                6.5, 9.0, 7.0, 8.0, 3.0, 1.5),
    ("2026-10-29", "USO",   "long",  "Strike rumor duplicate",            2.5, 5.5, 1.5, 2.5, 1.5, 1.0),
    ("2026-10-29", "IBIT",  "short", "Binance hack (~$5.7B outflows)",    7.0, 8.5, 7.5, 8.0, 3.0, 1.5),
    ("2026-10-30", "CIBR",  "long",  "Proxy ETF chase on Binance hack",   2.5, 3.5, 1.5, 3.0, 2.0, 1.0),
    ("2026-11-02", "USO",   "short", "Diplomatic end to Iran war",        4.5, 6.0, 4.0, 5.5, 2.5, 1.0),
    ("2026-11-02", "ORCL",  "short", "Major AI cloud/capex shock",        6.5, 9.0, 7.0, 8.0, 3.0, 1.5),
    ("2026-11-03", "SHOP",  "short", "Missed Q3 expectations (-15%)",     6.5, 9.0, 7.0, 8.0, 3.0, 1.5),
    ("2026-11-04", "USO",   "short", "Oil fell below $93 on sweep",       5.0, 6.5, 6.5, 7.0, 3.0, 1.5),
    ("2026-11-05", "JPM",   "short", "CNBC Senate probe headline",        5.5, 9.0, 5.0, 7.5, 3.0, 1.5),
    ("2026-11-07", "NVDA",  "short", "FT US officials China link report", 5.0, 9.0, 4.5, 7.0, 2.5, 1.0),
    ("2026-11-12", "NVDA",  "short", "SEC/regulatory shock",              7.0, 9.0, 7.0, 8.5, 3.0, 1.5),
    ("2026-11-12", "SMCI",  "short", "Accounting/guidance shock",         7.0, 9.0, 7.0, 8.0, 3.0, 1.5),
    ("2026-11-12", "IBIT",  "short", "BTC broke under $71,000",           5.5, 8.5, 7.0, 6.5, 2.5, 1.5),
    ("2026-11-14", "IBIT",  "short", "BTC broke under $66,000 ($215M liq)", 5.5, 8.5, 7.0, 6.5, 2.5, 1.5),
    ("2026-11-16", "UAL",   "short", "Widespread system outage",          5.5, 9.0, 5.0, 7.0, 2.0, 1.5),
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
        o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if None in (o, h, l, c) or c <= 0 or o <= 0:
            continue
        dt = datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d")
        bars.append({"date": dt, "open": o, "high": h, "low": l, "close": c})
    return bars


def score_entry_quality(bars, idx, side):
    if idx < 1:
        return 5.0
    prev_c = bars[idx - 1]["close"]
    o = bars[idx]["open"]
    gap_pct = (o - prev_c) / prev_c * 100.0
    # Move already spent in the direction of the trade
    spent = gap_pct if side == "long" else -gap_pct
    if spent >= 6.0:
        return 1.5
    if spent >= 3.0:
        return 3.0
    if spent >= 1.5:
        return 4.5
    if spent >= 0.0:
        return 6.0
    return 7.0  # fresh / unspent


def score_conflict_check(all_tweets, cur_idx):
    d0, sym0, side0 = all_tweets[cur_idx][0], all_tweets[cur_idx][1], all_tweets[cur_idx][2]
    dt0 = datetime.strptime(d0, "%Y-%m-%d")
    same_ticker_opp = False
    same_day_opp = False
    for j, t in enumerate(all_tweets):
        if j == cur_idx:
            continue
        dtj = datetime.strptime(t[0], "%Y-%m-%d")
        diff = abs((dtj - dt0).days)
        if diff <= 3 and t[1] == sym0 and t[2] != side0:
            same_ticker_opp = True
        if diff == 0 and t[2] != side0:
            same_day_opp = True
    if same_ticker_opp:
        return 2.0
    if same_day_opp:
        return 4.0
    return 6.5


def eval_trade(bars, entry_idx, side, max_sessions=None, size=5000.0):
    entry = bars[entry_idx]["open"]
    end_idx = len(bars) - 1
    while end_idx > entry_idx and bars[end_idx]["date"] > WIN_END:
        end_idx -= 1
    if max_sessions is not None:
        exit_idx = min(entry_idx + max_sessions, end_idx)
    else:
        exit_idx = end_idx
    exit_price = bars[exit_idx]["close"]
    cal_days = max(
        1,
        (
            datetime.strptime(bars[exit_idx]["date"], "%Y-%m-%d")
            - datetime.strptime(bars[entry_idx]["date"], "%Y-%m-%d")
        ).days,
    )
    gross_ret = (entry - exit_price) / entry if side == "short" else (exit_price - entry) / entry
    slip = size * 0.0020
    borrow = (size * 0.03 * (cal_days / 365.0)) if side == "short" else 0.0
    net_pnl = size * gross_ret - slip - borrow
    return {
        "entry_date": bars[entry_idx]["date"],
        "exit_date": bars[exit_idx]["date"],
        "net_pnl": round(net_pnl, 2),
        "gross_ret_pct": round(gross_ret * 100.0, 2),
    }


def summarize(records, size=5000.0):
    wins = [r for r in records if r["net_pnl"] > 0]
    losses = [r for r in records if r["net_pnl"] <= 0]
    gw = sum(r["net_pnl"] for r in wins)
    gl = abs(sum(r["net_pnl"] for r in losses))
    pf = round(gw / gl, 2) if gl > 0 else None
    total_net = round(sum(r["net_pnl"] for r in records), 2)
    gross_cap = len(records) * size
    # Track peak concurrent cash
    events = []
    for r in records:
        events.append((r["entry_date"], 1, size))
        events.append((r["exit_date"], 0, -size))
    events.sort()
    cur = peak = 0.0
    for _, _, delta in events:
        cur += delta
        peak = max(peak, cur)
    roc_peak = round(total_net / peak * 100.0, 2) if peak > 0 else 0.0
    best = max(records, key=lambda r: r["net_pnl"]) if records else None
    worst = min(records, key=lambda r: r["net_pnl"]) if records else None
    return {
        "trades": len(records),
        "wins": len(wins),
        "losses": len(losses),
        "wr_pct": round(len(wins) / len(records) * 100.0, 1) if records else 0.0,
        "peak_cash": peak,
        "gross_deployed": gross_cap,
        "net_pnl": total_net,
        "roc_on_peak_pct": roc_peak,
        "pf": pf,
        "best": f"{best['ticker']} ({best['side']} {best['entry_date']} +${best['net_pnl']:.0f})" if best else None,
        "worst": f"{worst['ticker']} ({worst['side']} {worst['entry_date']} ${worst['net_pnl']:.0f})" if worst else None,
    }


def main():
    syms = sorted(set(t[1] for t in TWEETS))
    cache = {s: fetch_daily(s) for s in syms}

    scored = []
    for i, (post_dt, sym, side, note, c1, c2, c3, c4, c5, c6) in enumerate(TWEETS):
        bars = cache[sym]
        idx = next((k for k, b in enumerate(bars) if b["date"] >= post_dt), None)
        if idx is None or idx >= len(bars) - 1:
            continue
        c7 = score_entry_quality(bars, idx, side)
        c8 = score_conflict_check(TWEETS, i)
        comp = round((c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8) / 8.0, 3)
        res_5d = eval_trade(bars, idx, side, max_sessions=5, size=5000.0)
        res_nov = eval_trade(bars, idx, side, max_sessions=None, size=5000.0)
        scored.append({
            "date": post_dt,
            "ticker": sym,
            "side": side,
            "note": note,
            "composite": comp,
            "entry_quality": c7,
            "conflict_check": c8,
            "res_5d": {**res_5d, "ticker": sym, "side": side, "composite": comp},
            "res_nov": {**res_nov, "ticker": sym, "side": side, "composite": comp},
        })

    passed_3 = [s for s in scored if s["composite"] >= 3.0]
    rejected_3 = [s for s in scored if s["composite"] < 3.0]
    passed_5 = [s for s in scored if s["composite"] >= 5.0]

    out = {
        "total_tweets_scored": len(scored),
        "floor_3_0": {
            "passed": len(passed_3),
            "rejected": len(rejected_3),
            "avg_composite_passed": round(sum(s["composite"] for s in passed_3) / len(passed_3), 3),
            "rejected_tickets": [(s["date"], s["ticker"], s["side"], s["composite"]) for s in rejected_3],
            "hold_5_sessions": summarize([s["res_5d"] for s in passed_3]),
            "hold_to_nov25": summarize([s["res_nov"] for s in passed_3]),
        },
        "diagnostic_floor_5_0": {
            "passed": len(passed_5),
            "avg_composite_passed": round(sum(s["composite"] for s in passed_5) / len(passed_5), 3),
            "hold_5_sessions": summarize([s["res_5d"] for s in passed_5]),
            "hold_to_nov25": summarize([s["res_nov"] for s in passed_5]),
        },
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
