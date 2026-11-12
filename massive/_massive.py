"""Shared helper for the Massive API scripts: authenticated GET with JSON decoding.

The API key is read only from the MASSIVE_API_KEY environment variable and sent as
`Authorization: Bearer <key>` (the API also accepts an `apiKey` query parameter, which
these scripts avoid so the key never lands in URLs or logs).
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("MASSIVE_BASE_URL", "https://api.massive.com")


def get(path, params=None):
    """GET BASE_URL+path and return the decoded JSON body. Exits with status 1 on error."""
    api_key = os.environ.get("MASSIVE_API_KEY")
    if not api_key:
        sys.exit("Error: MASSIVE_API_KEY is not set in the environment.")
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            body = json.loads(body).get("error") or json.loads(body).get("message") or body
        except (ValueError, AttributeError):
            pass
        sys.exit(f"HTTP {e.code}: {str(body)[:500]}")
    except urllib.error.URLError as e:
        sys.exit(f"Request failed: {e.reason}")


def crypto_ticker(arg):
    """Accept BTCUSD, btc-usd, BTC/USD or X:BTCUSD and return X:BTCUSD."""
    t = arg.upper().replace("-", "").replace("/", "")
    return t if t.startswith("X:") else "X:" + t
