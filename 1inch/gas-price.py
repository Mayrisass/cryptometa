#!/usr/bin/env python3
"""Get current gas prices from the 1inch Gas Price API.

Usage: ONEINCH_API_KEY=... [CHAIN_ID=1] python3 gas-price.py
The API key is read only from the ONEINCH_API_KEY environment variable.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from decimal import Decimal

CHAIN_ID = int(os.environ.get("CHAIN_ID", "1"))  # default: Ethereum mainnet


def gwei(wei) -> str:
    return f"{(Decimal(str(wei)) / Decimal(10**9)).normalize():f} gwei"


def main() -> int:
    api_key = os.environ.get("ONEINCH_API_KEY")
    if not api_key:
        print("Error: ONEINCH_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    req = urllib.request.Request(
        f"https://api.1inch.com/gas-price/v1.6/{CHAIN_ID}",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            gas = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1

    print(f"Chain {CHAIN_ID} gas prices")
    if "baseFee" in gas:  # EIP-1559 chains
        print(f"  base fee: {gwei(gas['baseFee'])}")
        for tier in ("low", "medium", "high", "instant"):
            t = gas.get(tier)
            if t:
                print(f"  {tier:<8} max fee {gwei(t['maxFeePerGas']):>16}   tip {gwei(t['maxPriorityFeePerGas'])}")
    else:  # legacy gas-price chains
        for tier, price in gas.items():
            print(f"  {tier:<8} {gwei(price)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
