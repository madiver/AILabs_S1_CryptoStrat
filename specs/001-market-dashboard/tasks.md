# Tasks: Phase 1 Market Dashboard

**Input**: Design documents from `/specs/001-market-dashboard/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Required by constitution and plan for market data parsing, candle construction, WebSocket contracts, chart behavior, connection states, reconnect backfill, and no-trading safety.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the backend/frontend project structure and install Phase 1 dependencies.

- [X] T001 Create backend package directories in backend/src/ailabs_crypto/{api,market_data,models,runtime} and backend/tests/{contract,integration,unit}
- [X] T002 Create frontend package directories in frontend/src/{components,charts,services,state,styles} and frontend/tests/{integration,unit,e2e}
- [X] T003 Update pyproject.toml with FastAPI, Uvicorn, httpx, websockets, Pydantic, pytest, pytest-asyncio dependencies
- [X] T004 Update package.json with Vite, React, React DOM, TradingView Lightweight Charts, Vitest, Testing Library, Playwright dependencies and dev/build/test scripts
- [X] T005 Add Vite TypeScript configuration in frontend/vite.config.ts
- [X] T006 Add frontend TypeScript configuration in frontend/tsconfig.json
- [X] T007 Add backend package markers in backend/src/ailabs_crypto/__init__.py and backend/src/ailabs_crypto/{api,market_data,models,runtime}/__init__.py
- [X] T008 Add baseline frontend app entry files in frontend/index.html, frontend/src/main.tsx, and frontend/src/styles/base.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared contracts, domain models, configuration, and safety boundaries required before any user story can work.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T009 [P] Define backend market data enums and constants in backend/src/ailabs_crypto/models/constants.py
- [X] T010 [P] Define backend Pydantic models for MarketSymbol, MarketSummary, Candle, ConnectionState, DashboardEvent, and AuditEvent in backend/src/ailabs_crypto/models/market.py
- [X] T011 [P] Define frontend TypeScript contract types matching OpenAPI and WebSocket contracts in frontend/src/services/contracts.ts
- [X] T012 Implement supported symbol and interval validation helpers in backend/src/ailabs_crypto/market_data/catalog.py
- [X] T013 Implement market-data-only runtime settings with trading_enabled=false in backend/src/ailabs_crypto/runtime/settings.py
- [X] T014 Implement structured audit event recorder with in-memory storage in backend/src/ailabs_crypto/runtime/audit.py
- [X] T015 Implement FastAPI app factory and health endpoint in backend/src/ailabs_crypto/api/app.py and backend/src/main.py
- [X] T016 Implement frontend API client shell for REST and WebSocket connections in frontend/src/services/apiClient.ts and frontend/src/services/marketSocket.ts
- [X] T017 [P] Add backend safety test proving no order/account/balance/position routes exist in backend/tests/contract/test_no_trading_routes.py
- [X] T018 [P] Add frontend safety test proving no trading action labels render in frontend/tests/unit/noTradingSafety.test.tsx
- [X] T019 Run uv sync and npm install to update uv.lock and package-lock.json with Phase 1 dependencies

**Checkpoint**: Foundation ready. Backend can start, `/api/health` returns market-data-only mode, shared types exist, and no trading routes/UI are present.

---

## Phase 3: User Story 1 - Monitor Market Status (Priority: P1) MVP

**Goal**: A viewer opens the dashboard and sees BTC-USD, ETH-USD, and SOL-USD market tiles with current price, 24-hour price change, and freshness state while clearly seeing trading is disabled.

**Independent Test**: Open the dashboard with market data available and verify all three market tiles show price, 24-hour price change, freshness state, and market-data-only mode without credentials.

### Tests for User Story 1

- [X] T020 [P] [US1] Add backend contract tests for GET /api/symbols and GET /api/markets/summary in backend/tests/contract/test_market_summary_contract.py
- [X] T021 [P] [US1] Add backend unit tests for Coinbase public product parsing into MarketSummary in backend/tests/unit/test_coinbase_product_parser.py
- [X] T022 [P] [US1] Add frontend unit tests for market tile rendering and market-data-only mode in frontend/tests/unit/MarketTiles.test.tsx
- [X] T023 [P] [US1] Add Playwright MVP smoke test for dashboard market tiles and no trading controls in frontend/tests/e2e/marketTiles.spec.ts

### Implementation for User Story 1

- [X] T024 [P] [US1] Implement Coinbase public product client for BTC-USD, ETH-USD, and SOL-USD in backend/src/ailabs_crypto/market_data/coinbase_client.py
- [X] T025 [US1] Implement MarketSummaryService for current price, 24-hour price change, freshness, and audit events in backend/src/ailabs_crypto/market_data/summary_service.py
- [X] T026 [US1] Implement GET /api/symbols and GET /api/markets/summary routes in backend/src/ailabs_crypto/api/routes_market.py
- [X] T027 [US1] Register market routes in backend/src/ailabs_crypto/api/app.py
- [X] T028 [P] [US1] Implement frontend market store for summaries, active symbol, and mode in frontend/src/state/marketStore.ts
- [X] T029 [P] [US1] Implement MarketModeBanner component in frontend/src/components/MarketModeBanner.tsx
- [X] T030 [P] [US1] Implement MarketTile and MarketTileGrid components in frontend/src/components/MarketTile.tsx and frontend/src/components/MarketTileGrid.tsx
- [X] T031 [US1] Wire initial dashboard layout with market tiles and mode banner in frontend/src/App.tsx
- [X] T032 [US1] Add workstation-style base layout and responsive tile styling in frontend/src/styles/dashboard.css

**Checkpoint**: User Story 1 is complete when the app displays three supported market tiles, 24-hour change, freshness, and market-data-only mode with no trading controls.

---

## Phase 4: User Story 2 - Inspect Symbol Candles (Priority: P2)

**Goal**: A viewer selects a supported symbol and inspects a large candlestick chart with volume, at least 100 historical candles on initial load, live updates, and OHLCV readout.

**Independent Test**: Select each supported symbol and verify the main chart, volume display, selected state, 100-candle initial load, and candle inspection readout update for that symbol.

### Tests for User Story 2

- [X] T033 [P] [US2] Add backend contract tests for GET /api/candles with supported inputs, unsupported inputs, complete history, partial history, and unavailable history in backend/tests/contract/test_candles_contract.py
- [X] T034 [P] [US2] Add backend unit tests for Coinbase candle parsing, sorting, validation, and 100-candle minimum in backend/tests/unit/test_candle_service.py
- [X] T035 [P] [US2] Add frontend unit tests for chart data mapping, candle readout formatting, and unavailable volume display in frontend/tests/unit/chartMapping.test.ts
- [X] T036 [P] [US2] Add Playwright chart smoke test for symbol selection, rendered canvas, and OHLCV readout in frontend/tests/e2e/candlestickChart.spec.ts

### Implementation for User Story 2

- [X] T037 [P] [US2] Extend Coinbase client with public candles requests and granularity mapping in backend/src/ailabs_crypto/market_data/coinbase_client.py
- [X] T038 [US2] Implement CandleService for historical candle loading, validation, and source=historical tagging in backend/src/ailabs_crypto/market_data/candle_service.py
- [X] T039 [US2] Implement GET /api/candles route in backend/src/ailabs_crypto/api/routes_market.py
- [X] T040 [P] [US2] Implement frontend candle REST loader in frontend/src/services/candleService.ts
- [X] T041 [P] [US2] Implement Lightweight Charts wrapper with candlestick and histogram volume series in frontend/src/charts/LightweightCandlestickChart.tsx
- [X] T042 [P] [US2] Implement chart data conversion helpers in frontend/src/charts/chartData.ts
- [X] T043 [US2] Implement CandleReadout component for timestamp, open, high, low, close, and volume in frontend/src/components/CandleReadout.tsx
- [X] T044 [US2] Wire active symbol selection from MarketTileGrid to candle loading and chart rendering in frontend/src/App.tsx
- [X] T045 [US2] Add chart layout, volume pane, and readout styling in frontend/src/styles/chart.css

**Checkpoint**: User Story 2 is complete when each supported symbol can render at least 100 recent candles with volume and inspectable OHLCV details.

---

## Phase 5: User Story 3 - Change Chart Interval (Priority: P3)

**Goal**: A viewer changes the active chart interval among 1m, 5m, 15m, and 1h and sees chart state update within the same dashboard flow.

**Independent Test**: Switch through all supported intervals for a selected symbol and verify the active interval is visible and the chart reloads that interval within 2 seconds under normal conditions.

### Tests for User Story 3

- [X] T046 [P] [US3] Add backend unit tests for interval validation and Coinbase granularity mapping in backend/tests/unit/test_intervals.py
- [X] T047 [P] [US3] Add frontend unit tests for interval selector state and invalid interval rejection in frontend/tests/unit/IntervalSelector.test.tsx
- [X] T048 [P] [US3] Add Playwright test for switching 1m, 5m, 15m, and 1h intervals in frontend/tests/e2e/intervalSwitching.spec.ts

### Implementation for User Story 3

- [X] T049 [P] [US3] Implement interval metadata and labels in frontend/src/state/intervals.ts
- [X] T050 [P] [US3] Implement IntervalSelector component in frontend/src/components/IntervalSelector.tsx
- [X] T051 [US3] Wire interval selection to candle reload and active chart state in frontend/src/App.tsx
- [X] T052 [US3] Ensure backend candle endpoint returns 400 for unsupported intervals in backend/src/ailabs_crypto/api/routes_market.py
- [X] T053 [US3] Add interval selector styling and compact responsive behavior in frontend/src/styles/dashboard.css

**Checkpoint**: User Story 3 is complete when the chart supports all four required intervals and rejects unsupported intervals.

---

## Phase 6: User Story 4 - Understand Connection Health (Priority: P4)

**Goal**: A viewer can distinguish healthy, stale, reconnecting, and offline states, and missed candles are backfilled before affected data returns to healthy.

**Independent Test**: Simulate healthy, stale, reconnecting, offline, and reconnect-with-gap states and verify the dashboard communicates each state distinctly while preserving last known values and backfilling before healthy.

### Tests for User Story 4

- [X] T054 [P] [US4] Add backend unit tests for 15-second stale detection and connection state transitions in backend/tests/unit/test_connection_state.py
- [X] T055 [P] [US4] Add backend unit tests for reconnect backfill before healthy state in backend/tests/unit/test_backfill.py
- [X] T056 [P] [US4] Add backend WebSocket contract tests for connection_state, market_summary, candle_snapshot, candle_update, and error events in backend/tests/contract/test_market_websocket_contract.py
- [X] T057 [P] [US4] Add frontend unit tests for WebSocket event reducer and stale/reconnecting/offline states in frontend/tests/unit/marketSocketReducer.test.ts
- [X] T058 [P] [US4] Add Playwright test for visible connection states and no stale data presented as current in frontend/tests/e2e/connectionHealth.spec.ts

### Implementation for User Story 4

- [X] T059 [P] [US4] Implement connection state machine in backend/src/ailabs_crypto/market_data/connection_state.py
- [X] T060 [US4] Implement Coinbase WebSocket consumer for public market data and heartbeats in backend/src/ailabs_crypto/market_data/coinbase_ws.py
- [X] T061 [US4] Implement reconnect and missed-candle backfill orchestration in backend/src/ailabs_crypto/market_data/backfill.py
- [X] T062 [US4] Implement dashboard WebSocket manager and event broadcasting in backend/src/ailabs_crypto/api/ws_market_data.py
- [X] T063 [US4] Register WebSocket route in backend/src/ailabs_crypto/api/app.py
- [X] T064 [P] [US4] Implement frontend WebSocket event reducer in frontend/src/state/marketEvents.ts
- [X] T065 [P] [US4] Implement ConnectionStatus component in frontend/src/components/ConnectionStatus.tsx
- [X] T066 [US4] Wire backend WebSocket events into frontend market store and chart updates in frontend/src/services/marketSocket.ts and frontend/src/App.tsx
- [X] T067 [US4] Ensure chart applies candle_snapshot with setData and candle_update with update in frontend/src/charts/LightweightCandlestickChart.tsx
- [X] T068 [US4] Add connection status and stale/offline styling in frontend/src/styles/dashboard.css

**Checkpoint**: User Story 4 is complete when all connection states are visible, stale data is marked after 15 seconds, missed candles are backfilled, and healthy returns only after backfill completes.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validate the full Phase 1 dashboard, document run behavior, and remove rough edges.

- [X] T069 Run backend tests with uv run pytest backend/tests and fix failures in backend/src/ailabs_crypto
- [X] T070 Run frontend unit tests with npm run test and fix failures in frontend/src
- [X] T071 Run TypeScript typecheck with npm run typecheck and fix failures in frontend/src and package configuration
- [X] T072 Run Playwright tests with npm run test:e2e and fix browser/layout/chart issues in frontend/src
- [X] T073 Validate quickstart commands and update specs/001-market-dashboard/quickstart.md if commands changed
- [X] T074 Verify no Coinbase credentials, account endpoints, order endpoints, balances, positions, paper trading, or live trading controls exist in backend/src and frontend/src
- [X] T075 Run a market-data-only comprehension check and document that at least 90% of reviewers identify trading as disabled in specs/001-market-dashboard/quickstart.md
- [X] T076 Update README.md with Phase 1 run instructions and market-data-only disclaimer
- [X] T077 Review frontend responsive layout on desktop and narrow viewport and adjust frontend/src/styles/dashboard.css and frontend/src/styles/chart.css
- [X] T078 Confirm structured audit events are emitted for stale transitions, reconnect attempts, backfill completion, offline transitions, symbol selection, interval selection, and safety checks in backend/src/ailabs_crypto/runtime/audit.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; starts immediately.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational; MVP scope.
- **User Story 2 (Phase 4)**: Depends on Foundational and integrates with US1 active symbol state.
- **User Story 3 (Phase 5)**: Depends on US2 chart and candle loading.
- **User Story 4 (Phase 6)**: Depends on backend/frontend foundations and chart update paths from US2.
- **Polish (Phase 7)**: Depends on all implemented user stories.

### User Story Dependencies

- **US1 Monitor Market Status**: Independent after foundation; recommended MVP.
- **US2 Inspect Symbol Candles**: Can start after foundation but integrates best after US1 establishes active symbol UI.
- **US3 Change Chart Interval**: Depends on US2 candle loading and chart rendering.
- **US4 Understand Connection Health**: Can build backend state after foundation, but frontend chart update completion depends on US2.

### Within Each User Story

- Write tests before implementation.
- Backend models and services before routes/WebSocket endpoints.
- Frontend services/state before components that consume them.
- Components before Playwright final validation.

---

## Parallel Opportunities

- T009-T011 can run in parallel after setup.
- T020-T023 can run in parallel for US1 tests.
- T024, T028, T029, and T030 can run in parallel after US1 tests are written.
- T033-T036 can run in parallel for US2 tests.
- T037, T040, T041, and T042 can run in parallel after US2 tests are written.
- T046-T048 can run in parallel for US3 tests.
- T049 and T050 can run in parallel with T052.
- T054-T058 can run in parallel for US4 tests.
- T059, T064, and T065 can run in parallel after US4 tests are written.

---

## Parallel Example: User Story 1

```bash
Task: "T020 [P] [US1] Add backend contract tests for GET /api/symbols and GET /api/markets/summary in backend/tests/contract/test_market_summary_contract.py"
Task: "T021 [P] [US1] Add backend unit tests for Coinbase public product parsing into MarketSummary in backend/tests/unit/test_coinbase_product_parser.py"
Task: "T022 [P] [US1] Add frontend unit tests for market tile rendering and market-data-only mode in frontend/tests/unit/MarketTiles.test.tsx"
Task: "T023 [P] [US1] Add Playwright MVP smoke test for dashboard market tiles and no trading controls in frontend/tests/e2e/marketTiles.spec.ts"
```

## Parallel Example: User Story 2

```bash
Task: "T037 [P] [US2] Extend Coinbase client with public candles requests and granularity mapping in backend/src/ailabs_crypto/market_data/coinbase_client.py"
Task: "T040 [P] [US2] Implement frontend candle REST loader in frontend/src/services/candleService.ts"
Task: "T041 [P] [US2] Implement Lightweight Charts wrapper with candlestick and histogram volume series in frontend/src/charts/LightweightCandlestickChart.tsx"
Task: "T042 [P] [US2] Implement chart data conversion helpers in frontend/src/charts/chartData.ts"
```

## Parallel Example: User Story 4

```bash
Task: "T059 [P] [US4] Implement connection state machine in backend/src/ailabs_crypto/market_data/connection_state.py"
Task: "T064 [P] [US4] Implement frontend WebSocket event reducer in frontend/src/state/marketEvents.ts"
Task: "T065 [P] [US4] Implement ConnectionStatus component in frontend/src/components/ConnectionStatus.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup.
2. Complete Phase 2 foundation.
3. Complete US1 market tiles and mode banner.
4. Run US1 backend, frontend, and Playwright tests.
5. Stop and validate the market-data-only dashboard MVP.

### Incremental Delivery

1. US1 delivers market tiles and safety mode.
2. US2 adds candlestick chart, volume, and readout.
3. US3 adds interval switching.
4. US4 adds full connection health, stale detection, WebSocket updates, and reconnect backfill.
5. Polish validates the full quickstart and responsive workstation behavior.

### Format Validation

All task lines above follow the required checklist format:

```text
Task line shape: - [ ] T### [P?] [US?] Description with file path
```

Setup, Foundational, and Polish tasks omit story labels. User story tasks include `[US1]`, `[US2]`, `[US3]`, or `[US4]`.
