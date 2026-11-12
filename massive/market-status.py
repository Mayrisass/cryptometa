#!/usr/bin/env python3
"""Current market status (US exchanges, crypto, forex) and upcoming market holidays.

Usage: MASSIVE_API_KEY=... python3 market-status.py
Endpoints: GET /v1/marketstatus/now, GET /v1/marketstatus/upcoming
"""
import sys

from _massive import get


def main() -> int:
    now = get("/v1/marketstatus/now")
    print(f"Server time: {now.get('serverTime')}")
    print(f"Market: {now.get('market')}")
    for name, status in (now.get("exchanges") or {}).items():
        print(f"  {name:<8} {status}")
    for name, status in (now.get("currencies") or {}).items():
        print(f"  {name:<8} {status}")
    holidays = get("/v1/marketstatus/upcoming") or []
    print("Upcoming holidays:")
    for h in holidays[:10]:
        hours = f" {h['open']} - {h['close']}" if h.get("open") else ""
        print(f"  {h['date']} {h['exchange']:<7} {h['name']} ({h['status']}{hours})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
