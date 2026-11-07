# 1inch API scripts

Small, read-only scripts for the [1inch Business API](https://business.1inch.com). None of them sign or send transactions.

| Script | What it does | Endpoint |
|---|---|---|
| `balances.py` | Token balances for a wallet | `GET /balance/v1.2/{chainId}/balances/{wallet}` |
| `quote.py` | Classic swap quote (default 1 ETH → USDC) | `GET /swap/v6.1/{chainId}/quote` |
| `crosschain-quote.js` | Fusion+ cross-chain quote (0.1 WETH Ethereum → USDC.e Polygon) | `GET /fusion-plus/quoter/v1.2/quote/receive` |
| `portfolio-status.js` | Portfolio API service status (`is_available`) | `GET /portfolio/portfolio/v5.0/general/status` |
| `block-number.py` | Latest block via the Web3 RPC (`eth_blockNumber`) | `POST /web3/{chainId}` |
| `gas-price.py` | Current gas prices: base fee plus low/medium/high/instant tiers, in gwei | `GET /gas-price/v1.6/{chainId}` |
| `spot-price.py` | Token spot prices in USD (default: WETH, WBTC, USDC, USDT, DAI, 1INCH) | `GET /price/v1.1/{chainId}/{addresses}` |

## API key

Every script reads the key from the `ONEINCH_API_KEY` environment variable. The key is never in the code, and the scripts stop before sending anything if it is missing.

```sh
export ONEINCH_API_KEY=...   # your 1inch Business API key
```

In a Claude Code cloud session where the key is saved as a network secret for `api.1inch.com`, the proxy injects it into requests. Set the variable to a placeholder there: `ONEINCH_API_KEY=proxy-injected`.

## Usage

```sh
# Balances (Python 3, standard library only). CHAIN_ID defaults to 1 (Ethereum).
python3 balances.py 0xYourWallet
CHAIN_ID=8453 python3 balances.py 0xYourWallet      # Base

# Classic swap quote: [src] [dst] [amount in the token's smallest unit]
python3 quote.py                                    # 1 ETH -> USDC
python3 quote.py 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 0xdAC17F958D2ee523a2206206994597C13D831ec7 100000000

# Latest block number via the Web3 RPC (JSON-RPC eth_blockNumber)
python3 block-number.py
CHAIN_ID=137 python3 block-number.py                # Polygon

# Gas prices in gwei
python3 gas-price.py

# Spot prices in USD; pass token addresses, or set CURRENCY= for wei of the native coin
python3 spot-price.py
python3 spot-price.py 0xTokenA 0xTokenB

# Cross-chain quote (Node + axios)
npm install
node crosschain-quote.js 0xYourWallet               # wallet is optional
node portfolio-status.js                            # Portfolio API health check
```

Balance and quote amounts from the API are raw on-chain units; divide by `10^decimals` for the token. The free Dev plan allows 1 request per second.
