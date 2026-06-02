from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from ailabs_crypto.market_data.catalog import coinbase_granularity, interval_seconds
from ailabs_crypto.models.constants import (
    CandleSource,
    ChartInterval,
    Freshness,
    ProductId,
)
from ailabs_crypto.models.market import Candle, MarketSummary
from ailabs_crypto.runtime.settings import settings


class CoinbasePublicClient:
    def __init__(self, base_url: str = settings.coinbase_rest_url, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get_product_summary(self, product_id: ProductId) -> MarketSummary:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/market/products/{product_id.value}")
            response.raise_for_status()
            return self.parse_product_summary(response.json())

    async def get_candles(
        self,
        product_id: ProductId,
        interval: ChartInterval,
        limit: int,
    ) -> list[Candle]:
        seconds = interval_seconds(interval)
        end = int(datetime.now(timezone.utc).timestamp())
        start = end - (limit * seconds)
        params = {
            "start": str(start),
            "end": str(end),
            "granularity": coinbase_granularity(interval),
            "limit": str(limit),
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/market/products/{product_id.value}/candles",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()
        candles = [self.parse_candle(product_id, interval, row) for row in payload.get("candles", [])]
        return sorted(candles, key=lambda candle: candle.time)

    @staticmethod
    def parse_product_summary(payload: dict[str, Any]) -> MarketSummary:
        product_id = ProductId(payload["product_id"])
        return MarketSummary(
            product_id=product_id,
            price=str(payload.get("price") or "0"),
            price_change_24h_percent=str(payload.get("price_percentage_change_24h") or "0"),
            last_update_at=datetime.now(timezone.utc),
            freshness=Freshness.FRESH,
        )

    @staticmethod
    def parse_candle(product_id: ProductId, interval: ChartInterval, payload: dict[str, Any]) -> Candle:
        return Candle(
            product_id=product_id,
            interval=interval,
            time=int(payload["start"]),
            open=str(payload["open"]),
            high=str(payload["high"]),
            low=str(payload["low"]),
            close=str(payload["close"]),
            volume=str(payload["volume"]) if payload.get("volume") is not None else None,
            complete=True,
            source=CandleSource.HISTORICAL,
        )
