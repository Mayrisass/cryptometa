// Tenderly Web3 Action: handles payloads POSTed to the action's webhook trigger
// (for example by ../webhook.py). It logs each payload, keeps the latest one and a
// running count in the project's storage, and fails the run on a payload that is not
// a JSON object, so bad calls show up as failed in the Execution History.

const STORAGE_LAST = 'webhook/last-payload';
const STORAGE_COUNT = 'webhook/count';

// Do not change function name.
const actionFn = async (context, webhookEvent) => {
    const payload = webhookEvent && webhookEvent.payload;
    if (payload === null || typeof payload !== 'object' || Array.isArray(payload)) {
        throw new Error(`Expected a JSON object payload, got: ${JSON.stringify(payload)}`);
    }

    const count = ((await context.storage.getNumber(STORAGE_COUNT)) || 0) + 1;
    const received = { receivedAt: new Date().toISOString(), payload };

    await context.storage.putJson(STORAGE_LAST, received);
    await context.storage.putNumber(STORAGE_COUNT, count);

    console.log(`Webhook call #${count}:`, JSON.stringify(payload));

    // To access a project secret (Tenderly dashboard > Web3 Actions > Secrets):
    // const secret = await context.secrets.get('MY-SECRET');

    return { count };
};

// Do not change this.
module.exports = { actionFn };
