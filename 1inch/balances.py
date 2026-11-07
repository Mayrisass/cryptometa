#!/usr/bin/env python3
"""Fetch Ethereum token balances for a wallet via the 1inch Balance API.

Usage: ONEINCH_API_KEY=... [CHAIN_ID=1] python3 balances.py [wallet_address]
The API key is read only from the ONEINCH_API_KEY environment variable.
"""
import json
import os
import sys
import urllib.error
import urllib.request

CHAIN_ID = int(os.environ.get("CHAIN_ID", "1"))  # default: Ethereum mainnet
DEFAULT_WALLET = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"  # vitalik.eth, public address


def main() -> int:
    api_key = os.environ.get("ONEINCH_API_KEY")
    if not api_key:
        print("Error: ONEINCH_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    wallet = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_WALLET
    url = f"https://api.1inch.com/balance/v1.2/{CHAIN_ID}/balances/{wallet}"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            balances = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1

    nonzero = {token: bal for token, bal in balances.items() if bal != "0"}
    print(f"Wallet {wallet} on chain {CHAIN_ID}: {len(nonzero)} non-zero of {len(balances)} tokens")
    for token, bal in sorted(nonzero.items()):
        print(f"  {token}: {bal}")  # raw units (wei / smallest token unit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
