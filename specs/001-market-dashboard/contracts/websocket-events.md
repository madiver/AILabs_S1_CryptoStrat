# WebSocket Events Contract

Backend endpoint: `ws://localhost:8000/ws/market-data`

The frontend connects to the backend only. It never connects directly to Coinbase and
never sends credentials.

## Client Messages

### Subscribe

```json
{
  "type": "subscribe",
  "symbols": ["BTC-USD", "ETH-USD", "SOL-USD"],
  "active_symbol": "BTC-USD",
  "active_interval": "1m"
}
```

### Set Active Chart

```json
{
  "type": "set_active_chart",
  "symbol": "ETH-USD",
  "interval": "5m"
}
```

## Server Events

All server events share this envelope:

```json
{
  "type": "connection_state",
  "event_id": "evt_01",
  "occurred_at": "2026-06-02T12:00:00Z",
  "payload": {}
}
```

Unknown event types must be ignored by the frontend without closing the connection.

### connection_state

```json
{
  "type": "connection_state",
  "event_id": "evt_01",
  "occurred_at": "2026-06-02T12:00:00Z",
  "payload": {
    "status": "healthy",
    "scope": "coinbase",
    "product_id": "BTC-USD",
    "interval": "1m",
    "last_update_at": "2026-06-02T12:00:00Z",
    "reason": "fresh market data received"
  }
}
```

`status` is one of `healthy`, `stale`, `reconnecting`, or `offline`.

### market_summary

```json
{
  "type": "market_summary",
  "event_id": "evt_02",
  "occurred_at": "2026-06-02T12:00:00Z",
  "payload": {
    "product_id": "BTC-USD",
    "price": "68450.12",
    "price_change_24h_percent": "2.13%",
    "last_update_at": "2026-06-02T12:00:00Z",
    "freshness": "fresh"
  }
}
```

### candle_snapshot

Sent after initial load, active chart change, or reconnect backfill.

```json
{
  "type": "candle_snapshot",
  "event_id": "evt_03",
  "occurred_at": "2026-06-02T12:00:00Z",
  "payload": {
    "product_id": "BTC-USD",
    "interval": "1m",
    "freshness": "fresh",
    "history_status": "complete",
    "candles": [
      {
        "product_id": "BTC-USD",
        "interval": "1m",
        "time": 1780401540,
        "open": "68420.00",
        "high": "68480.00",
        "low": "68410.00",
        "close": "68450.12",
        "volume": "12.345",
        "complete": true,
        "source": "historical"
      }
    ]
  }
}
```

`history_status` is `complete`, `partial`, or `unavailable`. A complete snapshot must
contain at least 100 candles when market data is available; partial or unavailable
snapshots preserve chart context while clearly indicating limited history.

### candle_update

Sent for the active chart after the backend normalizes a live or backfilled candle.

```json
{
  "type": "candle_update",
  "event_id": "evt_04",
  "occurred_at": "2026-06-02T12:00:01Z",
  "payload": {
    "product_id": "BTC-USD",
    "interval": "1m",
    "candle": {
      "product_id": "BTC-USD",
      "interval": "1m",
      "time": 1780401600,
      "open": "68450.12",
      "high": "68460.00",
      "low": "68430.00",
      "close": "68455.00",
      "volume": "0.456",
      "complete": false,
      "source": "live"
    }
  }
}
```

### error

Errors must be user-safe and must not include credentials, private URLs, or account data.

```json
{
  "type": "error",
  "event_id": "evt_05",
  "occurred_at": "2026-06-02T12:00:01Z",
  "payload": {
    "code": "market_data_unavailable",
    "message": "Market data is temporarily unavailable for BTC-USD."
  }
}
```

## Reconnect And Backfill Rules

- If 15 seconds pass without a fresh update for a symbol or active chart, send
  `connection_state` with `status: "stale"`.
- During reconnect, send `connection_state` with `status: "reconnecting"`.
- If candles were missed, send a `candle_snapshot` or ordered `candle_update` events
  with `source: "backfill"`.
- Do not send `status: "healthy"` for the affected symbol/interval until missed candles
  are backfilled.
- If reconnect fails, send `status: "offline"` and preserve last known market values.
