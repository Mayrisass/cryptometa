#!/usr/bin/env python3
"""OHLCV bars for a crypto pair over a date range.

Usage: MASSIVE_API_KEY=... python3 crypto-aggs.py [PAIR] [FROM] [TO] [TIMESPAN] [MULTIPLIER]
Defaults: X:BTCUSD, last 7 days, 1 day bars. FROM/TO are YYYY-MM-DD or millisecond timestamps.
TIMESPAN is one of second, minute, hour, day, week, month, quarter, year.
Endpoint: GET /v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}
"""
import datetime as dt
import sys

from _massive import crypto_ticker, get

TIMESPANS = {"second", "minute", "hour", "day", "week", "month", "quarter", "year"}


def main() -> int:
    args = sys.argv[1:]
    today = dt.datetime.now(dt.timezone.utc).date()
    ticker = crypto_ticker(args[0]) if len(args) > 0 else "X:BTCUSD"
    start = args[1] if len(args) > 1 else str(today - dt.timedelta(days=7))
    end = args[2] if len(args) > 2 else str(today)
    timespan = args[3] if len(args) > 3 else "day"
    multiplier = args[4] if len(args) > 4 else "1"
    if timespan not in TIMESPANS:
        sys.exit(f"Error: TIMESPAN must be one of {', '.join(sorted(TIMESPANS))}.")

    data = get(f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start}/{end}",
               {"adjusted": "true", "sort": "asc", "limit": 5000})
    bars = data.get("results") or []
    print(f"{ticker} {multiplier} {timespan} bars, {start} to {end}: {len(bars)}")
    print(f"{'start (UTC)':<17} {'open':>12} {'high':>12} {'low':>12} {'close':>12} {'volume':>14}")
    for b in bars:
        t = dt.datetime.fromtimestamp(b["t"] / 1000, dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
        print(f"{t:<17} {b['o']:>12} {b['h']:>12} {b['l']:>12} {b['c']:>12} {b['v']:>14.4f}")
    if data.get("next_url"):
        print("(more bars available: narrow the range or raise MULTIPLIER)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
