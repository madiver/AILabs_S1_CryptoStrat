# Product Roadmap

## Product Direction

AI in the Lab - Episode 1: Crypto Trading Dashboard will build a web-based crypto trading dashboard with a TypeScript frontend and Python backend. The system will use Coinbase as the centralized exchange integration and will start as a real-time market-data and paper-trading application before any live trading capability is enabled.

The goal is to demonstrate an auditable AI-assisted engineering workflow, not to produce investment advice or a production trading system in the first build.

## Core Principles

- Keep the dashboard useful before enabling execution.
- Treat the backend as the only authority for strategy logic, risk checks, and Coinbase API signing.
- Keep live trading disabled by default.
- Capture strategy decisions, risk decisions, orders, fills, and errors as auditable events.
- Prefer simple, explainable strategy behavior before complex models.
- Separate market data, strategy evaluation, risk gating, execution, and UI concerns.

## Target Architecture

- Frontend: TypeScript web application.
- Backend: Python service.
- Exchange: Coinbase Advanced Trade API.
- Market data: Coinbase WebSocket, normalized by the backend.
- Order/account management: Coinbase REST API through the backend.
- Charting: TradingView Lightweight Charts.
- Initial symbols: `BTC-USD`, `ETH-USD`, `SOL-USD`.

## Frontend Roadmap

### Phase 1: Market Dashboard

- Real-time symbol tiles for `BTC-USD`, `ETH-USD`, and `SOL-USD`.
- Large active candlestick chart.
- Symbol selector.
- Timeframe selector for `1m`, `5m`, `15m`, and `1h`.
- Volume pane.
- Coinbase/backend connection status.
- Market-data-only mode indicator.

### Phase 2: Strategy Visibility

- Strategy status panel.
- Current signal display: long, short, or flat.
- Signal confidence or score when available.
- Explanation log for recent strategy decisions.
- Signal markers on the candlestick chart.
- Strategy version/name display.

### Phase 3: Paper Trading

- Paper positions panel.
- Paper orders and fills table.
- Realized and unrealized P&L.
- Equity curve.
- Trade markers on charts.
- Exportable paper-trading ledger.

### Phase 4: Risk And Execution Controls

- Per-symbol enable/disable controls.
- Max position size display.
- Max daily loss display.
- Trading mode display: market-data, paper, or live.
- Live trading lock.
- Emergency stop / kill switch.
- Execution and risk decision log.

## Candlestick Chart Roadmap

The application will use TradingView Lightweight Charts as the charting layer.

### Initial Chart Features

- Candlestick series using normalized OHLCV data.
- Live candle updates from Coinbase market data.
- Appending completed candles as intervals close.
- Volume histogram pane.
- Crosshair readout for timestamp, open, high, low, close, and volume.
- Auto-scaling price axis.
- Follow-latest behavior with the ability to scroll back.

### Later Chart Features

- Strategy signal markers.
- Paper/live entry and exit markers.
- Stop-loss and risk-event markers.
- VWAP overlay.
- EMA/SMA overlays.
- Optional indicator panes such as RSI or MACD.

## Backend Roadmap

### Phase 1: Market Data Service

- Connect to Coinbase WebSocket.
- Subscribe to selected product IDs.
- Normalize incoming market data.
- Maintain rolling OHLCV candles.
- Expose real-time updates to the frontend.
- Track connection health, reconnects, and latency.

### Phase 2: Strategy Engine

- Evaluate strategy logic on normalized candle events.
- Emit structured strategy decisions.
- Keep features and labels causally aligned.
- Record decision explanations for auditability.
- Support a flat/no-trade default state.

### Phase 3: Paper Execution

- Simulate order submission and fills.
- Apply realistic fee and slippage assumptions.
- Maintain paper positions and balances.
- Produce an auditable order/fill ledger.
- Compare strategy results against simple benchmarks.

### Phase 4: Risk Engine

- Enforce max position size.
- Enforce max daily loss.
- Enforce per-symbol trading enablement.
- Enforce cooldowns after errors or loss limits.
- Block orders that fail validation.
- Emit risk decisions separately from strategy decisions.

### Phase 5: Coinbase Live Execution

- Add authenticated Coinbase API integration.
- Keep API keys outside source control.
- Submit and cancel orders only through the backend.
- Reconcile Coinbase orders, fills, balances, and local state.
- Keep live trading disabled unless explicitly enabled by configuration and UI controls.

## Safety And Compliance

- Educational only; not investment advice.
- No live trading in the initial build.
- No secrets in source control.
- No frontend access to Coinbase credentials.
- Backend must enforce all risk constraints before order submission.
- Live trading requires explicit opt-in, clear mode display, and emergency stop.

## Open Product Questions

- Which frontend framework should be used?
- Which Python web framework should be used?
- Should the backend expose WebSocket, Server-Sent Events, or both to the frontend?
- What strategy should be implemented first?
- What paper-trading fee and slippage assumptions should be used?
- Should historical candles come from Coinbase REST, local cache, or both?
- What persistence layer is appropriate for the audit/event ledger?
- What is the minimum acceptable test coverage before live trading code exists?
