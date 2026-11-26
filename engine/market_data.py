"""Zero-dependency Yahoo Finance OHLC loader with local JSON caching, SPY 20-SMA, and 14d ATR."""
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.request

CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache_ohlc"

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

CRYPTO_EXEMPT_TICKERS = {"IBIT", "FBTC", "BITO", "ETHA", "ETHE", "GBTC", "BTC-USD", "ETH-USD"}
PROXY_OR_NOISE_TICKERS = {"QQQ", "SPY", "TLT", "HYG", "USO", "EWZ", "CIBR", "GDX", "ITB", "WEAT"}


def fetch_daily_bars(symbol: str, start: str = "2026-08-01", end: str = "2026-11-26", use_cache: bool = True):
    """Fetch daily OHLCV bars from Yahoo Finance chart API (cached locally in .cache_ohlc/)."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{symbol}_{start}_{end}.json"
    if use_cache and cache_path.exists():
        return json.loads(cache_path.read_text())

    p1 = int(datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
    p2 = int(datetime.strptime(end, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp()) + 86399
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={p1}&period2={p2}&interval=1d&includeAdjustedClose=true"
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
        bars.append({"date": dt, "open": float(o), "high": float(h), "low": float(l), "close": float(c), "volume": float(v or 0)})
    if use_cache and bars:
        cache_path.write_text(json.dumps(bars))
    return bars


def compute_spy_regime(spy_bars):
    """Return {date: 'bull' | 'bear'} based on SPY close vs. its 20-day simple moving average."""
    regime = {}
    closes = [b["close"] for b in spy_bars]
    for i, b in enumerate(spy_bars):
        if i >= 19:
            sma20 = sum(closes[i - 19 : i + 1]) / 20.0
            regime[b["date"]] = "bull" if b["close"] >= sma20 else "bear"
    return regime


def compute_atr14_pct(bars, idx: int):
    """Compute 14-day ATR as a percentage of prior close."""
    if idx < 14:
        return None
    trs = []
    for j in range(idx - 13, idx + 1):
        h, l, pc = bars[j]["high"], bars[j]["low"], bars[j - 1]["close"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    return round((sum(trs) / 14.0) / bars[idx - 1]["close"] * 100.0, 2)
