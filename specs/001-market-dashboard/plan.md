# Implementation Plan: Phase 1 Market Dashboard

**Branch**: `001-market-dashboard` | **Date**: 2026-06-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-market-dashboard/spec.md`

## Summary

Build a market-data-only crypto dashboard for BTC-USD, ETH-USD, and SOL-USD. The
Python backend ingests Coinbase public market data, normalizes product summaries and
OHLCV candles, tracks freshness/reconnect state, and exposes REST plus WebSocket
contracts to the TypeScript frontend. The frontend renders a dense trading workstation
with market tiles, explicit market-data-only mode, symbol/interval controls, and a
TradingView Lightweight Charts candlestick chart with volume and inspection readouts.

## Technical Context

**Language/Version**: Python 3.13.7 via `uv`; Node.js 22.22.0; TypeScript 6.0.3

**Primary Dependencies**: FastAPI, Uvicorn, httpx, websockets, Pydantic, pytest,
Vite, React, TradingView Lightweight Charts, Vitest, Playwright

**Storage**: N/A for Phase 1. Runtime memory only; no persistence.

**Testing**: pytest + FastAPI TestClient for backend REST/WebSocket behavior; Vitest
for frontend state/formatting helpers; Playwright for chart/dashboard smoke flows.

**Target Platform**: Local developer machine and browser demo.

**Project Type**: Web application with Python backend and TypeScript frontend.

**Performance Goals**: Dashboard identifies supported symbols and mode within 10
seconds; symbol and interval changes update chart state within 2 seconds under normal
conditions; stale data is displayed within 1 second after the 15-second missing-update
threshold.

**Constraints**: Market-data-only; no Coinbase credentials; no authentication; no
persistence; no account access; no paper/live trading controls; chart must initially
load at least 100 recent candles per selected symbol and interval; reconnect must
backfill missed candles before returning affected data to healthy.

**Scale/Scope**: Three products (`BTC-USD`, `ETH-USD`, `SOL-USD`), four intervals
(`1m`, `5m`, `15m`, `1h`), one active chart, public market data only.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Auditability**: PASS. Plan captures connection state changes, symbol/interval
  selections, stale transitions, reconnect transitions, and backfill decisions as
  structured backend events and frontend-visible state.
- **Backend Authority**: PASS. Backend owns Coinbase ingestion, candle construction,
  stale detection, reconnect backfill, and frontend market-data broadcast. No frontend
  credential or order behavior exists.
- **Execution Safety**: PASS. Phase 1 is market-data-only. Live trading, paper trading,
  account access, balances, positions, and orders are excluded from contracts and UI.
- **Realtime Data Validation**: PASS. Plan defines Coinbase as data source, UNIX/RFC3339
  timestamp normalization, 15-second stale threshold, reconnect/backfill behavior, and
  causal live candle update rules.
- **Boundary Discipline**: PASS. Market data, candle aggregation, backend API, frontend
  services, chart components, and UI panels are separate modules with contracts.
- **Validation Scope**: PASS. Tests cover market-data parsing, candle backfill,
  stale/reconnect state transitions, no-trading safety, chart initialization, chart
  inspection, and responsive dashboard flow.

## Project Structure

### Documentation (this feature)

```text
specs/001-market-dashboard/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── openapi.yaml
│   └── websocket-events.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── ailabs_crypto/
│   │   ├── api/
│   │   ├── market_data/
│   │   ├── models/
│   │   └── runtime/
│   └── main.py
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/
│   ├── charts/
│   ├── services/
│   ├── state/
│   └── styles/
└── tests/
    ├── e2e/
    ├── integration/
    └── unit/
```

**Structure Decision**: Use separate `backend/` and `frontend/` directories to preserve
the constitution boundary between backend-owned market data behavior and frontend chart
rendering. Keep existing root `src/index.ts` only until the frontend scaffold replaces
or absorbs it during implementation.

## Phase 0: Research

Research is captured in [research.md](./research.md). All technical unknowns were
resolved:

- Coinbase public market data source and backfill approach.
- TradingView Lightweight Charts realtime update pattern.
- Python web/realtime server approach.
- Frontend application shell approach.
- Testing strategy for backend, frontend, and chart behavior.

## Phase 1: Design And Contracts

Design artifacts are complete:

- [data-model.md](./data-model.md)
- [contracts/openapi.yaml](./contracts/openapi.yaml)
- [contracts/websocket-events.md](./contracts/websocket-events.md)
- [quickstart.md](./quickstart.md)

## Post-Design Constitution Check

- **Auditability**: PASS. Data model includes `AuditEvent`; WebSocket contract includes
  connection state, market summary, candle snapshot/update, and error events.
- **Backend Authority**: PASS. Contracts expose only backend-owned market-data state.
  There are no order, account, credential, position, or balance endpoints.
- **Execution Safety**: PASS. Contracts and quickstart keep the app in market-data-only
  mode; no trading controls or credentials are required.
- **Realtime Data Validation**: PASS. Contracts define timestamps, sequence handling,
  stale threshold, reconnecting state, and backfill completion before healthy state.
- **Boundary Discipline**: PASS. API schemas separate market summaries, candles,
  connection state, and UI-consumable events.
- **Validation Scope**: PASS. Quickstart lists backend, frontend, and browser validation
  checks aligned to the spec.

## Complexity Tracking

No constitution violations.
