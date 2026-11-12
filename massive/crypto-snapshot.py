#!/usr/bin/env python3
"""Current snapshot (last trade, day bar, change vs. previous day) for crypto pairs.

Usage: MASSIVE_API_KEY=... python3 crypto-snapshot.py [PAIR ...]
Pairs default to BTCUSD ETHUSD SOLUSD. Accepts BTCUSD, BTC-USD, BTC/USD or X:BTCUSD.
Endpoint: GET /v2/snapshot/locale/global/markets/crypto/tickers?tickers=...
"""
import sys

from _massive import crypto_ticker, get


def main() -> int:
    tickers = [crypto_ticker(a) for a in sys.argv[1:]] or ["X:BTCUSD", "X:ETHUSD", "X:SOLUSD"]
    data = get("/v2/snapshot/locale/global/markets/crypto/tickers", {"tickers": ",".join(tickers)})
    rows = {t.get("ticker"): t for t in data.get("tickers") or []}
    print(f"{'pair':<12} {'last':>14} {'day open':>14} {'change %':>9} {'day volume':>16}")
    for t in tickers:
        s = rows.get(t)
        if not s:
            print(f"{t:<12} {'no data':>14}")
            continue
        last = (s.get("lastTrade") or {}).get("p") or (s.get("min") or {}).get("c")
        day = s.get("day") or {}
        print(f"{t:<12} {last if last is not None else 'n/a':>14} {day.get('o', 'n/a'):>14} "
              f"{s.get('todaysChangePerc', 0):>9.2f} {day.get('v', 'n/a'):>16}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
