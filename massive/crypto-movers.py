#!/usr/bin/env python3
"""Top 20 crypto gainers or losers of the day.

Usage: MASSIVE_API_KEY=... python3 crypto-movers.py [gainers|losers]
Endpoint: GET /v2/snapshot/locale/global/markets/crypto/{direction}
"""
import sys

from _massive import get


def main() -> int:
    direction = sys.argv[1] if len(sys.argv) > 1 else "gainers"
    if direction not in ("gainers", "losers"):
        sys.exit("Error: direction must be 'gainers' or 'losers'.")
    data = get(f"/v2/snapshot/locale/global/markets/crypto/{direction}")
    print(f"Top crypto {direction}")
    for s in data.get("tickers") or []:
        last = (s.get("lastTrade") or {}).get("p")
        print(f"  {s['ticker']:<14} {s.get('todaysChangePerc', 0):>8.2f}%  last {last}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
