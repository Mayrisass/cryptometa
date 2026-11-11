#!/usr/bin/env python3
"""Send a JSON payload to a Tenderly Web3 Action webhook trigger.

Usage:
  TENDERLY_WEBHOOK_URL=https://api.tenderly.co/api/v1/actions/<action-id>/webhook \
    python3 webhook.py '{"exampleKey": "exampleValue"}'
  python3 webhook.py payload.json        # read the payload from a file
  echo '{"a": 1}' | python3 webhook.py -  # read the payload from stdin
  python3 webhook.py                     # send {"exampleKey": "exampleValue"}

The webhook URL is read only from TENDERLY_WEBHOOK_URL: anyone with the URL can trigger
the action, so keep it out of the code. Set TENDERLY_ACCESS_KEY too if the action's webhook
trigger is configured to require authentication (sent as the X-Access-Key header).
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_PAYLOAD = {"exampleKey": "exampleValue"}
URL_PREFIX = "https://api.tenderly.co/api/v1/actions/"


def load_payload(arg):
    if arg is None:
        return DEFAULT_PAYLOAD
    if arg == "-":
        return json.load(sys.stdin)
    if os.path.isfile(arg):
        with open(arg, encoding="utf-8") as f:
            return json.load(f)
    return json.loads(arg)


def main() -> int:
    url = os.environ.get("TENDERLY_WEBHOOK_URL", "").strip()
    if not url:
        print("Error: TENDERLY_WEBHOOK_URL is not set in the environment.", file=sys.stderr)
        return 1
    if not (url.startswith(URL_PREFIX) and url.endswith("/webhook")):
        print(f"Error: TENDERLY_WEBHOOK_URL should look like {URL_PREFIX}<action-id>/webhook",
              file=sys.stderr)
        return 1

    try:
        payload = load_payload(sys.argv[1] if len(sys.argv) > 1 else None)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: payload is not valid JSON: {e}", file=sys.stderr)
        return 1

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    access_key = os.environ.get("TENDERLY_ACCESS_KEY")
    if access_key:
        headers["X-Access-Key"] = access_key

    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers,
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode(errors="replace")
            remaining = resp.headers.get("x-tdly-remaining")
            print(f"HTTP {resp.status} {body}")
            if remaining is not None:
                print(f"Tenderly calls remaining: {remaining}/{resp.headers.get('x-tdly-limit', '?')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode(errors='replace')[:500]}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        return 1

    # A 2xx only means Tenderly queued the run; check the action's Execution History for its result.
    return 0


if __name__ == "__main__":
    sys.exit(main())
