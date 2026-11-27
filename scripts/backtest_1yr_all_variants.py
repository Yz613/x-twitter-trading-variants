"""
1-Year Full Backtest Across All 32+ Variants + S&P Vibe & Priced-In Ablations
=============================================================================
Input:  /Users/yehudazahler/Downloads/tweets.jsonl (6,436 @KobeissiLetter posts, 2025-11-25 to 2026-11-26)
Market: Live Yahoo Finance daily OHLCV bars (2025-10-01 to 2026-11-26), cached locally.
Output: scripts/backtest_1yr_results.json
All P&L figures strictly net of 0.10%/leg slippage, 3.0% short borrow, and 6.5% margin interest
(except Stage 0-3 gross baselines where explicitly noted, though we compute net for fair 1yr comparison).
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import urllib.request

TWEETS_PATH = Path("/Users/yehudazahler/Downloads/tweets.jsonl")
OUT_PATH = Path(__file__).resolve().parent / "backtest_1yr_results.json"
TRADES_OUT_PATH = Path(__file__).resolve().parent.parent / "public" / "one-year" / "trades.json"
CACHE_DIR = Path(__file__).resolve().parent / ".cache_1yr_ohlc"
CACHE_DIR.mkdir(exist_ok=True)

WIN_START = "2025-11-25"
WIN_END = "2026-11-25"
FETCH_START = int(datetime(2025, 9, 15, tzinfo=timezone.utc).timestamp())
FETCH_END = int(datetime(2026, 11, 26, 23, 59, tzinfo=timezone.utc).timestamp())

CRYPTO_EXEMPT = {"IBIT", "ETHA", "FBTC", "BITO", "GBTC"}
PROXY_ETFS = {"SPY", "QQQ", "TLT", "HYG", "USO", "GLD", "SLV", "WEAT", "GDX", "ITB", "CIBR", "EWZ", "XLF", "XLE", "IWM"}

# Unambiguous company/asset name -> ticker mapping
NAME_MAP = [
    (r"\bnvidia\b|\$nvda\b", "NVDA"),
    (r"\boracle\b|\$orcl\b", "ORCL"),
    (r"\btesla\b|\$tsla\b", "TSLA"),
    (r"\bmeta platforms\b|\bmeta\b(?!-)|\$meta\b", "META"),
    (r"\bservicenow\b|\$now\b", "NOW"),
    (r"\breddit\b|\$rddt\b", "RDDT"),
    (r"\bamazon\b|\$amzn\b", "AMZN"),
    (r"\bmicrosoft\b|\$msft\b", "MSFT"),
    (r"\balphabet\b|\bgoogle\b|\$googl?\b", "GOOGL"),
    (r"\bapple\b|\$aapl\b", "AAPL"),
    (r"\bintel\b|\$intc\b", "INTC"),
    (r"\bamd\b|\$amd\b", "AMD"),
    (r"\bsuper micro\b|\bsupermicro\b|\$smci\b", "SMCI"),
    (r"\bnetflix\b|\$nflx\b", "NFLX"),
    (r"\bshopify\b|\$shop\b", "SHOP"),
    (r"\bpalantir\b|\$pltr\b", "PLTR"),
    (r"\bcoinbase\b|\$coin\b", "COIN"),
    (r"\bmicrostrategy\b|\bstrategy\b.*bitcoin|\$mstr\b", "MSTR"),
    (r"\bboeing\b|\$ba\b", "BA"),
    (r"\bjpmorgan\b|\bjp morgan\b|\$jpm\b", "JPM"),
    (r"\bbank of america\b|\$bac\b", "BAC"),
    (r"\bunited airlines\b|\$ual\b", "UAL"),
    (r"\bchipotle\b|\$cmg\b", "CMG"),
    (r"\bibm\b|\$ibm\b", "IBM"),
    (r"\bwalmart\b|\$wmt\b", "WMT"),
    (r"\btarget\b.*(?:earnings|sales|stock|shares|guidance)|\$tgt\b", "TGT"),
    (r"\bdisney\b|\$dis\b", "DIS"),
    (r"\bnike\b|\$nke\b", "NKE"),
    (r"\bstarbucks\b|\$sbux\b", "SBUX"),
    (r"\brobinhood\b|\$hood\b", "HOOD"),
    (r"\bapplovin\b|\$app\b", "APP"),
    (r"\bsnowflake\b|\$snow\b", "SNOW"),
    (r"\bcrowdstrike\b|\$crwd\b", "CRWD"),
    (r"\bpalo alto\b|\$panw\b", "PANW"),
    (r"\bbroadcom\b|\$avgo\b", "AVGO"),
    (r"\bmicron\b|\$mu\b", "MU"),
    (r"\bmarvell\b|\$mrvl\b", "MRVL"),
    (r"\buber\b|\$uber\b", "UBER"),
    (r"\bpaypal\b|\$pypl\b", "PYPL"),
    (r"\bspotify\b|\$spot\b", "SPOT"),
    (r"\bcarvana\b|\$cvna\b", "CVNA"),
    (r"\bsofi\b|\$sofi\b", "SOFI"),
    (r"\baffirm\b|\$afrm\b", "AFRM"),
    (r"\bdell\b|\$dell\b", "DELL"),
    (r"\bsnapchat\b|\bsnap inc\b|\$snap\b", "SNAP"),
    (r"\barm holdings\b|\$arm\b", "ARM"),
    (r"\bcoreweave\b|\$crwv\b", "CRWV"),
    (r"\bbitcoin\b|\bbtc\b|\$ibit\b", "IBIT"),
    (r"\bethereum\b|\bether\b|\$etha\b", "ETHA"),
    (r"\bgold\b|\$gld\b", "GLD"),
    (r"\bsilver\b|\$slv\b", "SLV"),
    (r"\bcrude oil\b|\bwti\b|\boil prices\b|\bus oil\b|\$uso\b", "USO"),
    (r"\bnasdaq 100\b|\bnasdaq\b|\$qqq\b", "QQQ"),
    (r"\bs&p 500\b|\$spy\b", "SPY"),
    (r"\b10-year\b|\b30-year\b|\btreasury\b|\$tlt\b", "TLT"),
]

COMPILED_NAMES = [(re.compile(pat, re.I), sym) for pat, sym in NAME_MAP]

BEAR_HARD = re.compile(
    r"\b(misses|missed|cuts guidance|cut guidance|lowers guidance|weak quarter|sec probe|doj|investigation|"
    r"hacked|hack|outflows|liquidation|liquidated|fined|fine|lawsuit|stock sale|equity raise|dilution|"
    r"layoffs|outage|recall|downgraded|warns|warning|plunges|plunged|crashes|crashed|tumbles|tumbled|"
    r"sinks|sank|plummets|plummeted|falls below|fell below|breaks below|broke below|broke under|drops \d+%)\b",
    re.I,
)
BEAR_SOFT = re.compile(
    r"\b(falls|fell|drops|dropped|down \d|selloff|sell-off|bearish|short|puts|slumps|slumped|decline|declines|"
    r"loses|lost \$|tariff|tariffs|hot cpi|hot pce|rate hike|hike odds|inflation jumps|worst day|worst week)\b",
    re.I,
)
BULL_HARD = re.compile(
    r"\b(beats|beat expectations|raises guidance|raised guidance|surges|surged|soars|soared|buyback|"
    r"acquisition|acquires|contract|approved|upgraded|record revenue|reclaims|reclaimed|rallies|rallied|"
    r"jumps \d+%|breaks above|broke above|all-time high|record high)\b",
    re.I,
)
BULL_SOFT = re.compile(
    r"\b(rises|rose|gains|gained|up \d|bullish|buy|calls|oversold|rebound|bounce|rate cut|cut odds|m2 rose)\b",
    re.I,
)
NAMED_SOURCE = re.compile(r"\b(reuters|wsj|wall street journal|ft|financial times|cnbc|bloomberg|sec|doj|fed|bls|bea)\b", re.I)
PRICE_OR_NUM = re.compile(r"(\$\d[\d,.]*[bmk]?|\d+(?:\.\d+)?%)", re.I)
HORIZON_RE = re.compile(r"\b(24 hours|today|intraday|this week|next week|quarter|q[1-4]|month|year|202[567]|days|weeks)\b", re.I)
INVALIDATION_RE = re.compile(r"\b(stop|invalidation|invalidated|below \$\d+|above \$\d+|reclaim)\b", re.I)

MARKET_ONLY_UNIVERSE = [
    "NVDA", "META", "ORCL", "NOW", "RDDT", "AMD", "INTC", "SMCI", "PLTR",
    "TSLA", "SHOP", "NFLX", "AMZN", "GOOGL", "MSFT", "COIN", "MSTR", "IBIT",
    "HOOD", "APP", "SNOW", "DDOG", "NET", "CRWD", "PANW", "MDB", "ZS",
    "ARM", "AVGO", "MU", "MRVL", "UBER", "DASH", "ABNB", "PYPL", "SPOT",
    "RBLX", "DKNG", "SOFI", "AFRM", "CVNA", "CELH", "ANET", "DELL", "ESTC",
    "GTLB", "SNAP", "PINS", "ROKU", "TTD", "OKTA", "TWLO", "DOCU", "ZM",
    "U", "PATH", "CFLT", "BILL", "HUBS", "TEAM",
    "BA", "JPM", "BAC", "DIS", "WMT", "TGT", "NKE", "SBUX", "CMG", "IBM",
]


def extract_signals():
    signals = []
    total_rows = 0
    orig_rows = 0
    with TWEETS_PATH.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            total_rows += 1
            text = (obj.get("text") or "").strip()
            if not text or text.startswith("RT @") or obj.get("in_reply_to_user_id"):
                continue
            refs = obj.get("referenced_tweets") or []
            if any(r.get("type") in ("retweeted", "replied_to") for r in refs):
                continue
            orig_rows += 1

            # Match first unambiguous ticker
            ticker = None
            for pat, sym in COMPILED_NAMES:
                if pat.search(text):
                    ticker = sym
                    break
            if not ticker:
                continue

            bh = len(BEAR_HARD.findall(text))
            bs = len(BEAR_SOFT.findall(text))
            lh = len(BULL_HARD.findall(text))
            ls = len(BULL_SOFT.findall(text))
            bear_score = bh * 2 + bs
            bull_score = lh * 2 + ls
            if bear_score == 0 and bull_score == 0:
                continue
            if bear_score == bull_score:
                continue
            side = "short" if bear_score > bull_score else "long"

            is_proxy = ticker in PROXY_ETFS
            is_crypto = ticker in CRYPTO_EXEMPT
            hard_hits = bh if side == "short" else lh

            # Assign Tier 1-5 (zero hindsight)
            if not is_proxy and hard_hits >= 2:
                tier = 5
            elif not is_proxy and hard_hits == 1:
                tier = 4
            elif is_proxy and hard_hits >= 1:
                tier = 3
            elif not is_proxy and (bs if side == "short" else ls) >= 2:
                tier = 3
            elif not is_proxy:
                tier = 2
            else:
                tier = 1

            # Shlomo's first 6 text-based metrics (0.0-10.0), calibrated to his Nov 25 rubric
            explicit_order = bool(re.search(r"\b(buy|sell|short|long|bullish|bearish|calls|puts)\b", text, re.I))
            c1 = 7.0 if explicit_order else (6.0 if hard_hits >= 2 else (5.0 if hard_hits == 1 else 3.5))
            c2 = 9.0 if (not is_proxy and not is_crypto) else (8.5 if is_crypto else 5.5)
            nums = PRICE_OR_NUM.findall(text)
            c3 = 7.5 if len(nums) >= 2 else (6.0 if len(nums) == 1 else 2.5)
            has_src = bool(NAMED_SOURCE.search(text))
            c4 = 8.0 if (has_src and nums) else (6.5 if (has_src or len(nums) >= 2) else (4.5 if nums else 2.5))
            c5 = 4.0 if HORIZON_RE.search(text) else 2.0
            c6 = 3.0 if INVALIDATION_RE.search(text) else 1.5

            created = obj.get("created_at") or ""
            dt_date = created[:10]
            if dt_date < WIN_START or dt_date > WIN_END:
                continue

            signals.append({
                "id": str(obj.get("id") or ""),
                "date": dt_date,
                "created_at": created,
                "ticker": ticker,
                "side": side,
                "tier": tier,
                "is_proxy": is_proxy,
                "is_crypto": is_crypto,
                "rubric6": (c1, c2, c3, c4, c5, c6),
                "text": text,
            })

    signals.sort(key=lambda s: (s["created_at"], s["ticker"]))
    return total_rows, orig_rows, signals


def fetch_daily(symbol):
    p = CACHE_DIR / f"{symbol}.json"
    if p.exists():
        return json.loads(p.read_text())
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={FETCH_START}&period2={FETCH_END}&interval=1d&includeAdjustedClose=true"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
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
            bars.append({"date": dt, "open": float(o), "high": float(h), "low": float(l), "close": float(c), "volume": float(v or 0)})
        if bars:
            p.write_text(json.dumps(bars))
        return bars
    except Exception:
        return []


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
    return round((sum(trs) / 14.0) / bars[idx - 1]["close"] * 100.0, 2)


def eval_exit(bars, entry_idx, side, cfg, entry_field="open"):
    entry = bars[entry_idx][entry_field]
    end_idx = len(bars) - 1
    while end_idx > entry_idx and bars[end_idx]["date"] > WIN_END:
        end_idx -= 1
    max_hold = cfg.get("max_hold_days", 20)
    limit_idx = min(entry_idx + max_hold, end_idx) if max_hold else end_idx
    exit_idx = limit_idx
    exit_price = bars[limit_idx]["close"]

    target = cfg.get("profit_target_pct")
    cat_stop = cfg.get("catastrophe_stop_pct")
    intraday_stop = cfg.get("intraday_stop_pct")
    trailing_stop = cfg.get("trailing_stop_pct")
    day5_cut = cfg.get("day5_dead_money_cut", False)

    peak_ret = 0.0
    for k in range(entry_idx + 1, limit_idx + 1):
        bar = bars[k]
        c = bar["close"]
        ret = (entry - c) / entry if side == "short" else (c - entry) / entry
        if intraday_stop is not None:
            wpx = bar["high"] if side == "short" else bar["low"]
            wret = (entry - wpx) / entry if side == "short" else (wpx - entry) / entry
            if wret <= -intraday_stop:
                exit_idx = k
                exit_price = entry * (1 + intraday_stop) if side == "short" else entry * (1 - intraday_stop)
                break
        if target is not None and ret >= target:
            exit_idx, exit_price = k, c
            break
        if cat_stop is not None and ret <= -cat_stop:
            exit_idx, exit_price = k, c
            break
        if trailing_stop is not None:
            peak_ret = max(peak_ret, ret)
            if peak_ret >= 0.10 and (peak_ret - ret) >= trailing_stop:
                exit_idx, exit_price = k, c
                break
        if day5_cut and (k - entry_idx) == 5 and ret < 0.02:
            exit_idx, exit_price = k, c
            break

    cal_days = max(1, (datetime.strptime(bars[exit_idx]["date"], "%Y-%m-%d") - datetime.strptime(bars[entry_idx]["date"], "%Y-%m-%d")).days)
    gross_ret = (entry - exit_price) / entry if side == "short" else (exit_price - entry) / entry
    return bars[entry_idx]["date"], bars[exit_idx]["date"], cal_days, gross_ret, round(entry, 2), round(exit_price, 2)


def simulate(events, cfg):
    cash_cap = cfg.get("cash_cap")
    leverage = float(cfg.get("leverage", 1.0))
    allow_dups = cfg.get("allow_duplicates", False)
    equity = float(cash_cap or 100000.0)
    peak_eq = equity
    max_dd = 0.0
    peak_cash = 0.0
    open_pos = []
    taken = []

    for ev in events:
        still = []
        for op in open_pos:
            if op["exit_date"] <= ev["date"]:
                equity += op["net_pnl"]
                peak_eq = max(peak_eq, equity)
                dd = (equity - peak_eq) / peak_eq * 100.0 if peak_eq > 0 else -100.0
                max_dd = min(max_dd, dd)
            else:
                still.append(op)
        open_pos = still

        sym, side, tier = ev["ticker"], ev["side"], ev["tier"]
        if not allow_dups and any(op["ticker"] == sym for op in open_pos):
            continue
        if tier < cfg.get("min_tier", 1):
            continue
        if cfg.get("direct_only", False) and sym in PROXY_ETFS and sym not in CRYPTO_EXEMPT:
            continue
        if cfg.get("shlomo_min_score") is not None and ev["shlomo_comp"] < cfg["shlomo_min_score"]:
            continue
        if cfg.get("min_entry_quality") is not None and ev["entry_q"] < cfg["min_entry_quality"]:
            continue
        if cfg.get("min_conflict_check") is not None and ev["conflict_q"] < cfg["min_conflict_check"]:
            continue

        # Priced-in filters (can be enabled independently of ATR/SPY!)
        if cfg.get("skip_long_gap_gt_3", False) and side == "long" and ev["gap_pct"] > 3.0:
            continue
        if cfg.get("tape_confirm", False):
            if side == "short" and ev["day_chg"] > 1.0:
                continue
            if side == "long" and ev["day_chg"] < -1.0:
                continue

        # Velocity & macro regime filters
        if not cfg.get("bypass_market_filters", False):
            min_atr = cfg.get("min_atr_pct", 0.0)
            if min_atr > 0 and not (cfg.get("crypto_exempt", True) and sym in CRYPTO_EXEMPT):
                if ev["atr"] is None or ev["atr"] < min_atr:
                    continue
            if cfg.get("ban_bear_longs", False) and ev["regime"] == "bear" and side == "long":
                continue

        mode = cfg.get("sizing_mode", "fixed_cash")
        if mode == "tier_map":
            tmap = {5: 10000.0, 4: 5000.0, 3: 2000.0, 2: 500.0, 1: 20.0}
            cash = tmap.get(tier, 5000.0)
            if cfg.get("spy_regime_gate", False):
                if ev["regime"] == "bear" and side == "long":
                    cash *= 0.25
                elif ev["regime"] == "bull" and side == "short" and tier <= 3:
                    cash *= 0.5
        elif mode == "regime_fixed_cash":
            bc = float(cfg.get("cash_per_trade", 5000.0))
            cash = bc if ev["regime"] == "bear" else bc * 0.5
        elif mode == "shlomo_tiered":
            sc = ev["shlomo_comp"]
            cash = 10000.0 if sc >= 5.75 else (5000.0 if sc >= 5.25 else 2500.0)
        elif mode == "fractional_kelly":
            if equity <= 2000.0:
                continue
            frac = cfg.get("kelly_fraction_t5", 0.16) if tier >= 5 else cfg.get("kelly_fraction_t4", 0.12)
            cash = round(equity * frac, 2)
            if sum(op["cash"] for op in open_pos) + cash > equity * 0.80:
                continue
        else:
            cash = float(cfg.get("cash_per_trade", 5000.0))

        cur_cash = sum(op["cash"] for op in open_pos)
        if cash_cap is not None and cur_cash + cash > cash_cap:
            continue

        notional = cash * leverage
        ed, xd, cdays, gret, epx, xpx = eval_exit(ev["bars"], ev["idx"], side, cfg, entry_field=ev["entry_field"])
        slip = notional * 0.0020
        borrow = (notional * 0.03 * (cdays / 365.0)) if side == "short" else 0.0
        mint = max(0.0, notional - cash) * 0.065 * (cdays / 365.0)
        net_pnl = notional * gret - slip - borrow - mint

        rec = {
            "ticker": sym, "side": side, "entry_date": ed, "exit_date": xd,
            "entry_px": epx, "exit_px": xpx, "hold_days": cdays,
            "cash": round(cash, 2), "notional": round(notional, 2),
            "gross_ret_pct": round(gret * 100.0, 2),
            "net_pnl": round(net_pnl, 2),
            "tier": tier, "shlomo": round(ev["shlomo_comp"], 2),
            "gap_pct": round(ev["gap_pct"], 2), "day_chg": round(ev["day_chg"], 2),
            "tid": ev.get("tid", ""),
        }
        open_pos.append(rec)
        taken.append(rec)
        peak_cash = max(peak_cash, sum(op["cash"] for op in open_pos))

    for op in sorted(open_pos, key=lambda x: x["exit_date"]):
        equity += op["net_pnl"]
        peak_eq = max(peak_eq, equity)
        dd = (equity - peak_eq) / peak_eq * 100.0 if peak_eq > 0 else -100.0
        max_dd = min(max_dd, dd)

    wins = [t for t in taken if t["net_pnl"] > 0]
    losses = [t for t in taken if t["net_pnl"] <= 0]
    gw = sum(t["net_pnl"] for t in wins)
    gl = abs(sum(t["net_pnl"] for t in losses))
    pf = round(gw / gl, 2) if gl > 0 else ("INF" if gw > 0 else 0.0)
    total_net = round(sum(t["net_pnl"] for t in taken), 2)
    denom = float(cash_cap) if cash_cap is not None else peak_cash
    roc = round(total_net / denom * 100.0, 2) if denom > 0 else 0.0
    return {
        "trades": len(taken), "wins": len(wins), "losses": len(losses),
        "wr_pct": round(len(wins) / len(taken) * 100.0, 1) if taken else 0.0,
        "capital_base": round(denom, 2), "net_pnl": total_net, "roc_pct": roc,
        "pf": pf, "max_dd_pct": round(max_dd, 2),
        "trade_log": taken,
    }


def simulate_spy_vibe(spy_bars, mode="long_cash", capital=25000.0):
    """Pure S&P 500 Vibe Check: trade SPY using ONLY SPY vs. 20-day SMA (zero tweets)."""
    closes = [b["close"] for b in spy_bars]
    eq = capital
    peak = capital
    max_dd = 0.0
    pos = 0  # 1=long, -1=short, 0=cash
    entry_px = None
    entry_date = None
    trades = wins = losses = 0
    gw = gl = 0.0
    tlog = []

    for i in range(19, len(spy_bars)):
        b = spy_bars[i]
        if b["date"] < WIN_START or b["date"] > WIN_END:
            continue
        sma20 = sum(closes[i - 19 : i + 1]) / 20.0
        target_pos = 1 if b["close"] >= sma20 else (0 if mode == "long_cash" else (-1 if mode == "long_short" else 1))
        if mode == "buy_hold":
            target_pos = 1
        if target_pos != pos:
            if pos != 0 and entry_px:
                ret = (b["close"] - entry_px) / entry_px if pos == 1 else (entry_px - b["close"]) / entry_px
                cash_dep = round(eq, 2)
                pnl = eq * ret - eq * 0.0020
                eq += pnl
                trades += 1
                if pnl > 0:
                    wins += 1; gw += pnl
                else:
                    losses += 1; gl += abs(pnl)
                cdays = max(1, (datetime.strptime(b["date"], "%Y-%m-%d") - datetime.strptime(entry_date, "%Y-%m-%d")).days)
                tlog.append({
                    "ticker": "SPY", "side": "long" if pos == 1 else "short",
                    "entry_date": entry_date, "exit_date": b["date"],
                    "entry_px": round(entry_px, 2), "exit_px": round(b["close"], 2), "hold_days": cdays,
                    "cash": cash_dep, "notional": cash_dep, "gross_ret_pct": round(ret * 100.0, 2),
                    "net_pnl": round(pnl, 2), "tier": 0, "shlomo": 0.0, "gap_pct": 0.0, "day_chg": 0.0,
                    "tid": "SPY_VIBE",
                })
            pos = target_pos
            entry_px = b["close"] if pos != 0 else None
            entry_date = b["date"] if pos != 0 else None
        mark_eq = eq
        if pos != 0 and entry_px:
            ret = (b["close"] - entry_px) / entry_px if pos == 1 else (entry_px - b["close"]) / entry_px
            mark_eq = eq * (1 + ret)
        peak = max(peak, mark_eq)
        max_dd = min(max_dd, (mark_eq - peak) / peak * 100.0)

    if pos != 0 and entry_px:
        b = spy_bars[-1]
        ret = (b["close"] - entry_px) / entry_px if pos == 1 else (entry_px - b["close"]) / entry_px
        cash_dep = round(eq, 2)
        pnl = eq * ret - eq * 0.0020
        eq += pnl
        trades += 1
        if pnl > 0:
            wins += 1; gw += pnl
        else:
            losses += 1; gl += abs(pnl)
        cdays = max(1, (datetime.strptime(b["date"], "%Y-%m-%d") - datetime.strptime(entry_date, "%Y-%m-%d")).days)
        tlog.append({
            "ticker": "SPY", "side": "long" if pos == 1 else "short",
            "entry_date": entry_date, "exit_date": b["date"],
            "entry_px": round(entry_px, 2), "exit_px": round(b["close"], 2), "hold_days": cdays,
            "cash": cash_dep, "notional": cash_dep, "gross_ret_pct": round(ret * 100.0, 2),
            "net_pnl": round(pnl, 2), "tier": 0, "shlomo": 0.0, "gap_pct": 0.0, "day_chg": 0.0,
            "tid": "SPY_VIBE",
        })

    net = round(eq - capital, 2)
    return {
        "trades": trades, "wins": wins, "losses": losses,
        "wr_pct": round(wins / trades * 100.0, 1) if trades else 0.0,
        "capital_base": capital, "net_pnl": net, "roc_pct": round(net / capital * 100.0, 2),
        "pf": round(gw / gl, 2) if gl > 0 else ("INF" if gw > 0 else 0.0),
        "max_dd_pct": round(max_dd, 2),
        "trade_log": tlog,
    }


def main():
    total_rows, orig_rows, raw_signals = extract_signals()
    all_syms = sorted(set(MARKET_ONLY_UNIVERSE) | set(s["ticker"] for s in raw_signals) | {"SPY"})

    with ThreadPoolExecutor(max_workers=12) as pool:
        cache = dict(zip(all_syms, pool.map(fetch_daily, all_syms)))

    spy_bars = cache["SPY"]
    spy_regime = compute_spy_regime(spy_bars)

    # Enrich tweet events with OHLC, ATR, gap, day_chg, SPY regime, and Shlomo's 8-metric composite
    tweet_events = []
    # Pre-index by date for fast conflict check
    for i, s in enumerate(raw_signals):
        bars = cache.get(s["ticker"]) or []
        idx = next((k for k, b in enumerate(bars) if b["date"] >= s["date"]), None)
        if idx is None or idx >= len(bars) - 1:
            continue
        prev_c = bars[idx - 1]["close"] if idx > 0 else bars[idx]["open"]
        o, c = bars[idx]["open"], bars[idx]["close"]
        gap_pct = (o - prev_c) / prev_c * 100.0
        day_chg = (c - prev_c) / prev_c * 100.0
        atr = compute_atr14_pct(bars, idx - 1)

        # Objective Shlomo metric 7: entry_quality
        spent = gap_pct if s["side"] == "long" else -gap_pct
        c7 = 1.5 if spent >= 6.0 else (3.0 if spent >= 3.0 else (4.5 if spent >= 1.5 else (6.0 if spent >= 0.0 else 7.0)))

        # Objective Shlomo metric 8: conflict_check (look in +-30 neighbor window)
        d0 = datetime.strptime(s["date"], "%Y-%m-%d")
        same_t_opp = same_d_opp = False
        for j in range(max(0, i - 40), min(len(raw_signals), i + 40)):
            if j == i:
                continue
            sj = raw_signals[j]
            diff = abs((datetime.strptime(sj["date"], "%Y-%m-%d") - d0).days)
            if diff <= 3 and sj["ticker"] == s["ticker"] and sj["side"] != s["side"]:
                same_t_opp = True
            if diff == 0 and sj["side"] != s["side"]:
                same_d_opp = True
        c8 = 2.0 if same_t_opp else (4.0 if same_d_opp else 6.5)

        c1, c2, c3, c4, c5, c6 = s["rubric6"]
        comp = round((c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8) / 8.0, 3)

        tweet_events.append({
            "ticker": s["ticker"], "side": s["side"], "tier": s["tier"], "date": bars[idx]["date"],
            "bars": bars, "idx": idx, "atr": atr, "gap_pct": gap_pct, "day_chg": day_chg,
            "regime": spy_regime.get(bars[idx]["date"], "bull"),
            "shlomo_comp": comp, "entry_q": c7, "conflict_q": c8, "entry_field": "open",
            "tid": s["id"],
        })

    # Build tweet lookup table (deduplicated by tweet ID for compact trades.json)
    tweet_lookup = {
        s["id"]: {"created_at": s["created_at"], "text": s["text"]}
        for s in raw_signals
    }
    tweet_lookup["MKT_ONLY"] = {"created_at": "", "text": "[Market-Only Technical Breakdown: -8% to -28% drop, red close, >=2x 20d avg volume — zero tweets used]"}
    tweet_lookup["SPY_VIBE"] = {"created_at": "", "text": "[Pure S&P 500 Vibe Check: SPY Close vs. 20-Day SMA crossover — zero tweets used]"}

    # Build 1-year Market-Only breakdown events (-8% to -28%, red close, >= 2x avg vol)
    mkt_events = []
    for sym in MARKET_ONLY_UNIVERSE:
        bars = cache.get(sym) or []
        last_idx = -999
        for i in range(20, len(bars) - 1):
            d = bars[i]["date"]
            if d < WIN_START or d > "2026-11-20" or (i - last_idx) < 10:
                continue
            prev_c, o, c = bars[i - 1]["close"], bars[i]["open"], bars[i]["close"]
            drop = (c - prev_c) / prev_c * 100.0
            if not (-28.0 <= drop <= -8.0) or c >= o:
                continue
            avg_v = sum(b["volume"] for b in bars[i - 20 : i]) / 20.0
            if avg_v > 0 and bars[i]["volume"] < 2.0 * avg_v:
                continue
            mkt_events.append({
                "ticker": sym, "side": "short", "tier": 5, "date": d,
                "bars": bars, "idx": i, "atr": compute_atr14_pct(bars, i - 1),
                "gap_pct": (o - prev_c) / prev_c * 100.0, "day_chg": drop,
                "regime": spy_regime.get(d, "bull"), "shlomo_comp": 6.0, "entry_q": 6.0, "conflict_q": 6.5,
                "entry_field": "close", "tid": "MKT_ONLY",
            })
            last_idx = i
    mkt_events.sort(key=lambda e: (e["date"], e["ticker"]))

    # Define all variants to test across the full 1-year window
    VARIANT_SPECS = [
        # Core A-X
        ("Variant A", "core", tweet_events, {"sizing_mode": "fixed_cash", "cash_per_trade": 10000, "allow_duplicates": True, "bypass_market_filters": True, "max_hold_days": 20}),
        ("Variant B", "core", tweet_events, {"direct_only": True, "skip_long_gap_gt_3": True, "sizing_mode": "fixed_cash", "cash_per_trade": 10000, "max_hold_days": 20}),
        ("Variant C", "core", tweet_events, {"direct_only": True, "skip_long_gap_gt_3": True, "intraday_stop_pct": 0.08, "max_hold_days": 10, "sizing_mode": "fixed_cash", "cash_per_trade": 10000}),
        ("Variant F", "core", tweet_events, {"direct_only": True, "skip_long_gap_gt_3": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant G", "core", tweet_events, {"direct_only": True, "skip_long_gap_gt_3": True, "catastrophe_stop_pct": 0.12, "trailing_stop_pct": 0.10, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant H", "core", tweet_events, {"direct_only": True, "skip_long_gap_gt_3": True, "allow_duplicates": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant I", "core", tweet_events, {"direct_only": True, "skip_long_gap_gt_3": True, "profit_target_pct": 0.15, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant J", "core", tweet_events, {"direct_only": True, "min_tier": 2, "skip_long_gap_gt_3": True, "tape_confirm": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant K", "core", tweet_events, {"direct_only": True, "min_tier": 2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant L", "core", tweet_events, {"direct_only": True, "min_tier": 2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "sizing_mode": "fixed_cash", "cash_per_trade": 3500, "max_hold_days": 20}),
        ("Variant M", "core", tweet_events, {"direct_only": True, "min_tier": 2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant N", "core", tweet_events, {"direct_only": True, "min_tier": 4, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant O", "core", tweet_events, {"direct_only": True, "min_tier": 4, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "allow_duplicates": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant P", "core", tweet_events, {"direct_only": True, "min_tier": 4, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        ("Variant Q", "core", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 30000, "profit_target_pct": 0.20, "day5_dead_money_cut": True, "max_hold_days": 20}),
        ("Variant R", "core", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 20}),
        ("Variant S", "core", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fractional_kelly", "kelly_fraction_t5": 0.16, "kelly_fraction_t4": 0.12, "cash_cap": 25000, "profit_target_pct": 0.20, "catastrophe_stop_pct": 0.15, "day5_dead_money_cut": True, "max_hold_days": 15}),
        ("Variant T", "core", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fractional_kelly", "kelly_fraction_t5": 0.32, "kelly_fraction_t4": 0.24, "cash_cap": 25000, "catastrophe_stop_pct": 0.15, "day5_dead_money_cut": True, "max_hold_days": 20}),
        ("Variant U", "core", tweet_events, {"direct_only": True, "min_tier": 5, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fractional_kelly", "kelly_fraction_t5": 0.16, "kelly_fraction_t4": 0.12, "cash_cap": 25000, "profit_target_pct": 0.20, "catastrophe_stop_pct": 0.15, "max_hold_days": 15}),
        ("Variant V", "core", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fractional_kelly", "kelly_fraction_t5": 0.16, "kelly_fraction_t4": 0.12, "cash_cap": 25000, "profit_target_pct": 0.20, "catastrophe_stop_pct": 0.15, "max_hold_days": 15}),
        ("Variant X", "core", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": True, "ban_bear_longs": True, "sizing_mode": "fractional_kelly", "kelly_fraction_t5": 0.20, "kelly_fraction_t4": 0.13, "cash_cap": 25000, "profit_target_pct": 0.20, "catastrophe_stop_pct": 0.15, "max_hold_days": 20}),

        # Shlomo Suite (5)
        ("Shlomo-3.0", "shlomo", tweet_events, {"shlomo_min_score": 3.0, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 5}),
        ("Shlomo-5.25", "shlomo", tweet_events, {"shlomo_min_score": 5.25, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 5}),
        ("Shlomo-5.50", "shlomo", tweet_events, {"shlomo_min_score": 5.50, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 5}),
        ("Shlomo-Sniper", "shlomo", tweet_events, {"shlomo_min_score": 5.50, "min_entry_quality": 4.5, "min_conflict_check": 5.0, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 5}),
        ("Shlomo-Tiered", "shlomo", tweet_events, {"shlomo_min_score": 5.0, "bypass_market_filters": True, "sizing_mode": "shlomo_tiered", "max_hold_days": 20}),

        # Shlomo 8-Metrics + Variant K's 2 Priced-In Filters (Rule 2 Gap > +3% + Tape Confirmation; NO ATR, NO SPY)
        ("Shlomo-3.0-PI (+ K Priced-In)", "shlomo_pi", tweet_events, {"shlomo_min_score": 3.0, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 5}),
        ("Shlomo-5.25-PI (+ K Priced-In)", "shlomo_pi", tweet_events, {"shlomo_min_score": 5.25, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 5}),
        ("Shlomo-5.50-PI (+ K Priced-In)", "shlomo_pi", tweet_events, {"shlomo_min_score": 5.50, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 5}),
        ("Shlomo-Sniper-PI (+ K Priced-In)", "shlomo_pi", tweet_events, {"shlomo_min_score": 5.50, "min_entry_quality": 4.5, "min_conflict_check": 5.0, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 5}),
        ("Shlomo-Tiered-PI (+ K Priced-In)", "shlomo_pi", tweet_events, {"shlomo_min_score": 5.0, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "shlomo_tiered", "max_hold_days": 20}),

        # Market-Only vs Tweets-Only Ablations (6)
        ("Variant R-MKT", "ablation", mkt_events, {"min_atr_pct": 3.2, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 20}),
        ("Variant Q-MKT", "ablation", mkt_events, {"min_atr_pct": 3.2, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 30000, "profit_target_pct": 0.20, "day5_dead_money_cut": True, "max_hold_days": 20}),
        ("Variant K-MKT", "ablation", mkt_events, {"min_atr_pct": 0.0, "sizing_mode": "regime_fixed_cash", "cash_per_trade": 5000, "max_hold_days": 20}),
        ("Variant R-TW", "ablation", tweet_events, {"bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 20}),
        ("Variant Q-TW", "ablation", tweet_events, {"bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 30000, "profit_target_pct": 0.20, "day5_dead_money_cut": True, "max_hold_days": 20}),
        ("Variant K-TW", "ablation", tweet_events, {"bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "max_hold_days": 20}),

        # NEW USER-REQUESTED QUESTION 2: Tweets + Priced-In Filters ONLY (Gap >3% + Tape Confirm, NO ATR, NO SPY!)
        ("Variant R-TW-PI (Tweets + Priced-In)", "priced_in", tweet_events, {"direct_only": True, "min_tier": 4, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 20}),
        ("Variant Q-TW-PI (Tweets + Priced-In)", "priced_in", tweet_events, {"direct_only": True, "min_tier": 4, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 30000, "profit_target_pct": 0.20, "day5_dead_money_cut": True, "max_hold_days": 20}),
        ("Variant K-TW-PI (Tweets + Priced-In)", "priced_in", tweet_events, {"direct_only": True, "min_tier": 2, "skip_long_gap_gt_3": True, "tape_confirm": True, "bypass_market_filters": True, "sizing_mode": "tier_map", "max_hold_days": 20}),
        # Isolated SPY Vibe ablation on R (R without SPY ban)
        ("Variant R-NoSPY (R without S&P Vibe)", "spy_vibe", tweet_events, {"direct_only": True, "min_tier": 4, "min_atr_pct": 3.2, "skip_long_gap_gt_3": True, "tape_confirm": True, "spy_regime_gate": False, "ban_bear_longs": False, "sizing_mode": "fixed_cash", "cash_per_trade": 5000, "cash_cap": 25000, "leverage": 2.0, "profit_target_pct": 0.20, "max_hold_days": 20}),
    ]

    results = []
    variant_trades = {}
    used_tids = set()
    for name, grp, evs, cfg in VARIANT_SPECS:
        r = simulate(evs, cfg)
        tlog = r.pop("trade_log")
        results.append({"name": name, "group": grp, **r})
        variant_trades[name] = {
            "group": grp, **r, "trade_log": tlog,
        }
        for tr in tlog:
            if tr.get("tid"):
                used_tids.add(tr["tid"])

    # NEW USER-REQUESTED QUESTION 1: Pure S&P 500 Vibe Check (SPY vs 20-SMA, zero tweets)
    spy_vibe_results = {}
    for sname, smode in [
        ("SPY-Vibe-LongCash (SPY >= 20-SMA)", "long_cash"),
        ("SPY-Vibe-LongShort (SPY vs 20-SMA)", "long_short"),
        ("SPY Buy & Hold Benchmark", "buy_hold"),
    ]:
        sr = simulate_spy_vibe(spy_bars, smode, 25000.0)
        stlog = sr.pop("trade_log")
        spy_vibe_results[sname] = sr
        variant_trades[sname] = {"group": "spy_vibe", **sr, "trade_log": stlog}
        used_tids.add("SPY_VIBE")

    payload = {
        "window": f"{WIN_START} to {WIN_END}",
        "total_tweets_in_jsonl": total_rows,
        "original_tweets": orig_rows,
        "extracted_directional_signals": len(tweet_events),
        "market_only_breakdown_signals": len(mkt_events),
        "spy_vibe_benchmarks": spy_vibe_results,
        "variants": results,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n")

    trades_payload = {
        "window": f"{WIN_START} to {WIN_END}",
        "tweets": {tid: tweet_lookup[tid] for tid in sorted(used_tids) if tid in tweet_lookup},
        "variants": variant_trades,
    }
    TRADES_OUT_PATH.write_text(json.dumps(trades_payload, separators=(",", ":")))
    print(f"Wrote {TRADES_OUT_PATH} ({TRADES_OUT_PATH.stat().st_size / 1024:.1f} KB, {len(variant_trades)} variants, {len(trades_payload['tweets'])} unique tweets)")

    print(f"1-YEAR SUMMARY: {total_rows} tweets -> {orig_rows} original -> {len(tweet_events)} priced directional signals | {len(mkt_events)} market-only breakdowns")
    print("\n--- S&P 500 VIBE CHECK BENCHMARKS ($25k) ---")
    for k, v in spy_vibe_results.items():
        print(f"  {k:<60} ROC: {v['roc_pct']:>+7.2f}%  P&L: ${v['net_pnl']:>+9,.0f}  WR: {v['wr_pct']:>5.1f}%  DD: {v['max_dd_pct']:>6.2f}%  Trades: {v['trades']}")
    print("\n--- ALL VARIANTS (SORTED BY 1-YEAR ROC %) ---")
    print(f"{'Variant':<40} {'Grp':<10} {'Trd':>4} {'WR%':>6} {'Cap':>9} {'Net P&L':>11} {'ROC%':>9} {'PF':>6} {'DD%':>7}")
    for r in sorted(results, key=lambda x: x["roc_pct"], reverse=True):
        print(f"{r['name']:<40} {r['group']:<10} {r['trades']:>4} {r['wr_pct']:>5.1f}% ${r['capital_base']:>8,.0f} ${r['net_pnl']:>+10,.0f} {r['roc_pct']:>+8.2f}% {str(r['pf']):>6} {r['max_dd_pct']:>6.2f}%")


if __name__ == "__main__":
    main()
