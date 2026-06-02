from fastapi import APIRouter, Query

from ailabs_crypto.market_data.catalog import list_supported_symbols, validate_interval, validate_symbol
from ailabs_crypto.market_data.candle_service import CandleService
from ailabs_crypto.market_data.summary_service import MarketSummaryService
from ailabs_crypto.models.constants import DEFAULT_CANDLE_LIMIT, MARKET_DATA_MODE, MAX_CANDLE_LIMIT

router = APIRouter()
summary_service = MarketSummaryService()
candle_service = CandleService()


@router.get("/api/symbols")
async def get_symbols() -> dict:
    return {"symbols": list_supported_symbols()}


@router.get("/api/markets/summary")
async def get_market_summaries() -> dict:
    return {"mode": MARKET_DATA_MODE, "summaries": await summary_service.get_summaries()}


@router.get("/api/candles")
async def get_candles(
    symbol: str,
    interval: str,
    limit: int = Query(DEFAULT_CANDLE_LIMIT, ge=DEFAULT_CANDLE_LIMIT, le=MAX_CANDLE_LIMIT),
):
    product_id = validate_symbol(symbol)
    chart_interval = validate_interval(interval)
    return await candle_service.get_snapshot(product_id, chart_interval, limit=limit)
