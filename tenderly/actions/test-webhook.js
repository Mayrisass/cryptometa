// Runs actionFn locally against an in-memory stand-in for context.storage.
const assert = require('assert');
const { actionFn } = require('./webhook');

const store = new Map();
const context = {
    storage: {
        getNumber: async (k) => (store.has(k) ? store.get(k) : 0),
        putNumber: async (k, v) => store.set(k, v),
        getJson: async (k) => store.get(k) || {},
        putJson: async (k, v) => store.set(k, v),
    },
};

(async () => {
    assert.deepStrictEqual(await actionFn(context, { payload: { exampleKey: 'exampleValue' } }), { count: 1 });
    assert.deepStrictEqual(await actionFn(context, { payload: { a: 1 } }), { count: 2 });
    assert.deepStrictEqual(store.get('webhook/last-payload').payload, { a: 1 });
    for (const bad of [undefined, null, 'text', [1, 2]]) {
        await assert.rejects(actionFn(context, { payload: bad }));
    }
    assert.strictEqual(store.get('webhook/count'), 2);
    console.log('ok');
})().catch((e) => { console.error(e); process.exit(1); });
