from fastapi import HTTPException

from ailabs_crypto.models.constants import (
    COINBASE_GRANULARITIES,
    INTERVAL_SECONDS,
    SUPPORTED_SYMBOLS,
    ChartInterval,
    ProductId,
)
from ailabs_crypto.models.market import MarketSymbol


def list_supported_symbols() -> list[MarketSymbol]:
    return [
        MarketSymbol(
            product_id=product_id,
            base_currency=base_currency,
            quote_currency=quote_currency,
            display_name=display_name,
            enabled=True,
        )
        for product_id, (base_currency, quote_currency, display_name) in SUPPORTED_SYMBOLS.items()
    ]


def validate_symbol(value: str) -> ProductId:
    try:
        product_id = ProductId(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Unsupported symbol: {value}") from exc
    if product_id not in SUPPORTED_SYMBOLS:
        raise HTTPException(status_code=400, detail=f"Unsupported symbol: {value}")
    return product_id


def validate_interval(value: str) -> ChartInterval:
    try:
        interval = ChartInterval(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Unsupported interval: {value}") from exc
    if interval not in INTERVAL_SECONDS:
        raise HTTPException(status_code=400, detail=f"Unsupported interval: {value}")
    return interval


def interval_seconds(interval: ChartInterval) -> int:
    return INTERVAL_SECONDS[interval]


def coinbase_granularity(interval: ChartInterval) -> str:
    return COINBASE_GRANULARITIES[interval].value
