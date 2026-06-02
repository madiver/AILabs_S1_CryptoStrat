from enum import StrEnum


class ProductId(StrEnum):
    BTC_USD = "BTC-USD"
    ETH_USD = "ETH-USD"
    SOL_USD = "SOL-USD"


class ChartInterval(StrEnum):
    ONE_MINUTE = "1m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    ONE_HOUR = "1h"


class CoinbaseGranularity(StrEnum):
    ONE_MINUTE = "ONE_MINUTE"
    FIVE_MINUTE = "FIVE_MINUTE"
    FIFTEEN_MINUTE = "FIFTEEN_MINUTE"
    ONE_HOUR = "ONE_HOUR"


class Freshness(StrEnum):
    FRESH = "fresh"
    STALE = "stale"
    RECONNECTING = "reconnecting"
    OFFLINE = "offline"


class CandleSource(StrEnum):
    HISTORICAL = "historical"
    LIVE = "live"
    BACKFILL = "backfill"


class HistoryStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


class ConnectionScope(StrEnum):
    BACKEND = "backend"
    COINBASE = "coinbase"
    SYMBOL = "symbol"
    CHART = "chart"


class DashboardEventType(StrEnum):
    MARKET_SUMMARY = "market_summary"
    CANDLE_SNAPSHOT = "candle_snapshot"
    CANDLE_UPDATE = "candle_update"
    CONNECTION_STATE = "connection_state"
    ERROR = "error"


class AuditCategory(StrEnum):
    CONNECTION = "connection"
    MARKET_DATA = "market_data"
    SELECTION = "selection"
    BACKFILL = "backfill"
    SAFETY = "safety"


SUPPORTED_SYMBOLS = {
    ProductId.BTC_USD: ("BTC", "USD", "BTC-USD"),
    ProductId.ETH_USD: ("ETH", "USD", "ETH-USD"),
    ProductId.SOL_USD: ("SOL", "USD", "SOL-USD"),
}

INTERVAL_SECONDS = {
    ChartInterval.ONE_MINUTE: 60,
    ChartInterval.FIVE_MINUTE: 300,
    ChartInterval.FIFTEEN_MINUTE: 900,
    ChartInterval.ONE_HOUR: 3600,
}

COINBASE_GRANULARITIES = {
    ChartInterval.ONE_MINUTE: CoinbaseGranularity.ONE_MINUTE,
    ChartInterval.FIVE_MINUTE: CoinbaseGranularity.FIVE_MINUTE,
    ChartInterval.FIFTEEN_MINUTE: CoinbaseGranularity.FIFTEEN_MINUTE,
    ChartInterval.ONE_HOUR: CoinbaseGranularity.ONE_HOUR,
}

STALE_AFTER_SECONDS = 15
DEFAULT_CANDLE_LIMIT = 100
MAX_CANDLE_LIMIT = 350
MARKET_DATA_MODE = "market-data-only"
