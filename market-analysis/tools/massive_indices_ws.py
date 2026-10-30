"""Stream per-minute index aggregates from Massive's WebSocket API.

Docs: https://massive.com/docs/websocket/indices/aggregates-per-minute.md

Usage:
    export MASSIVE_API_KEY=...            # never hardcode the key
    pip install websockets
    python massive_indices_ws.py                   # I:SPX, delayed feed
    python massive_indices_ws.py I:SPX I:NDX I:DJI
    python massive_indices_ws.py --realtime I:SPX  # needs Indices Advanced+

Plans: Starter = 15-minute delayed, Advanced/Business = real-time,
Basic = not included.
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import websockets

REALTIME_URL = "wss://socket.massive.com/indices"
DELAYED_URL = "wss://delayed.massive.com/indices"
ET = ZoneInfo("America/New_York")


def fmt_time(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, ET).strftime("%Y-%m-%d %H:%M ET")


def print_bar(bar: dict) -> None:
    change = bar["c"] - bar["op"]
    pct = change / bar["op"] * 100 if bar["op"] else 0.0
    print(
        f"{fmt_time(bar['s'])}  {bar['sym']:<8} "
        f"O {bar['o']:>10.2f}  H {bar['h']:>10.2f}  "
        f"L {bar['l']:>10.2f}  C {bar['c']:>10.2f}  "
        f"day {change:+.2f} ({pct:+.2f}%)",
        flush=True,
    )


async def stream(url: str, api_key: str, tickers: list[str]) -> None:
    channels = ",".join(f"AM.{t}" for t in tickers)
    async for ws in websockets.connect(url):  # reconnects automatically
        try:
            await ws.send(json.dumps({"action": "auth", "params": api_key}))
            async for raw in ws:
                for msg in json.loads(raw):
                    ev = msg.get("ev")
                    if ev == "status":
                        status = msg.get("status")
                        print(f"[status] {status}: {msg.get('message')}", file=sys.stderr)
                        if status == "auth_success":
                            await ws.send(json.dumps({"action": "subscribe", "params": channels}))
                        elif status == "auth_failed":
                            sys.exit("Authentication failed: check MASSIVE_API_KEY and your plan.")
                    elif ev == "AM":
                        print_bar(msg)
        except websockets.ConnectionClosed as exc:
            print(f"[conn] closed ({exc}); reconnecting...", file=sys.stderr)
            continue


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("tickers", nargs="*", default=["I:SPX"], help="index tickers, e.g. I:SPX (use * for all)")
    parser.add_argument("--realtime", action="store_true", help="use the real-time feed instead of delayed")
    args = parser.parse_args()

    api_key = os.environ.get("MASSIVE_API_KEY")
    if not api_key:
        sys.exit("Set MASSIVE_API_KEY first (https://massive.com/dashboard/keys).")

    url = REALTIME_URL if args.realtime else DELAYED_URL
    print(f"Connecting to {url} for {', '.join(args.tickers)} ...", file=sys.stderr)
    try:
        asyncio.run(stream(url, api_key, args.tickers))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
