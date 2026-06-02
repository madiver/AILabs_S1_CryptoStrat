# Research: Phase 1 Market Dashboard

## Decision: Use Coinbase Advanced Trade public market data surfaces

**Rationale**: Coinbase Advanced Trade WebSocket market data is publicly available for
most channels and provides the `ticker`, `ticker_batch`, `candles`, `market_trades`,
and `heartbeats` channels without authentication. The public REST product endpoint
provides current price and `price_percentage_change_24h`, and the public candles
endpoint supports the required granularities and a limit up to 350 candles, which is
enough for the 100-candle initial chart requirement.

Official docs reviewed:

- Coinbase Advanced Trade WebSocket overview:
  https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/websocket/websocket-overview
- Coinbase Advanced Trade WebSocket channels:
  https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/websocket/websocket-channels
- Coinbase public product endpoint:
  https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/public/get-public-product
- Coinbase public product candles endpoint:
  https://coinbase-cloud.mintlify.app/api-reference/advanced-trade-api/rest-api/public/get-public-product-candles

Verification note: unauthenticated requests to the public product and public candles
endpoints returned HTTP 200 during planning, so Phase 1 can avoid Coinbase credentials.

**Alternatives considered**:

- Use authenticated Coinbase APIs: rejected for Phase 1 because the spec explicitly
  requires no credentials and no account access.
- Build candles only from market trades: rejected for Phase 1 because the public candles
  endpoint can seed the chart directly, and live candles can be refreshed from public
  candle/ticker streams.
- Use a third-party market-data provider: rejected because the roadmap specifies
  Coinbase as the centralized exchange integration.

## Decision: Seed charts with REST candles, then update via backend-normalized realtime data

**Rationale**: The spec requires at least 100 historical candles on initial load and
backfill after reconnect. REST candles are the right source for deterministic initial
loads and missed-candle recovery. Realtime updates should flow through the backend,
which normalizes the data and only marks affected symbol/interval state healthy after
backfill completes.

**Alternatives considered**:

- Seed from frontend calls directly to Coinbase: rejected because the constitution keeps
  market-data normalization and health decisions in the backend.
- Start charts empty and fill from live updates: rejected by clarification.
- Keep chart gaps after reconnect: rejected by clarification.

## Decision: Use FastAPI for the Python backend

**Rationale**: FastAPI supports REST endpoints, WebSocket endpoints, automatic OpenAPI
generation, Pydantic validation, and straightforward pytest/TestClient coverage. It
matches the frontend/backend split and keeps public market-data contracts explicit.

Current docs reviewed through Context7: `/fastapi/fastapi`, focused on WebSocket
endpoints and TestClient WebSocket testing.

**Alternatives considered**:

- Flask: rejected because WebSocket support requires extra moving parts and the project
  benefits from native validation/OpenAPI.
- aiohttp: viable but less aligned with automatic OpenAPI and common Python API testing
  patterns for this project.
- Pure Python WebSocket server: rejected because REST contracts, OpenAPI, and test
  ergonomics matter for Spec Kit traceability.

## Decision: Use Vite + React + TypeScript for the frontend

**Rationale**: The UI is a dense stateful dashboard with tiles, connection state,
symbol/interval controls, chart components, and responsive layout. React provides a
practical component model; Vite provides a fast TypeScript dev/build path with standard
`npm run dev`, `npm run build`, and `npm run preview` scripts.

Current docs reviewed through Context7: `/vitejs/vite`, focused on TypeScript app setup
and standard npm dev/build/preview scripts.

**Alternatives considered**:

- Vanilla TypeScript: viable but more manual state and component organization for the
  trading workstation UI.
- Next.js: rejected for Phase 1 because routing/server rendering is unnecessary.
- Svelte/Vue: viable but not already implied by the repo; React is the conservative
  default for a complex TypeScript dashboard.

## Decision: Use TradingView Lightweight Charts for chart rendering

**Rationale**: Lightweight Charts supports candlestick series, histogram volume series,
initial `setData`, and efficient realtime `update` calls for modifying the latest bar or
appending a new one. This matches the clarified requirements for initial historical
candles, live updates, volume display, and TradingView-like chart behavior.

Current docs reviewed through Context7: `/tradingview/lightweight-charts`, focused on
candlestick series, histogram series, `setData`, `update`, and realtime updates.

**Alternatives considered**:

- Full TradingView Charting Library: rejected because access/licensing is heavier than
  needed for Phase 1.
- Chart.js/D3: rejected because they would require more custom financial chart behavior.
- Server-rendered charts: rejected because the dashboard needs interactive browser-side
  inspection.

## Decision: Use backend WebSocket for dashboard updates plus REST for initial reads

**Rationale**: REST endpoints are simple and cacheable for supported symbols, market
summary, and initial candles. A backend WebSocket is appropriate for connection state,
market tile updates, candle updates, stale transitions, and reconnect/backfill events.
Keeping the frontend connected to the backend rather than Coinbase preserves the
backend-authority and no-credential constraints.

**Alternatives considered**:

- Frontend connects directly to Coinbase WebSocket: rejected by backend boundary
  principle.
- Server-Sent Events: viable for one-way updates, but WebSocket is more flexible for
  symbol/interval subscriptions during later phases.
- Polling only: rejected because it weakens realtime freshness and reconnect signaling.

## Decision: No persistence in Phase 1

**Rationale**: The spec excludes persistence. Runtime memory can hold current symbols,
latest summaries, candle windows, connection health, and audit events needed during the
demo session. Durable audit/event storage can be introduced in a later phase.

**Alternatives considered**:

- SQLite ledger: rejected for Phase 1 scope.
- Browser local storage: rejected because the project does not need user settings yet
  and the constitution avoids unnecessary persistence.

## Decision: Testing targets

**Rationale**: Backend tests must verify Coinbase payload parsing, candle normalization,
stale detection after 15 seconds, reconnect backfill before healthy, and absence of
trading endpoints. Frontend tests must verify visible market-data-only state, symbol and
interval selection, chart initialization with 100 candles, candle readout formatting,
and responsive workstation layout. Browser smoke tests should catch canvas/chart
rendering and layout failures that unit tests cannot see.

**Alternatives considered**:

- Unit tests only: rejected because WebSocket flows and canvas rendering need integration
  and browser validation.
- Manual demo only: rejected by constitution-required validation.
