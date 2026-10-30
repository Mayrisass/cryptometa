# Market analysis

Market-data notes and charts built with [Massive](https://massive.com) data.
Separate from the token metadata in `data/`; nothing here is read by `bin/generate`.

| Folder | Contents |
| --- | --- |
| [`2026-10-chip-selloff/`](2026-10-chip-selloff/) | October 2026 tech/chip selloff: market vs. sectors, what drove XLK's drop, why Nvidia lagged the rebound, big-tech capex scorecard |
| [`tools/`](tools/) | `massive_indices_ws.py` — streams per-minute index bars from Massive's WebSocket API |

## Running the tools

```bash
pip install websockets matplotlib
export MASSIVE_API_KEY=...        # https://massive.com/dashboard/keys — never commit it
python tools/massive_indices_ws.py I:SPX I:NDX   # needs an Indices plan
```
