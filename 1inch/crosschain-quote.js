// Fusion+ cross-chain quote: 0.1 WETH (Ethereum) -> USDC.e (Polygon).
// The API key is read only from the ONEINCH_API_KEY environment variable.
const axios = require('axios');

const API_KEY = process.env.ONEINCH_API_KEY;

async function httpCall() {
  if (!API_KEY) {
    console.error('Error: ONEINCH_API_KEY is not set in the environment.');
    process.exitCode = 1;
    return;
  }

  const url = 'https://api.1inch.com/fusion-plus/quoter/v1.2/quote/receive';

  const config = {
    headers: {
      Authorization: `Bearer ${API_KEY}`,
    },
    params: {
      srcChain: 1,
      dstChain: 137,
      srcTokenAddress: '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
      dstTokenAddress: '0x2791bca1f2de4661ed88a30c99a7a9449aa84174',
      amount: '100000000000000000',
      walletAddress: process.argv[2] || '0x0000000000000000000000000000000000000000',
      enableEstimate: false,
    },
    paramsSerializer: {
      indexes: null,
    },
  };

  try {
    const response = await axios.get(url, config);
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    // Print status and body only, so the request headers (with the key) are never logged.
    console.error(`HTTP ${error.response?.status ?? 'error'}:`, error.response?.data ?? error.message);
    process.exitCode = 1;
  }
}

httpCall();
