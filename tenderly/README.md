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

## The action (`actions/webhook.js`)

The receiving side, built from Tenderly's webhook action template (`actionFn` and the export are unchanged). For each call it:

- fails the run if the payload is not a JSON object, so bad calls show as failed in Execution History;
- logs the payload;
- stores the latest payload with a timestamp under `webhook/last-payload` and a running count under `webhook/count` in the project's Web3 Actions storage.

Test it locally (no Tenderly account needed):

```sh
cd actions && node test-webhook.js
```

Deploy with the [Tenderly CLI](https://github.com/Tenderly/tenderly-cli): set your account and project slugs in `tenderly.yaml` (replace `ACCOUNT/PROJECT`), then run `tenderly login` and `tenderly actions deploy` from this folder. If you paste the code into the dashboard editor instead, use the contents of `actions/webhook.js`. To require auth on the webhook, set `authenticated: true` in `tenderly.yaml` and send the key with `TENDERLY_ACCESS_KEY`.
