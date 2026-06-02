from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ailabs_crypto.models.constants import (
    AuditCategory,
    CandleSource,
    ChartInterval,
    ConnectionScope,
    DashboardEventType,
    Freshness,
    HistoryStatus,
    MARKET_DATA_MODE,
    ProductId,
)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MarketSymbol(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    product_id: ProductId
    base_currency: str
    quote_currency: str = "USD"
    display_name: str
    enabled: bool = True


class MarketSummary(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    product_id: ProductId
    price: str
    price_change_24h_percent: str
    last_update_at: datetime
    freshness: Freshness


class Candle(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    product_id: ProductId
    interval: ChartInterval
    time: int
    open: str
    high: str
    low: str
    close: str
    volume: str | None
    complete: bool
    source: CandleSource

    @field_validator("open", "high", "low", "close", "volume")
    @classmethod
    def validate_decimal_string(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            number = float(value)
        except ValueError as exc:
            raise ValueError("must be a decimal string") from exc
        if number < 0:
            raise ValueError("must not be negative")
        return value

    @model_validator(mode="after")
    def validate_ohlc(self) -> "Candle":
        high = float(self.high)
        low = float(self.low)
        open_price = float(self.open)
        close = float(self.close)
        if high < max(open_price, low, close):
            raise ValueError("high must be >= open, low, and close")
        if low > min(open_price, high, close):
            raise ValueError("low must be <= open, high, and close")
        return self


class CandleSnapshot(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    product_id: ProductId
    interval: ChartInterval
    freshness: Freshness
    history_status: HistoryStatus
    candles: list[Candle]


class ConnectionState(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    status: Freshness
    scope: ConnectionScope
    product_id: ProductId | None = None
    interval: ChartInterval | None = None
    last_update_at: datetime | None = None
    last_heartbeat_at: datetime | None = None
    reason: str | None = None


class DashboardEvent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    type: DashboardEventType
    event_id: str = Field(default_factory=lambda: f"evt_{uuid4().hex}")
    occurred_at: datetime = Field(default_factory=utc_now)
    payload: dict[str, Any]


class AuditEvent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    event_id: str = Field(default_factory=lambda: f"audit_{uuid4().hex}")
    occurred_at: datetime = Field(default_factory=utc_now)
    category: AuditCategory
    action: str
    product_id: ProductId | None = None
    interval: ChartInterval | None = None
    details: dict[str, Any] | None = None


class HealthResponse(BaseModel):
    mode: str = MARKET_DATA_MODE
    backend_status: Freshness
    trading_enabled: bool = False
    generated_at: datetime = Field(default_factory=utc_now)


class ErrorResponse(BaseModel):
    error: str
    message: str
