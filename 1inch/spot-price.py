#!/usr/bin/env python3
"""Get token spot prices from the 1inch Spot Price API.

Usage: ONEINCH_API_KEY=... [CHAIN_ID=1] [CURRENCY=USD] python3 spot-price.py [token_address ...]
Defaults to a few major Ethereum tokens, priced in USD. Set CURRENCY= (empty) for prices in wei of
the chain's native coin. The API key is read only from the ONEINCH_API_KEY environment variable.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

CHAIN_ID = int(os.environ.get("CHAIN_ID", "1"))  # default: Ethereum mainnet
CURRENCY = os.environ.get("CURRENCY", "USD")
DEFAULT_TOKENS = {  # Ethereum mainnet
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "WETH",
    "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599": "WBTC",
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "USDC",
    "0xdac17f958d2ee523a2206206994597c13d831ec7": "USDT",
    "0x6b175474e89094c44da98b954eedeac495271d0f": "DAI",
    "0x111111111117dc0aa78b770fa6a738034120c302": "1INCH",
}


def main() -> int:
    api_key = os.environ.get("ONEINCH_API_KEY")
    if not api_key:
        print("Error: ONEINCH_API_KEY is not set in the environment.", file=sys.stderr)
        return 1

    tokens = [a.lower() for a in sys.argv[1:]] or list(DEFAULT_TOKENS)
    url = f"https://api.1inch.com/price/v1.1/{CHAIN_ID}/{','.join(tokens)}"
    if CURRENCY:
        url += "?" + urllib.parse.urlencode({"currency": CURRENCY})
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            prices = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1

    unit = CURRENCY or "wei"
    print(f"Chain {CHAIN_ID} spot prices ({unit})")
    for addr in tokens:
        label = DEFAULT_TOKENS.get(addr, addr) if CHAIN_ID == 1 else addr
        print(f"  {label:<8} {prices.get(addr, prices.get(addr.lower(), 'n/a'))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
