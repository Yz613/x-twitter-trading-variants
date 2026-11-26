"""Unified deterministic backtest simulator for all 32 X/Twitter & Market-Ablation variants."""
from datetime import datetime
import json
from pathlib import Path

from .market_data import (
    CRYPTO_EXEMPT_TICKERS,
    MARKET_ONLY_UNIVERSE,
    PROXY_OR_NOISE_TICKERS,
    compute_atr14_pct,
    compute_spy_regime,
    fetch_daily_bars,
)
from .shlomo_rubric import compute_composite

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SLIPPAGE_PER_LEG = 0.0010
SHORT_BORROW_APR = 0.03
MARGIN_INTEREST_APR = 0.065


def load_tweets() -> list[dict]:
    return json.loads((DATA_DIR / "kobeissi_tweets_oct_nov_2026.json").read_text())


def _eval_exit(bars, entry_idx: int, side: str, config: dict, entry_field: str = "open"):
    entry = bars[entry_idx][entry_field]
    win_end = config.get("window_end", "2026-11-25")
    end_idx = len(bars) - 1
    while end_idx > entry_idx and bars[end_idx]["date"] > win_end:
        end_idx -= 1

    max_hold = config.get("max_hold_days")
    limit_idx = min(entry_idx + max_hold, end_idx) if max_hold else end_idx
    exit_idx = limit_idx
    exit_price = bars[limit_idx]["close"]
    reason = f"{max_hold}d max" if max_hold and limit_idx < end_idx else f"{win_end} close"

    target = config.get("profit_target_pct")
    cat_stop = config.get("catastrophe_stop_pct")
    intraday_stop = config.get("intraday_stop_pct")
    trailing_stop = config.get("trailing_stop_pct")
    day5_cut = config.get("day5_dead_money_cut", False)

    peak_ret = 0.0
    for k in range(entry_idx + 1, limit_idx + 1):
        bar = bars[k]
        c = bar["close"]
        ret = (entry - c) / entry if side == "short" else (c - entry) / entry
        # Check intraday stop if configured
        if intraday_stop is not None:
            worst_px = bar["high"] if side == "short" else bar["low"]
            worst_ret = (entry - worst_px) / entry if side == "short" else (worst_px - entry) / entry
            if worst_ret <= -intraday_stop:
                exit_idx = k
                exit_price = entry * (1 + intraday_stop) if side == "short" else entry * (1 - intraday_stop)
                reason = f"-{int(intraday_stop * 100)}% intraday stop"
                break
        if target is not None and ret >= target:
            exit_idx, exit_price, reason = k, c, f"+{int(target * 100)}% target"
            break
        if cat_stop is not None and ret <= -cat_stop:
            exit_idx, exit_price, reason = k, c, f"-{int(cat_stop * 100)}% close stop"
            break
        if trailing_stop is not None:
            peak_ret = max(peak_ret, ret)
            if peak_ret >= 0.10 and (peak_ret - ret) >= trailing_stop:
                exit_idx, exit_price, reason = k, c, f"{int(trailing_stop * 100)}% trailing stop"
                break
        if day5_cut and (k - entry_idx) == 5 and ret < 0.02:
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
        "entry_price": round(entry, 2),
        "exit_price": round(exit_price, 2),
        "cal_days": cal_days,
        "gross_ret": gross_ret,
        "exit_reason": reason,
    }


def run_variant_backtest(config: dict, capital_override: float | None = None, ohlc_cache: dict | None = None) -> dict:
    """Run any variant's exact rules on real Yahoo Finance daily OHLC data (Oct 9 - Nov 25, 2026)."""
    cache = ohlc_cache if ohlc_cache is not None else {}

    def get_bars(sym: str):
        if sym not in cache:
            try:
                cache[sym] = fetch_daily_bars(sym)
            except Exception:
                cache[sym] = []
        return cache[sym]

    spy_regime = compute_spy_regime(get_bars("SPY"))
    win_start = config.get("window_start", "2026-10-09")
    win_end = config.get("window_end", "2026-11-25")
    sig_source = config.get("signal_source", "tweet")

    candidates = []
    if sig_source == "market_only":
        for sym in MARKET_ONLY_UNIVERSE:
            bars = get_bars(sym)
            last_idx = -999
            for i in range(20, len(bars) - 1):
                d = bars[i]["date"]
                if d < win_start or d > "2026-11-20" or (i - last_idx) < 10:
                    continue
                prev_c, o, c = bars[i - 1]["close"], bars[i]["open"], bars[i]["close"]
                drop_pct = (c - prev_c) / prev_c * 100.0
                if not (-28.0 <= drop_pct <= -8.0) or c >= o:
                    continue
                avg_vol = sum(b["volume"] for b in bars[i - 20 : i]) / 20.0
                if avg_vol > 0 and bars[i]["volume"] < 2.0 * avg_vol:
                    continue
                atr = compute_atr14_pct(bars, i - 1)
                candidates.append({
                    "ticker": sym, "side": "short", "tier": 5, "date": d,
                    "bars": bars, "idx": i, "atr": atr, "gap_pct": (o - prev_c) / prev_c * 100.0,
                    "day_chg": drop_pct, "regime": spy_regime.get(d, "bear"),
                    "shlomo": {"composite": 6.0, "scores": {"entry_quality": 6.0, "conflict_check": 6.5}},
                    "entry_field": "close",
                })
                last_idx = i
    else:
        tweets = load_tweets()
        for t_idx, tw in enumerate(tweets):
            if tw["date"] < win_start or tw["date"] > win_end:
                continue
            bars = get_bars(tw["ticker"])
            idx = next((k for k, b in enumerate(bars) if b["date"] >= tw["date"]), None)
            if idx is None or idx >= len(bars) - 1:
                continue
            prev_c = bars[idx - 1]["close"] if idx > 0 else bars[idx]["open"]
            o, c = bars[idx]["open"], bars[idx]["close"]
            atr = compute_atr14_pct(bars, idx - 1)
            shlomo = compute_composite(tw, bars, idx, tweets, t_idx)
            candidates.append({
                "ticker": tw["ticker"], "side": tw["side"], "tier": tw["tier"], "date": bars[idx]["date"],
                "bars": bars, "idx": idx, "atr": atr,
                "gap_pct": (o - prev_c) / prev_c * 100.0,
                "day_chg": (c - prev_c) / prev_c * 100.0,
                "regime": spy_regime.get(bars[idx]["date"], "bear"),
                "shlomo": shlomo, "entry_field": "open",
            })

    candidates.sort(key=lambda e: (e["date"], e["ticker"]))

    # Portfolio simulation
    cash_cap = capital_override if capital_override is not None else config.get("cash_cap")
    leverage = float(config.get("leverage", 1.0))
    if cash_cap is not None and cash_cap < 2000.0 and leverage > 1.0:
        leverage = 1.0  # Reg-T $2,000 minimum equity rule

    allow_dups = config.get("allow_duplicates", False)
    deduct_fees = config.get("net_of_fees", True)
    open_pos = []
    taken = []
    peak_cash = 0.0
    equity = float(cash_cap or config.get("initial_cash", 100000.0))

    for ev in candidates:
        # Close expired positions
        still = []
        for op in open_pos:
            if op["exit_date"] <= ev["date"]:
                equity += op["net_pnl"]
            else:
                still.append(op)
        open_pos = still

        sym, side, tier = ev["ticker"], ev["side"], ev["tier"]
        if not allow_dups and any(op["ticker"] == sym for op in open_pos):
            continue

        # Entry filters
        if tier < config.get("min_tier", 1):
            continue
        if config.get("direct_only", False) and sym in PROXY_OR_NOISE_TICKERS and sym not in CRYPTO_EXEMPT_TICKERS:
            continue
        if config.get("shlomo_min_score") is not None and ev["shlomo"]["composite"] < config["shlomo_min_score"]:
            continue
        if config.get("min_entry_quality") is not None and ev["shlomo"]["scores"]["entry_quality"] < config["min_entry_quality"]:
            continue
        if config.get("min_conflict_check") is not None and ev["shlomo"]["scores"]["conflict_check"] < config["min_conflict_check"]:
            continue

        if not config.get("bypass_market_filters", False):
            min_atr = config.get("min_atr_pct", 0.0)
            if min_atr > 0 and not (config.get("crypto_exempt", True) and sym in CRYPTO_EXEMPT_TICKERS):
                if ev["atr"] is None or ev["atr"] < min_atr:
                    continue
            if config.get("skip_long_gap_gt_3", False) and side == "long" and ev["gap_pct"] > 3.0:
                continue
            if config.get("tape_confirm", False):
                if side == "short" and ev["day_chg"] > 1.0:
                    continue
                if side == "long" and ev["day_chg"] < -1.0:
                    continue
            if config.get("ban_bear_longs", False) and ev["regime"] == "bear" and side == "long":
                continue

        # Determine cash size
        mode = config.get("sizing_mode", "fixed_cash")
        if mode == "tier_map":
            tmap = {5: 10000.0, 4: 5000.0, 3: 2000.0, 2: 500.0, 1: 20.0}
            cash = tmap.get(tier, 5000.0)
            if config.get("spy_regime_gate", False):
                if ev["regime"] == "bear" and side == "long":
                    cash *= 0.25
                elif ev["regime"] == "bull" and side == "short" and tier <= 3:
                    cash *= 0.5
        elif mode == "regime_fixed_cash":
            base_c = float(config.get("cash_per_trade", 5000.0))
            cash = base_c if ev["regime"] == "bear" else base_c * 0.5
        elif mode == "shlomo_tiered":
            sc = ev["shlomo"]["composite"]
            cash = 10000.0 if sc >= 5.75 else (5000.0 if sc >= 5.25 else 2500.0)
        elif mode == "fractional_kelly":
            frac = config.get("kelly_fraction_t5", 0.16) if tier >= 5 else config.get("kelly_fraction_t4", 0.12)
            cash = round(equity * frac, 2)
        else:
            cash = float(config.get("cash_per_trade", 5000.0))

        cur_cash = sum(op["cash"] for op in open_pos)
        if cash_cap is not None and cur_cash + cash > cash_cap:
            continue

        notional = cash * leverage
        p = _eval_exit(ev["bars"], ev["idx"], side, config, entry_field=ev["entry_field"])
        gross_pnl = notional * p["gross_ret"]
        if deduct_fees:
            slip = notional * (SLIPPAGE_PER_LEG * 2.0)
            borrow = (notional * SHORT_BORROW_APR * (p["cal_days"] / 365.0)) if side == "short" else 0.0
            mint = max(0.0, notional - cash) * MARGIN_INTEREST_APR * (p["cal_days"] / 365.0)
            net_pnl = gross_pnl - slip - borrow - mint
        else:
            net_pnl = gross_pnl

        rec = {
            "ticker": sym, "side": side, "tier": tier,
            "entry_date": p["entry_date"], "exit_date": p["exit_date"],
            "cash": round(cash, 2), "notional": round(notional, 2),
            "net_pnl": round(net_pnl, 2), "exit_reason": p["exit_reason"],
        }
        open_pos.append(rec)
        taken.append(rec)
        peak_cash = max(peak_cash, sum(op["cash"] for op in open_pos))

    wins = [t for t in taken if t["net_pnl"] > 0]
    losses = [t for t in taken if t["net_pnl"] <= 0]
    gw = sum(t["net_pnl"] for t in wins)
    gl = abs(sum(t["net_pnl"] for t in losses))
    pf = round(gw / gl, 2) if gl > 0 else (float("inf") if gw > 0 else 0.0)
    total_net = round(sum(t["net_pnl"] for t in taken), 2)
    denom = float(cash_cap) if cash_cap is not None else peak_cash
    roc = round((total_net / denom) * 100.0, 2) if denom > 0 else 0.0

    return {
        "id": config["id"],
        "name": config["name"],
        "trades": len(taken),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate_pct": round(len(wins) / len(taken) * 100.0, 1) if taken else 0.0,
        "capital_base": round(denom, 2),
        "net_pnl": total_net,
        "roc_pct": roc,
        "profit_factor": "INF" if pf == float("inf") else pf,
        "positions": taken,
    }
