# Data Model: Phase 1 Market Dashboard

## MarketSymbol

Represents one supported Coinbase product displayed in the dashboard.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `product_id` | string | yes | One of `BTC-USD`, `ETH-USD`, `SOL-USD` |
| `base_currency` | string | yes | `BTC`, `ETH`, or `SOL` |
| `quote_currency` | string | yes | `USD` |
| `display_name` | string | yes | Human-readable label |
| `enabled` | boolean | yes | Always true for Phase 1 supported products |

**Relationships**: One `MarketSymbol` has many `Candle` records per interval and one
current `MarketSummary`.

**Validation rules**:

- Reject unsupported `product_id` values.
- Treat product IDs as case-sensitive canonical identifiers.

## ChartInterval

Represents the user-selected candle interval.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | string | yes | One of `1m`, `5m`, `15m`, `1h` |
| `seconds` | integer | yes | 60, 300, 900, or 3600 |
| `coinbase_granularity` | string | yes | `ONE_MINUTE`, `FIVE_MINUTE`, `FIFTEEN_MINUTE`, `ONE_HOUR` |

**Relationships**: Each `Candle` belongs to exactly one interval.

**Validation rules**:

- Reject unsupported interval values.
- Always request at least 100 candles for the selected interval when data is available.

## MarketSummary

Represents the market tile state for a symbol.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `product_id` | string | yes | Supported product ID |
| `price` | decimal string | yes | Current quote price |
| `price_change_24h_percent` | decimal string | yes | 24-hour percentage change |
| `last_update_at` | RFC3339 timestamp | yes | Last accepted market update |
| `freshness` | enum | yes | `fresh`, `stale`, `reconnecting`, `offline` |

**Relationships**: One summary per supported symbol.

**Validation rules**:

- Mark stale when 15 seconds pass without a fresh update.
- Preserve last known values when stale, reconnecting, or offline.
- Never present stale values as current.

## Candle

Represents OHLCV data for a product and interval.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `product_id` | string | yes | Supported product ID |
| `interval` | string | yes | Supported chart interval |
| `time` | UNIX seconds | yes | Candle bucket start time |
| `open` | decimal string | yes | First trade price in bucket |
| `high` | decimal string | yes | Highest price in bucket |
| `low` | decimal string | yes | Lowest price in bucket |
| `close` | decimal string | yes | Last trade price in bucket |
| `volume` | decimal string or null | yes | Base asset volume; null when unavailable |
| `complete` | boolean | yes | False for current in-progress candle |
| `source` | enum | yes | `historical`, `live`, or `backfill` |

**Relationships**: Belongs to one `MarketSymbol` and one `ChartInterval`.

**Validation rules**:

- Candle time must align to interval boundaries.
- `high` must be greater than or equal to `open`, `low`, and `close`.
- `low` must be less than or equal to `open`, `high`, and `close`.
- Volume may be zero or unavailable but must not be negative when present.
- Initial chart response must include at least 100 candles when market data is available;
  otherwise the chart response must explicitly report partial or unavailable history.

## ConnectionState

Represents backend-to-Coinbase and frontend-to-backend market-data health.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `status` | enum | yes | `healthy`, `stale`, `reconnecting`, `offline` |
| `scope` | enum | yes | `backend`, `coinbase`, `symbol`, or `chart` |
| `product_id` | string | no | Present for symbol/chart scoped states |
| `interval` | string | no | Present for chart scoped states |
| `last_update_at` | RFC3339 timestamp | no | Last fresh update |
| `last_heartbeat_at` | RFC3339 timestamp | no | Last heartbeat if available |
| `reason` | string | no | Short user-safe explanation |

### State Transitions

```text
offline -> reconnecting -> healthy
healthy -> stale -> reconnecting
healthy -> offline
reconnecting -> offline
reconnecting -> healthy only after missed candles are backfilled
```

**Validation rules**:

- `healthy` requires current data and no known missing candle gap.
- `stale` starts after 15 seconds without a fresh update.
- `reconnecting` must not imply values are current.
- `offline` must not expose trading controls.

## DashboardEvent

Represents UI-consumable events sent from backend to frontend.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `type` | enum | yes | `market_summary`, `candle_snapshot`, `candle_update`, `connection_state`, `error` |
| `event_id` | string | yes | Unique event identifier |
| `occurred_at` | RFC3339 timestamp | yes | Backend event timestamp |
| `payload` | object | yes | Event-specific object |

**Validation rules**:

- Unsupported event types must be ignored by the frontend without breaking the session.
- Events must be safe for display and contain no credentials or private account data.

## AuditEvent

Represents structured auditability for Phase 1 runtime decisions.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `event_id` | string | yes | Unique event identifier |
| `occurred_at` | RFC3339 timestamp | yes | Backend timestamp |
| `category` | enum | yes | `connection`, `market_data`, `selection`, `backfill`, `safety` |
| `action` | string | yes | Example: `marked_stale`, `backfill_started`, `backfill_completed` |
| `product_id` | string | no | Symbol when relevant |
| `interval` | string | no | Interval when relevant |
| `details` | object | no | Non-sensitive context |

**Validation rules**:

- Do not include secrets, account IDs, balances, order IDs, or private URLs.
- Emit events for stale transitions, reconnect attempts, backfill completion, symbol
  selection, interval selection, and market-data-only safety checks.
