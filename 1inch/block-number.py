#!/usr/bin/env python3
"""Call eth_blockNumber through the 1inch Web3 RPC API.

Usage: ONEINCH_API_KEY=... [CHAIN_ID=1] python3 block-number.py
The API key is read only from the ONEINCH_API_KEY environment variable.
"""
import json
import os
import sys
import urllib.error
import urllib.request

CHAIN_ID = int(os.environ.get("CHAIN_ID", "1"))  # default: Ethereum mainnet


def main() -> int:
    api_key = os.environ.get("ONEINCH_API_KEY")
    if not api_key:
        print("Error: ONEINCH_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []}).encode()
    req = urllib.request.Request(
        f"https://api.1inch.com/web3/{CHAIN_ID}",
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            reply = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1

    if "error" in reply:
        print(f"RPC error: {reply['error']}", file=sys.stderr)
        return 1
    print(f"Chain {CHAIN_ID} latest block: {int(reply['result'], 16)} (hex {reply['result']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
