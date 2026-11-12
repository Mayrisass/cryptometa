# Massive API endpoint reference

All endpoints are `GET` on `https://api.massive.com` (staging: `https://api.staging.massive.com`). This list is taken from the Massive OpenAPI 3.0.3 spec, version 1.0.0. For an endpoint's parameters and response fields, see [massive.com/docs](https://massive.com/docs).

Path parameters are in `{braces}`. "Filters" means the endpoint takes the field-name filters described in the [README](./README.md#conventions-across-the-api).

## Crypto

| Endpoint | Description |
|---|---|
| `/v2/aggs/ticker/{cryptoTicker}/range/{multiplier}/{timespan}/{from}/{to}` | OHLCV bars in custom window sizes (`second` … `year`). `adjusted`, `sort`, `limit` (max 50000) |
| `/v2/aggs/ticker/{cryptoTicker}/prev` | Previous day's OHLC |
| `/v2/aggs/grouped/locale/global/market/crypto/{date}` | Daily OHLC for every crypto pair on a date |
| `/v1/open-close/crypto/{from}/{to}/{date}` | Open and close for a day, with the opening and closing trades |
| `/v3/trades/{cryptoTicker}` | Trades in a time range (ns timestamps). `timestamp` filters, `order`, `limit` (max 50000) |
| `/v1/last/crypto/{from}/{to}` | Last trade for a pair |
| `/v2/snapshot/locale/global/markets/crypto/tickers` | Snapshot of all pairs, or the ones in `tickers` |
| `/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}` | Snapshot of one pair |
| `/v2/snapshot/locale/global/markets/crypto/{direction}` | Top 20 `gainers` or `losers` |
| `/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}/book` | Level 2 book across exchanges. **Deprecated** |
| `/v1/indicators/{sma,ema,macd,rsi}/{cryptoTicker}` | Technical indicators: `timespan`, `window` (MACD: `short_window`, `long_window`, `signal_window`), `series_type`, `expand_underlying` |
| `/crypto/v1/exchanges` | Crypto exchanges (Coinbase, Binance, Bitfinex, …) |
| `/v1/historic/crypto/{from}/{to}/{date}` | Historic trade ticks. **Deprecated**: use `/v3/trades/{cryptoTicker}` |

## Stocks

| Endpoint | Description |
|---|---|
| `/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}` | OHLCV bars in custom window sizes |
| `/v2/aggs/ticker/{stocksTicker}/prev` | Previous day's OHLC |
| `/v2/aggs/grouped/locale/us/market/stocks/{date}` | Daily OHLC for the whole US market. `include_otc` |
| `/v1/open-close/{stocksTicker}/{date}` | Open, close, pre-market and after-hours prices for a day |
| `/v3/trades/{stockTicker}` | Trades in a time range |
| `/v3/quotes/{stockTicker}` | NBBO quotes in a time range |
| `/v2/last/trade/{stocksTicker}` | Last trade |
| `/v2/last/nbbo/{stocksTicker}` | Last NBBO quote |
| `/v2/snapshot/locale/us/markets/stocks/tickers` | Snapshot of all tickers, or the ones in `tickers`. `include_otc` |
| `/v2/snapshot/locale/us/markets/stocks/tickers/{stocksTicker}` | Snapshot of one ticker |
| `/v2/snapshot/locale/us/markets/stocks/{direction}` | Top 20 `gainers` or `losers` (volume ≥ 10,000) |
| `/v1/indicators/{sma,ema,macd,rsi}/{stockTicker}` | Technical indicators |
| `/stocks/dev/trades/{ticker}` | Trades, newer schema with `sip_timestamp` filters |
| `/stocks/v1/exchanges` | US stock exchanges, TRFs, SIPs and the ORF |
| `/stocks/v1/dividends` | Dividends with split-adjusted amounts and adjustment factors. Filters |
| `/stocks/v1/splits` | Splits and reverse splits with adjustment factors. Filters |
| `/stocks/v1/short-interest` | FINRA short interest by settlement date. Filters |
| `/stocks/v1/short-volume` | Daily short volume by venue. Filters |
| `/stocks/vX/float` | Free float shares and percentage. Filters |
| `/v2/ticks/stocks/trades/{ticker}/{date}` | **Deprecated**: use `/v3/trades/{stockTicker}` |
| `/v2/ticks/stocks/nbbo/{ticker}/{date}` | **Deprecated**: use `/v3/quotes/{stockTicker}` |

### Fundamentals

| Endpoint | Description |
|---|---|
| `/stocks/financials/v1/income-statements` | Quarterly, annual and trailing-twelve-month income statements. Filters by `cik`, `tickers`, `period_end`, `filing_date`, `fiscal_year`, `fiscal_quarter`, `timeframe` |
| `/stocks/financials/v1/balance-sheets` | Quarterly and annual balance sheets. Same filters |
| `/stocks/financials/v1/cash-flow-statements` | Quarterly, annual and TTM cash flow statements. Same filters |
| `/stocks/financials/v1/ratios` | Daily valuation, profitability, liquidity and leverage ratios (P/E, EV/EBITDA, ROE, …). Filters on every ratio |

### SEC filings and insiders

| Endpoint | Description |
|---|---|
| `/stocks/filings/vX/index` | EDGAR master index: form type, filing date and URL for every filing |
| `/stocks/filings/10-K/vX/sections` | Raw text of 10-K sections (`business`, `risk_factors`). Also at `/stocks/filings/10-K/vX_0/sections` |
| `/stocks/filings/vX/risk-factors` | Risk factors from 10-Ks, classified into three category levels |
| `/stocks/taxonomies/vX/risk-factors` | The risk factor classification list |
| `/stocks/filings/8-K/vX/text` | Parsed text of 8-K current reports |
| `/stocks/filings/8-K/vX/disclosures` | 8-K disclosures, classified into three category levels with a supporting excerpt |
| `/stocks/taxonomies/vX/disclosures` | The 8-K disclosure classification list |
| `/stocks/filings/vX/13-F` | Form 13F institutional holdings |
| `/stocks/filings/vX/form-3` | Form 3 initial insider ownership |
| `/stocks/filings/vX/form-4` | Form 4 insider transactions. `transaction_code` filter |
| `/stocks/filings/vX/form-5` | Form 5 annual insider statements |
| `/stocks/insiders/vX/activity` | Daily open-market insider buying and selling per issuer, cleaned of filer errors |
| `/stocks/insiders/vX/holdings` | Each insider's holdings per issuer, from Forms 3, 4 and 5 |
| `/v1/reference/sec/filings`, `/v1/reference/sec/filings/{filing_id}`, `.../files`, `.../files/{file_id}` | 10-K and 10-Q filings and their files. **Draft** |

## Options

| Endpoint | Description |
|---|---|
| `/v2/aggs/ticker/{optionsTicker}/range/{multiplier}/{timespan}/{from}/{to}` | OHLCV bars |
| `/v2/aggs/ticker/{optionsTicker}/prev` | Previous day's OHLC |
| `/v1/open-close/{optionsTicker}/{date}` | Open, close, pre-market and after-hours prices for a day |
| `/v3/trades/{optionsTicker}` | Trades in a time range |
| `/v3/quotes/{optionsTicker}` | Quotes in a time range |
| `/options/v3/trades/{ticker}`, `/options/v3/quotes/{ticker}` | Trades and NBBO quotes, newer schema |
| `/v2/last/trade/{optionsTicker}` | Last trade |
| `/v3/snapshot/options/{underlyingAsset}` | Snapshot of an underlying's option chain, with greeks and implied volatility. Filters by `strike_price`, `expiration_date`, `contract_type` |
| `/v3/snapshot/options/{underlyingAsset}/{optionContract}` | Snapshot of one contract |
| `/v3/reference/options/contracts` | Active and expired contracts. `underlying_ticker`, `contract_type`, `expiration_date`, `strike_price`, `as_of`, `expired` |
| `/v3/reference/options/contracts/{options_ticker}` | One contract |
| `/options/v1/open-interest` | Daily open interest per contract (OPRA) |
| `/options/vX/open-interest/underlying` | Daily open interest per underlying, calls and puts, with day-over-day change |
| `/options/v1/unusual-trades` | Trades with premium ≥ $100,000, size ≥ 1,000 contracts, or intermarket sweeps |
| `/options/v1/exchanges` | US options exchanges |
| `/v1/indicators/{sma,ema,macd,rsi}/{optionsTicker}` | Technical indicators |

## Forex

| Endpoint | Description |
|---|---|
| `/v2/aggs/ticker/{forexTicker}/range/{multiplier}/{timespan}/{from}/{to}` | OHLCV bars |
| `/v2/aggs/ticker/{forexTicker}/prev` | Previous day's OHLC |
| `/v2/aggs/grouped/locale/global/market/fx/{date}` | Daily OHLC for every pair on a date |
| `/v3/quotes/{fxTicker}` | BBO quotes in a time range |
| `/v1/last_quote/currencies/{from}/{to}` | Last quote for a pair |
| `/v1/conversion/{from}/{to}` | Convert an `amount` at the latest rate. `precision` 0–4 |
| `/v2/snapshot/locale/global/markets/forex/tickers` | Snapshot of all pairs, or the ones in `tickers` |
| `/v2/snapshot/locale/global/markets/forex/tickers/{ticker}` | Snapshot of one pair |
| `/v2/snapshot/locale/global/markets/forex/{direction}` | Top 20 `gainers` or `losers` |
| `/v1/indicators/{sma,ema,macd,rsi}/{fxTicker}` | Technical indicators |
| `/forex/v1/exchanges` | Forex venues |
| `/v1/historic/forex/{from}/{to}/{date}` | **Deprecated**: use `/v3/quotes/{fxTicker}` |

## Indices

| Endpoint | Description |
|---|---|
| `/v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}` | OHLC bars |
| `/v2/aggs/ticker/{indicesTicker}/prev` | Previous day's OHLC |
| `/v1/open-close/{indicesTicker}/{date}` | Open, close, pre-market and after-hours values for a day |
| `/v3/snapshot/indices` | Snapshot of indices. `ticker.any_of` (up to 250) |
| `/v1/indicators/{sma,ema,macd,rsi}/{indicesTicker}` | Technical indicators |

## Futures

| Endpoint | Description |
|---|---|
| `/futures/v1/aggs/{ticker}` | Bars by `resolution` (e.g. `1min`, `1session`). Filter on `window_start` (session bars start the day before `session_end_date`) |
| `/futures/v1/trades/{ticker}` | Tick-level trades |
| `/futures/v1/quotes/{ticker}` | Best bid and offer |
| `/futures/v1/snapshot` | Latest minute bar, quote, trade and session data. Filters by `product_code`, `ticker` |
| `/futures/v1/contracts` | Contracts with point-in-time specifications. Filters |
| `/futures/v1/products` | Products by sector, asset class, settlement and venue. Filters |
| `/futures/v1/schedules` | Session open, close and break times, in UTC |
| `/futures/v1/market-status` | Current status per product |
| `/futures/v1/exchanges` | Futures exchanges (CME, CBOT, NYMEX, COMEX, …) |

## All asset classes and reference data

| Endpoint | Description |
|---|---|
| `/v3/snapshot` | Universal snapshot for any mix of asset types. `ticker.any_of` (up to 250), `type` |
| `/v3/reference/tickers` | All tickers. `type`, `market`, `exchange`, `cik`, `cusip`, `date`, `search`, `active` |
| `/v3/reference/tickers/{ticker}` | Ticker details: company, address, branding, market cap, shares outstanding. `date` for point in time |
| `/v3/reference/tickers/types` | Ticker type codes |
| `/vX/reference/tickers/{id}/events` | Ticker change history. **Experimental** |
| `/v1/related-companies/{ticker}` | Related tickers, from news and returns |
| `/v2/reference/news` | News articles with per-ticker sentiment |
| `/v3/reference/dividends` | Cash dividends (older schema; see `/stocks/v1/dividends`) |
| `/v3/reference/splits` | Splits (older schema; see `/stocks/v1/splits`) |
| `/v3/reference/conditions` | Trade and quote condition codes, with their aggregation rules |
| `/v3/reference/exchanges` | Exchanges by `asset_class` and `locale` |
| `/v1/reference/ipos`, `/vX/reference/ipos` | IPOs and direct listings |
| `/v1/marketstatus/now` | Current trading status of exchanges and markets |
| `/v1/marketstatus/upcoming` | Upcoming market holidays and early closes |

## Partner datasets

| Endpoint | Description |
|---|---|
| `/benzinga/v1/ratings` | Analyst rating and price target changes |
| `/benzinga/v1/analyst-insights` | Analyst commentary behind ratings |
| `/benzinga/v1/consensus-ratings/{ticker}` | Consensus rating and price target. `date` range to aggregate over |
| `/benzinga/v1/analysts`, `/benzinga/v1/firms` | Analysts with performance scores, and research firms |
| `/benzinga/v1/earnings` | Actual vs. estimated EPS and revenue, with surprise |
| `/benzinga/v1/guidance` | Company EPS and revenue guidance |
| `/benzinga/v1/bulls-bears-say` | Bull and bear case summaries |
| `/benzinga/v2/news` | Benzinga news articles |
| `/etf-global/v1/profiles` | ETF metadata, fees, and sector, industry and geographic exposure |
| `/etf-global/v1/constituents` | ETF holdings with weights |
| `/etf-global/v1/fund-flows` | Daily fund flows, NAV and shares outstanding |
| `/etf-global/v1/analytics` | ETF Global risk, reward and quantitative scores |
| `/etf-global/v1/taxonomies` | ETF classification and methodology |
| `/fed/v1/treasury-yields` | Treasury yields, 1 month to 30 years |
| `/fed/v1/inflation` | CPI and PCE |
| `/fed/v1/inflation-expectations` | Market breakevens and Cleveland Fed model expectations |
| `/fed/v1/labor-market` | Unemployment, participation, hourly earnings, job openings |
| `/fed/v1/funding-conditions` | Fed funds, SOFR, OBFR, TGCR, repo operations, commercial paper |
| `/consumer-spending/eu/v1/merchant-aggregates` | Daily European card and open-banking spend per merchant (Fable) |
| `/consumer-spending/eu/v1/merchant-hierarchy` | Merchant to parent company and ticker mapping (Fable) |
| `/tmx/v1/corporate-events` | Corporate events calendar: earnings dates, conferences, shareholder meetings |
