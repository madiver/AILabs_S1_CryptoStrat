from ailabs_crypto.market_data.candle_service import CandleService
from ailabs_crypto.market_data.connection_state import ConnectionStateMachine
from ailabs_crypto.models.constants import AuditCategory, CandleSource, ChartInterval, ProductId
from ailabs_crypto.models.market import CandleSnapshot
from ailabs_crypto.runtime.audit import AuditRecorder, audit_recorder


class BackfillCoordinator:
    def __init__(
        self,
        candle_service: CandleService | None = None,
        state_machine: ConnectionStateMachine | None = None,
        recorder: AuditRecorder = audit_recorder,
    ) -> None:
        self.candle_service = candle_service or CandleService()
        self.state_machine = state_machine or ConnectionStateMachine(recorder=recorder)
        self.recorder = recorder

    async def backfill_before_healthy(
        self,
        product_id: ProductId,
        interval: ChartInterval,
        limit: int = 100,
    ) -> CandleSnapshot:
        self.state_machine.mark_reconnecting(product_id=product_id, interval=interval)
        self.recorder.record(AuditCategory.BACKFILL, "backfill_started", product_id=product_id, interval=interval)
        snapshot = await self.candle_service.get_snapshot(
            product_id,
            interval,
            limit=limit,
            source=CandleSource.BACKFILL,
        )
        self.recorder.record(
            AuditCategory.BACKFILL,
            "backfill_completed",
            product_id=product_id,
            interval=interval,
            details={"count": len(snapshot.candles), "history_status": snapshot.history_status},
        )
        if snapshot.candles:
            self.state_machine.mark_healthy(product_id=product_id, interval=interval, reason="backfill completed")
        return snapshot
