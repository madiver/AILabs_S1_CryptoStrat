import pytest

from ailabs_crypto.api.app import create_app
from ailabs_crypto.market_data.backfill import BackfillCoordinator
from ailabs_crypto.market_data.connection_state import ConnectionStateMachine
from ailabs_crypto.models.constants import AuditCategory, CandleSource, ChartInterval, Freshness, ProductId
from ailabs_crypto.models.market import Candle, CandleSnapshot
from ailabs_crypto.runtime.audit import AuditRecorder


class FakeCandleService:
    async def get_snapshot(self, product_id: ProductId, interval: ChartInterval, limit: int = 100, *, source=CandleSource.HISTORICAL):
        return CandleSnapshot(
            product_id=product_id,
            interval=interval,
            freshness=Freshness.FRESH,
            history_status="partial",
            candles=[
                Candle(
                    product_id=product_id,
                    interval=interval,
                    time=1,
                    open="1",
                    high="1",
                    low="1",
                    close="1",
                    volume="1",
                    complete=True,
                    source=source,
                )
            ],
        )


@pytest.mark.asyncio
async def test_required_runtime_audit_events_are_emitted() -> None:
    recorder = AuditRecorder()
    machine = ConnectionStateMachine(recorder=recorder)
    coordinator = BackfillCoordinator(
        candle_service=FakeCandleService(),
        state_machine=machine,
        recorder=recorder,
    )

    machine.mark_healthy(product_id=ProductId.BTC_USD)
    machine.mark_stale(product_id=ProductId.BTC_USD)
    machine.mark_reconnecting(product_id=ProductId.BTC_USD)
    machine.mark_offline()
    await coordinator.backfill_before_healthy(ProductId.BTC_USD, ChartInterval.ONE_MINUTE)
    recorder.record(AuditCategory.SELECTION, "symbol_selected", product_id=ProductId.BTC_USD)
    recorder.record(AuditCategory.SELECTION, "interval_selected", product_id=ProductId.BTC_USD, interval=ChartInterval.ONE_MINUTE)
    recorder.record(AuditCategory.SAFETY, "market_data_only_safety_check")

    actions = set(recorder.actions())

    assert {
        "marked_stale",
        "reconnect_attempted",
        "backfill_completed",
        "marked_offline",
        "symbol_selected",
        "interval_selected",
        "market_data_only_safety_check",
    }.issubset(actions)


def test_app_startup_records_market_data_only_safety_event() -> None:
    app = create_app()

    assert app.state.settings.trading_enabled is False
