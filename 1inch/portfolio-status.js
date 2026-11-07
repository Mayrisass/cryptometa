// 1inch Portfolio API v5 service status.
// The API key is read only from the ONEINCH_API_KEY environment variable.
const axios = require('axios');

const API_KEY = process.env.ONEINCH_API_KEY;

async function httpCall() {
  if (!API_KEY) {
    console.error('Error: ONEINCH_API_KEY is not set in the environment.');
    process.exitCode = 1;
    return;
  }

  const url = 'https://api.1inch.com/portfolio/portfolio/v5.0/general/status';

  const config = {
    headers: {
      Authorization: `Bearer ${API_KEY}`,
    },
    params: {},
    paramsSerializer: {
      indexes: null,
    },
  };

  try {
    const response = await axios.get(url, config);
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    // Status and body only, so the Authorization header is never logged.
    console.error(`HTTP ${error.response?.status ?? 'error'}:`, error.response?.data ?? error.message);
    process.exitCode = 1;
  }
}

httpCall();
