"""Shlomo's 8-Metric Ticket-Quality Rubric (0.0-10.0 equal-weight composite)."""
from datetime import datetime


def score_entry_quality(bars, idx: int, side: str) -> float:
    """Objective entry_quality score (1.5-7.0) based on pre-entry overnight gap in trade direction."""
    if idx < 1:
        return 5.0
    prev_c = bars[idx - 1]["close"]
    o = bars[idx]["open"]
    gap_pct = (o - prev_c) / prev_c * 100.0
    spent = gap_pct if side == "long" else -gap_pct
    if spent >= 6.0:
        return 1.5
    if spent >= 3.0:
        return 3.0
    if spent >= 1.5:
        return 4.5
    if spent >= 0.0:
        return 6.0
    return 7.0


def score_conflict_check(all_tweets: list[dict], cur_idx: int) -> float:
    """Objective conflict_check score (2.0-6.5) penalizing same-day or +-3d opposite-side tweets."""
    t0 = all_tweets[cur_idx]
    dt0 = datetime.strptime(t0["date"], "%Y-%m-%d")
    same_ticker_opp = False
    same_day_opp = False
    for j, tj in enumerate(all_tweets):
        if j == cur_idx:
            continue
        dtj = datetime.strptime(tj["date"], "%Y-%m-%d")
        diff = abs((dtj - dt0).days)
        if diff <= 3 and tj["ticker"] == t0["ticker"] and tj["side"] != t0["side"]:
            same_ticker_opp = True
        if diff == 0 and tj["side"] != t0["side"]:
            same_day_opp = True
    if same_ticker_opp:
        return 2.0
    if same_day_opp:
        return 4.0
    return 6.5


def compute_composite(tweet: dict, bars, idx: int, all_tweets: list[dict], cur_idx: int) -> dict:
    """Return all 8 rubric metric scores plus the equal-weight composite (0.0-10.0)."""
    r = tweet["rubric"]
    c7 = score_entry_quality(bars, idx, tweet["side"])
    c8 = score_conflict_check(all_tweets, cur_idx)
    scores = {
        "directional_clarity": float(r["directional_clarity"]),
        "instrument_specificity": float(r["instrument_specificity"]),
        "level_and_trigger": float(r["level_and_trigger"]),
        "evidence": float(r["evidence"]),
        "horizon": float(r["horizon"]),
        "invalidation": float(r["invalidation"]),
        "entry_quality": c7,
        "conflict_check": c8,
    }
    composite = round(sum(scores.values()) / 8.0, 3)
    return {"composite": composite, "scores": scores}
