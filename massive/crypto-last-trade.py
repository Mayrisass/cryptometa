#!/usr/bin/env python3
"""Last trade for a crypto pair.

Usage: MASSIVE_API_KEY=... python3 crypto-last-trade.py [FROM] [TO]
Defaults to BTC USD. Endpoint: GET /v1/last/crypto/{from}/{to}
"""
import datetime as dt
import sys

from _massive import get


def main() -> int:
    base = (sys.argv[1] if len(sys.argv) > 1 else "BTC").upper()
    quote = (sys.argv[2] if len(sys.argv) > 2 else "USD").upper()
    data = get(f"/v1/last/crypto/{base}/{quote}")
    last = data.get("last") or {}
    if not last:
        print(f"No last trade for {base}-{quote}.")
        return 1
    t = dt.datetime.fromtimestamp(last["timestamp"] / 1000, dt.timezone.utc)
    print(f"{data.get('symbol', base + '-' + quote)}: {last['price']} "
          f"(size {last['size']}, exchange {last['exchange']}, {t:%Y-%m-%d %H:%M:%S} UTC)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
