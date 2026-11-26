"""US equity market (NYSE/NASDAQ) holiday and early-close calendar."""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")


def _observed(d: date) -> date:
    """NYSE weekend observation rule: Saturday -> Friday, Sunday -> Monday."""
    if d.weekday() == 5:
        return d - timedelta(days=1)
    if d.weekday() == 6:
        return d + timedelta(days=1)
    return d


def _nth_weekday(year: int, month: int, weekday: int, n: int) -> date:
    """Return the nth (1-indexed) occurrence of weekday (0=Mon..6=Sun) in month."""
    first = date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    return first + timedelta(days=offset + (n - 1) * 7)


def _last_weekday(year: int, month: int, weekday: int) -> date:
    """Return the last occurrence of weekday (0=Mon..6=Sun) in month."""
    nxt = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    last = nxt - timedelta(days=1)
    offset = (last.weekday() - weekday) % 7
    return last - timedelta(days=offset)


def _easter_sunday(year: int) -> date:
    """Anonymous Gregorian algorithm for Easter Sunday."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def nyse_holidays(year: int) -> dict[date, str]:
    """Return mapping of NYSE full-day holiday dates -> holiday name for `year`."""
    holidays: dict[date, str] = {}
    # Check New Year's Day for year and year+1 (in case Jan 1 of year+1 is Saturday -> observed Dec 31)
    for y in (year, year + 1):
        nyd = _observed(date(y, 1, 1))
        if nyd.year == year:
            holidays[nyd] = "New Year's Day"

    holidays[_nth_weekday(year, 1, 0, 3)] = "Martin Luther King Jr. Day"
    holidays[_nth_weekday(year, 2, 0, 3)] = "Presidents' Day"
    holidays[_easter_sunday(year) - timedelta(days=2)] = "Good Friday"
    holidays[_last_weekday(year, 5, 0)] = "Memorial Day"
    if year >= 2022:
        holidays[_observed(date(year, 6, 19))] = "Juneteenth"
    holidays[_observed(date(year, 7, 4))] = "Independence Day"
    holidays[_nth_weekday(year, 9, 0, 1)] = "Labor Day"
    holidays[_nth_weekday(year, 11, 3, 4)] = "Thanksgiving Day"
    holidays[_observed(date(year, 12, 25))] = "Christmas Day"
    return holidays


def nyse_early_closes(year: int) -> dict[date, str]:
    """Return mapping of NYSE 1:00 p.m. ET early-close dates -> name for `year`."""
    early: dict[date, str] = {}
    thanksgiving = _nth_weekday(year, 11, 3, 4)
    early[thanksgiving + timedelta(days=1)] = "Day After Thanksgiving (1:00 PM ET Close)"
    jul3 = date(year, 7, 3)
    if jul3.weekday() < 5 and jul3 not in nyse_holidays(year):
        early[jul3] = "Day Before Independence Day (1:00 PM ET Close)"
    dec24 = date(year, 12, 24)
    if dec24.weekday() < 5 and dec24 not in nyse_holidays(year):
        early[dec24] = "Christmas Eve (1:00 PM ET Close)"
    return early


def market_closed_reason(dt_utc: datetime) -> str | None:
    """Return human-readable reason if NYSE/NASDAQ are closed all day, else None."""
    local = dt_utc.astimezone(ET)
    d = local.date()
    if d.weekday() >= 5:
        return "Weekend (US markets closed)"
    holiday = nyse_holidays(d.year).get(d)
    if holiday:
        return f"US Market Holiday ({holiday})"
    return None


def is_us_trading_day(dt_utc: datetime) -> bool:
    return market_closed_reason(dt_utc) is None


def is_in_trading_session(dt_utc: datetime, extended_hours: bool) -> bool:
    """True if dt_utc falls on a US trading day within regular or extended hours (respecting early closes)."""
    if not is_us_trading_day(dt_utc):
        return False
    local = dt_utc.astimezone(ET)
    minutes = local.hour * 60 + local.minute
    is_early = local.date() in nyse_early_closes(local.year)
    if extended_hours:
        close_min = 17 * 60 if is_early else 20 * 60
        return 4 * 60 <= minutes < close_min
    close_min = 13 * 60 if is_early else 16 * 60
    return 8 * 60 + 30 <= minutes < close_min
