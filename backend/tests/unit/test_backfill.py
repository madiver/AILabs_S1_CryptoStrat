import pytest

from ailabs_crypto.market_data.backfill import BackfillCoordinator
from ailabs_crypto.market_data.connection_state import ConnectionStateMachine
from ailabs_crypto.models.constants import CandleSource, ChartInterval, Freshness, ProductId
from ailabs_crypto.models.market import Candle, CandleSnapshot
from ailabs_crypto.runtime.audit import AuditRecorder


class FakeCandleService:
    async def get_snapshot(self, product_id: ProductId, interval: ChartInterval, limit: int = 100, *, source=CandleSource.HISTORICAL):
        candle = Candle(
            product_id=product_id,
            interval=interval,
            time=1_780_401_000,
            open="100",
            high="101",
            low="99",
            close="100",
            volume="1",
            complete=True,
            source=source,
        )
        return CandleSnapshot(
            product_id=product_id,
            interval=interval,
            freshness=Freshness.FRESH,
            history_status="partial",
            candles=[candle],
        )


@pytest.mark.asyncio
async def test_backfill_completes_before_healthy_state() -> None:
    recorder = AuditRecorder()
    machine = ConnectionStateMachine(recorder=recorder)
    coordinator = BackfillCoordinator(
        candle_service=FakeCandleService(),
        state_machine=machine,
        recorder=recorder,
    )

    snapshot = await coordinator.backfill_before_healthy(ProductId.BTC_USD, ChartInterval.ONE_MINUTE)

    assert snapshot.candles[0].source == CandleSource.BACKFILL
    assert machine.state.status == Freshness.FRESH
    assert list(recorder.actions()).index("backfill_completed") < list(recorder.actions()).index("marked_healthy")
