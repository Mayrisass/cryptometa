# Massive API scripts and reference

Small, read-only scripts for the [Massive](https://massive.com) market data REST API (`https://api.massive.com`), plus a reference of its endpoints in [`ENDPOINTS.md`](./ENDPOINTS.md). Python 3, standard library only.

| Script | What it does | Endpoint |
|---|---|---|
| `crypto-snapshot.py` | Last trade, day open, change % and day volume for crypto pairs (default BTC, ETH, SOL vs USD) | `GET /v2/snapshot/locale/global/markets/crypto/tickers` |
| `crypto-aggs.py` | OHLCV bars for a pair over a date range (default: BTC/USD, last 7 days, daily) | `GET /v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}` |
| `crypto-last-trade.py` | Last trade for a pair (default BTC/USD) | `GET /v1/last/crypto/{from}/{to}` |
| `crypto-movers.py` | Top 20 crypto gainers or losers of the day | `GET /v2/snapshot/locale/global/markets/crypto/{direction}` |
| `market-status.py` | Current status of US exchanges, crypto and forex, and the upcoming market holidays | `GET /v1/marketstatus/now`, `GET /v1/marketstatus/upcoming` |

`_massive.py` is the shared request helper.

## API key

Every script reads the key from the `MASSIVE_API_KEY` environment variable and stops before sending anything if it is missing. The key is sent as an `Authorization: Bearer` header, not as the `apiKey` query parameter, so it does not end up in URLs or logs.

```sh
export MASSIVE_API_KEY=...   # your Massive API key
```

`MASSIVE_BASE_URL` overrides the host, for example `https://api.staging.massive.com`.

## Usage

```sh
# Crypto pairs can be written BTCUSD, BTC-USD, BTC/USD or X:BTCUSD
python3 crypto-snapshot.py
python3 crypto-snapshot.py btc-usd eth-btc

# Bars: [pair] [from] [to] [timespan] [multiplier]; dates are YYYY-MM-DD or ms timestamps
python3 crypto-aggs.py                                   # BTC/USD, daily, last 7 days
python3 crypto-aggs.py ETHUSD 2025-11-03 2025-11-04 hour 1

python3 crypto-last-trade.py                             # BTC USD
python3 crypto-last-trade.py ETH USD

python3 crypto-movers.py losers
python3 market-status.py
```

What a request returns depends on your Massive plan: snapshot and last-trade data can be real time or 15-minute delayed, and endpoints outside your plan return `403`.

## Conventions across the API

These apply to most endpoints; [`ENDPOINTS.md`](./ENDPOINTS.md) lists them all.

- **Tickers** carry an asset prefix: stocks are bare (`AAPL`), options `O:SPY251219C00650000`, crypto `X:BTCUSD`, forex `C:EURUSD`, indices `I:NDX`. Tickers are case-sensitive.
- **Filters.** Newer endpoints (`/stocks/...`, `/benzinga/...`, `/etf-global/...`, `/fed/...`, `/futures/...`) take a field as a query parameter for equality, and suffixes for the rest: `.gt`, `.gte`, `.lt`, `.lte`, and `.any_of` with a comma-separated list. Array fields such as `tickers` take `.all_of` and `.any_of`.
- **Sorting.** Newer endpoints use `sort=field.asc` or `field.desc`, comma-separated for several columns. Older `v2`/`v3` endpoints use `sort=field` with a separate `order=asc|desc`.
- **Pagination.** When more results exist, the response has a `next_url`. Request it as is, with your key, to get the next page.
- **Timestamps.** Aggregate bars use Unix milliseconds. Trades, quotes and futures data use Unix nanoseconds. Snapshot `updated` fields can be either, depending on the endpoint.
- **Responses** are JSON with `status` and `request_id`. Errors return `status: "ERROR"` and an `error` message. Many newer endpoints can also return an Apache Arrow IPC file (`Accept: application/vnd.apache.arrow.file`), and some older ones return CSV.
