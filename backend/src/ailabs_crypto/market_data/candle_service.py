from ailabs_crypto.market_data.coinbase_client import CoinbasePublicClient
from ailabs_crypto.models.constants import (
    AuditCategory,
    CandleSource,
    ChartInterval,
    DEFAULT_CANDLE_LIMIT,
    Freshness,
    HistoryStatus,
    ProductId,
)
from ailabs_crypto.models.market import Candle, CandleSnapshot
from ailabs_crypto.runtime.audit import AuditRecorder, audit_recorder


class CandleService:
    def __init__(
        self,
        client: CoinbasePublicClient | None = None,
        recorder: AuditRecorder = audit_recorder,
    ) -> None:
        self.client = client or CoinbasePublicClient()
        self.recorder = recorder

    async def get_snapshot(
        self,
        product_id: ProductId,
        interval: ChartInterval,
        limit: int = DEFAULT_CANDLE_LIMIT,
        *,
        source: CandleSource = CandleSource.HISTORICAL,
    ) -> CandleSnapshot:
        try:
            candles = await self.client.get_candles(product_id, interval, limit)
            tagged = [candle.model_copy(update={"source": source}) for candle in candles]
            snapshot = self.snapshot_from_candles(product_id, interval, tagged, expected_count=limit)
            self.recorder.record(
                AuditCategory.MARKET_DATA,
                "candles_loaded",
                product_id=product_id,
                interval=interval,
                details={"count": len(snapshot.candles), "history_status": snapshot.history_status},
            )
            return snapshot
        except Exception as exc:
            self.recorder.record(
                AuditCategory.MARKET_DATA,
                "candles_unavailable",
                product_id=product_id,
                interval=interval,
                details={"error": exc.__class__.__name__},
            )
            return CandleSnapshot(
                product_id=product_id,
                interval=interval,
                freshness=Freshness.OFFLINE,
                history_status=HistoryStatus.UNAVAILABLE,
                candles=[],
            )

    @staticmethod
    def snapshot_from_candles(
        product_id: ProductId,
        interval: ChartInterval,
        candles: list[Candle],
        *,
        expected_count: int = DEFAULT_CANDLE_LIMIT,
    ) -> CandleSnapshot:
        sorted_candles = sorted(candles, key=lambda candle: candle.time)
        if len(sorted_candles) >= expected_count:
            status = HistoryStatus.COMPLETE
            freshness = Freshness.FRESH
        elif sorted_candles:
            status = HistoryStatus.PARTIAL
            freshness = Freshness.STALE
        else:
            status = HistoryStatus.UNAVAILABLE
            freshness = Freshness.OFFLINE
        return CandleSnapshot(
            product_id=product_id,
            interval=interval,
            freshness=freshness,
            history_status=status,
            candles=sorted_candles,
        )
