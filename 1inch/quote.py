#!/usr/bin/env python3
"""Get a 1inch Classic Swap quote on Ethereum.

Usage: ONEINCH_API_KEY=... python3 quote.py [src_token] [dst_token] [amount_in_base_units]
Defaults: 1 ETH -> USDC. The API key is read only from the ONEINCH_API_KEY environment variable.
A quote is read-only: it signs nothing, sends no transaction and moves no funds.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal

CHAIN_ID = int(os.environ.get("CHAIN_ID", "1"))  # default: Ethereum mainnet
ETH = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"  # 1inch's placeholder for the native coin
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"


def main() -> int:
    api_key = os.environ.get("ONEINCH_API_KEY")
    if not api_key:
        print("Error: ONEINCH_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    src = sys.argv[1] if len(sys.argv) > 1 else ETH
    dst = sys.argv[2] if len(sys.argv) > 2 else USDC
    amount = sys.argv[3] if len(sys.argv) > 3 else str(10**18)  # 1 ETH in wei

    params = urllib.parse.urlencode(
        {"src": src, "dst": dst, "amount": amount, "includeTokensInfo": "true", "includeGas": "true"}
    )
    url = f"https://api.1inch.com/swap/v6.1/{CHAIN_ID}/quote?{params}"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            q = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1

    s, d = q.get("srcToken", {}), q.get("dstToken", {})
    src_amt = Decimal(amount) / (Decimal(10) ** s.get("decimals", 0))
    dst_amt = Decimal(q["dstAmount"]) / (Decimal(10) ** d.get("decimals", 0))
    print(f"Chain {CHAIN_ID} quote: {src_amt} {s.get('symbol', src)} -> {dst_amt} {d.get('symbol', dst)}")
    if src_amt:
        print(f"Rate: 1 {s.get('symbol')} = {dst_amt / src_amt:.6f} {d.get('symbol')}")
    print(f"Raw dstAmount: {q['dstAmount']}  Estimated gas: {q.get('gas', 'n/a')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
