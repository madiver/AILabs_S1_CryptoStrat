# Feature Specification: Phase 1 Market Dashboard

**Feature Branch**: `001-market-dashboard`

**Created**: 2026-06-02

**Status**: Draft

**Input**: User description: "Create the Phase 1 Market Dashboard for AI in the Lab - Episode 1: Crypto Trading Dashboard. The feature should provide a real-time, market-data-only crypto dashboard for BTC-USD, ETH-USD, and SOL-USD. Users should be able to see current market status at a glance, switch between supported symbols, inspect a large candlestick chart for the active symbol, and understand whether the app is connected to live market data. This phase is strictly market-data-only. There is no authentication, no persistence, no order placement, no paper trading, and no live trading. The dashboard must clearly communicate that trading is disabled."

## Clarifications

### Session 2026-06-02

- Q: How long without an update should pass before market data is marked stale? -> A: 15 seconds
- Q: What comparison window should market tiles use for recent change? -> A: 24-hour price change
- Q: Should the chart show historical candles on initial load or build only from live updates? -> A: Show recent historical candles on initial load, then live updates
- Q: How many historical candles should load for the selected symbol and interval? -> A: At least 100 recent candles
- Q: What should happen after reconnect if candles were missed? -> A: Backfill missed candles before marking data healthy again

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Monitor Market Status (Priority: P1)

A viewer opens the dashboard and immediately sees the current market status for
BTC-USD, ETH-USD, and SOL-USD, including price, 24-hour price change, and whether
each displayed value is fresh.

**Why this priority**: This is the minimum useful dashboard experience. Without an
at-a-glance market overview and freshness indication, the screen cannot be trusted
as a live market dashboard.

**Independent Test**: Open the dashboard with market data available and verify that
all three supported symbols show price, 24-hour price change, and freshness state
without requiring any user setup or credentials.

**Acceptance Scenarios**:

1. **Given** live market data is available, **When** a user opens the dashboard,
   **Then** market tiles for BTC-USD, ETH-USD, and SOL-USD show current price,
   24-hour price change, and freshness status.
2. **Given** one symbol has not received a fresh update within 15 seconds,
   **When** the market tile is displayed, **Then** that tile clearly indicates stale
   data without hiding the last known value.
3. **Given** the dashboard has loaded, **When** the user scans the screen,
   **Then** the user can identify that the product is in market-data-only mode and
   that trading is disabled.

---

### User Story 2 - Inspect Symbol Candles (Priority: P2)

A viewer selects one supported symbol and inspects a large candlestick chart with
volume for that symbol. The chart is populated with recent historical candles on
initial load and then continues with live updates.

**Why this priority**: Candlestick inspection is the primary analytical view for the
dashboard and the foundation for later strategy and signal visibility.

**Independent Test**: Select each supported symbol and verify that the main chart,
volume display, and selected-symbol state all update to match the chosen symbol.

**Acceptance Scenarios**:

1. **Given** the dashboard is showing any supported symbol, **When** the user selects
   BTC-USD, ETH-USD, or SOL-USD, **Then** the main chart updates to the selected
   symbol and the selected state is visible.
2. **Given** candle and volume data exists for the selected symbol, **When** the main
   chart is displayed, **Then** the user sees candlesticks and a corresponding
   volume pane for the same time range.
3. **Given** the dashboard has just loaded, **When** the user views the active chart,
   **Then** at least 100 recent historical candles are visible before waiting for new
   live candles to accumulate.
4. **Given** the user hovers over or inspects a candle, **When** the candle readout is
   shown, **Then** it includes timestamp, open, high, low, close, and volume.

---

### User Story 3 - Change Chart Interval (Priority: P3)

A viewer changes the active chart interval among 1m, 5m, 15m, and 1h to inspect
different market time horizons.

**Why this priority**: Time interval switching makes the chart useful for short-term
and broader intraday context while staying within the Phase 1 market-data scope.

**Independent Test**: Switch through all supported intervals for a selected symbol
and verify that the active interval is visible and the chart represents that interval.

**Acceptance Scenarios**:

1. **Given** a supported symbol is selected, **When** the user chooses 1m, 5m, 15m,
   or 1h, **Then** the selected interval becomes visible and the chart updates to
   that interval.
2. **Given** a selected interval has temporarily incomplete data, **When** the chart
   updates, **Then** the dashboard preserves usable chart context and communicates
   the data limitation.

---

### User Story 4 - Understand Connection Health (Priority: P4)

A viewer can tell whether the live market data feed and application connection are
healthy, stale, reconnecting, or offline.

**Why this priority**: Realtime financial displays are misleading without visible
connection health and stale-data behavior.

**Independent Test**: Simulate healthy, stale, reconnecting, and offline states and
verify that the dashboard communicates each state distinctly while preserving the
last known safe display where appropriate.

**Acceptance Scenarios**:

1. **Given** live updates are arriving normally, **When** the dashboard is displayed,
   **Then** the connection indicator shows a healthy state and recent update time.
2. **Given** updates stop arriving, **When** 15 seconds pass without a fresh update,
   **Then** the dashboard marks the affected market data as stale.
3. **Given** the connection is recovering, **When** reconnect behavior is active,
   **Then** the dashboard shows a reconnecting state and avoids implying that data is
   current until fresh updates resume.
4. **Given** candles were missed during an interruption, **When** reconnect succeeds,
   **Then** the dashboard backfills the missed candles before marking the affected
   data healthy again.
5. **Given** market data is unavailable, **When** the dashboard cannot receive live
   updates, **Then** the dashboard shows an offline state and no trading controls.

### Edge Cases

- Market data for one symbol is stale while the other symbols are fresh.
- No market data has arrived yet for one or more supported symbols.
- The selected symbol becomes stale or offline while another symbol remains healthy.
- The user switches intervals during reconnecting or stale-data states.
- A candle is partially formed and still receiving live updates.
- Recent historical candles are unavailable or incomplete at initial load.
- A reconnect succeeds after one or more candles were missed.
- The user inspects a candle whose volume is zero or unavailable.
- The dashboard is opened on a narrow viewport where dense information still needs to
  remain readable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The dashboard MUST display market tiles for BTC-USD, ETH-USD, and
  SOL-USD.
- **FR-002**: Each market tile MUST display current price, 24-hour price change, and
  data freshness state.
- **FR-003**: The dashboard MUST provide a visible market-data-only mode indicator
  that communicates trading is disabled.
- **FR-004**: The dashboard MUST NOT expose controls, wording, or workflows that
  imply order placement, paper trading, live trading, authentication, account access,
  balances, or positions are available in Phase 1.
- **FR-005**: Users MUST be able to select BTC-USD, ETH-USD, or SOL-USD as the active
  chart symbol.
- **FR-006**: The main chart MUST reflect the active selected symbol.
- **FR-007**: Users MUST be able to select chart intervals of 1m, 5m, 15m, and 1h.
- **FR-008**: The main chart MUST display candlestick data for the active symbol and
  active interval.
- **FR-009**: The chart MUST show recent historical candles on initial load before
  relying on newly arriving live updates.
- **FR-010**: The chart MUST load at least 100 recent candles for the selected symbol
  and interval when market data is available.
- **FR-011**: The chart view MUST display volume aligned with the visible candle time
  range.
- **FR-012**: Users MUST be able to inspect candle details including timestamp, open,
  high, low, close, and volume.
- **FR-013**: The dashboard MUST distinguish healthy, stale, reconnecting, and offline
  connection states.
- **FR-014**: The dashboard MUST mark market data stale when 15 seconds pass without
  a fresh update for the affected symbol or chart.
- **FR-015**: The dashboard MUST preserve the last known market values during stale,
  reconnecting, or offline states while clearly marking them as not fresh.
- **FR-016**: The dashboard MUST avoid displaying stale market data as current.
- **FR-017**: After reconnecting, the dashboard MUST backfill missed candles for the
  affected symbol and interval before marking that data healthy again.
- **FR-018**: The dashboard MUST remain usable when one symbol is unavailable while
  other supported symbols continue updating.
- **FR-019**: The dashboard MUST provide a dense workstation-style layout centered on
  market monitoring rather than a marketing or landing-page experience.

### Key Entities *(include if feature involves data)*

- **Market Symbol**: A supported trading pair shown in the dashboard. Key attributes
  include symbol code, display name, active selection state, latest price, 24-hour
  price change, and freshness state.
- **Market Tile**: A compact summary of one market symbol. Key attributes include
  symbol, price, 24-hour price change, latest update time, and health/freshness
  indicator.
- **Candle**: A time-bounded market summary for a symbol and interval. Key attributes
  include timestamp, open, high, low, close, volume, symbol, interval, and completion
  state. Candles may be historical or live-updated.
- **Chart Interval**: A user-selectable time grouping for candles. Initial values are
  1m, 5m, 15m, and 1h.
- **Connection State**: The displayed health state for market data and application
  connectivity. Values include healthy, stale, reconnecting, and offline.

### Trading Safety And Auditability *(include if feature touches market data, strategy, risk, execution, persistence, credentials, or trading UI state)*

- **Mode Constraint**: The feature operates only in market-data-only mode. Live
  trading, paper trading, authentication, positions, balances, and order actions are
  outside Phase 1 scope.
- **Backend Authority**: No trading authority exists in this phase. No user action may
  request, queue, submit, cancel, simulate, or reconcile an order.
- **Risk Controls**: The required risk control for Phase 1 is prevention by absence:
  the dashboard must expose no trading controls and must visibly state that trading is
  disabled.
- **Audit Events**: The feature must make connection health, symbol selection, interval
  selection, stale-data transitions, reconnecting transitions, and offline transitions
  observable for review.
- **Realtime Data Assumptions**: Market values are live only when the dashboard marks
  them healthy. Stale, reconnecting, and offline displays must retain context without
  presenting old values as current. Data interrupted by reconnects must be backfilled
  before the affected display returns to healthy.
- **Credential Boundary**: No Coinbase credentials or user account credentials are
  required, requested, displayed, stored, or implied for Phase 1.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time viewer can identify all three supported symbols, the active
  symbol, and the market-data-only mode within 10 seconds of opening the dashboard.
- **SC-002**: Users can switch from one supported symbol to another and see the chart
  reflect the new symbol within 2 seconds under normal operating conditions.
- **SC-003**: Users can switch among all four supported intervals and see the active
  interval reflected in the chart within 2 seconds under normal operating conditions.
- **SC-004**: In usability review, at least 90% of reviewers can correctly state that
  trading is disabled and no orders can be placed from the Phase 1 dashboard.
- **SC-005**: When market data becomes stale, reconnecting, or offline during testing,
  the dashboard communicates the changed state within 1 second after the 15-second
  missing-update threshold is reached.
- **SC-006**: Users can inspect a visible candle and identify its timestamp, open,
  high, low, close, and volume without leaving the chart view.
- **SC-007**: After reconnecting from a simulated interruption, missed candles are
  restored before the affected symbol and interval return to a healthy state.
- **SC-008**: On initial load with market data available, the active chart displays
  at least 100 recent historical candles without requiring users to wait for new live
  candles.
- **SC-009**: The dashboard remains readable and operable for the primary monitoring
  flow on both desktop and narrow viewport layouts.

## Assumptions

- Phase 1 users are viewers of the live build or repository demo who need market
  visibility, not account management or trading controls.
- The supported market universe for Phase 1 is exactly BTC-USD, ETH-USD, and SOL-USD.
- The supported chart intervals for Phase 1 are exactly 1m, 5m, 15m, and 1h.
- "Recent change" means 24-hour price change.
- The freshness window is 15 seconds and is used consistently across tiles, chart
  state, and connection indicators.
- The chart should load recent historical candles first and then continue updating
  with live market data.
- The initial chart history target is at least 100 recent candles for the selected
  symbol and interval when market data is available.
- After reconnecting, missed candles are backfilled before affected data is marked
  healthy again.
- Historical persistence, user authentication, paper trading, live trading, balances,
  positions, and order history are intentionally excluded from Phase 1.
