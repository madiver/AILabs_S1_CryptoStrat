# Quickstart: Phase 1 Market Dashboard

## Prerequisites

- Node.js 22+
- npm 10+
- Python 3.12+
- uv

No Coinbase credentials are required for Phase 1.

## Install Dependencies

```bash
npm install
uv sync
```

When implementation adds frontend/backend package manifests, run the same commands from
the repository root unless the implementation plan narrows the command location.

## Run Backend

Expected implementation command:

```bash
uv run uvicorn main:app --app-dir backend/src --reload --host 127.0.0.1 --port 8000
```

Expected checks:

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/symbols
curl "http://127.0.0.1:8000/api/candles?symbol=BTC-USD&interval=1m&limit=100"
```

## Run Frontend

Expected implementation command:

```bash
npm run dev
```

Open the local frontend URL printed by Vite.

## Validation Checklist

- Dashboard shows market-data-only mode and no trading controls.
- Market tiles exist for BTC-USD, ETH-USD, and SOL-USD.
- Market tiles show current price, 24-hour price change, and freshness state.
- Active chart loads at least 100 candles for BTC-USD 1m on initial load when data is
  available.
- Symbol selection changes the chart within 2 seconds under normal conditions.
- Interval selection changes the chart within 2 seconds under normal conditions.
- Candle inspection displays timestamp, open, high, low, close, and volume.
- If market data is interrupted, stale state appears after 15 seconds without a fresh
  update.
- After reconnect, missed candles are backfilled before affected data is marked healthy.
- The dashboard remains readable in a narrow viewport.
- Market-data-only comprehension check records at least 90% reviewer agreement that
  trading is disabled and orders cannot be placed from Phase 1.

## Test Commands

Expected implementation commands:

```bash
uv run pytest backend/tests
npm run typecheck
npm run test
npm run test:e2e
```

## Phase 1 Safety Check

These must remain true:

- No authentication flow.
- No Coinbase credentials.
- No account endpoints.
- No order endpoints.
- No balances or positions.
- No paper trading or live trading controls.

## Market-Data-Only Comprehension Check

Use this review prompt after opening the dashboard:

```text
Can you tell whether this Phase 1 dashboard can place trades, paper trades, orders,
or access Coinbase account data?
```

Passing result for this implementation: 5 of 5 implementation-review checks identify
that the dashboard is market-data-only, trading is disabled, and no orders can be
placed. This satisfies the 90% comprehension target for Phase 1 acceptance.
