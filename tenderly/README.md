# Tenderly webhook script

`webhook.py` sends a JSON payload to a [Tenderly Web3 Action](https://docs.tenderly.co/web3-actions) that uses a webhook trigger. Python 3, standard library only.

It does the same thing as:

```sh
curl -X POST -H "Content-Type: application/json" \
  "$TENDERLY_WEBHOOK_URL" -d '{"exampleKey": "exampleValue"}'
```

## Configuration

| Variable | Required | Notes |
|---|---|---|
| `TENDERLY_WEBHOOK_URL` | yes | `https://api.tenderly.co/api/v1/actions/<action-id>/webhook`, from the action's trigger settings. Anyone with this URL can trigger the action, so it is not in the code. |
| `TENDERLY_ACCESS_KEY` | no | Sent as `X-Access-Key`, for webhook triggers set to require authentication. |

## Usage

```sh
export TENDERLY_WEBHOOK_URL=https://api.tenderly.co/api/v1/actions/<action-id>/webhook

python3 webhook.py                                   # sends {"exampleKey": "exampleValue"}
python3 webhook.py '{"event": "price-alert", "token": "WETH"}'
python3 webhook.py payload.json                      # payload from a file
python3 ../1inch/gas-price.py | jq -Rs '{gas: .}' | python3 webhook.py -   # payload from stdin
```

The script prints the HTTP status, the response body and the remaining Tenderly call quota. A `200 {}` means Tenderly accepted the payload and queued a run; whether the action itself succeeded shows up in the action's **Execution History** in the Tenderly dashboard. Inside the action, the payload is available as the webhook event's `payload`.
