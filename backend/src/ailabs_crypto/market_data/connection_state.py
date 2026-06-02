from datetime import datetime, timezone

from ailabs_crypto.models.constants import AuditCategory, ChartInterval, ConnectionScope, Freshness, ProductId
from ailabs_crypto.models.market import ConnectionState
from ailabs_crypto.runtime.audit import AuditRecorder, audit_recorder
from ailabs_crypto.runtime.settings import settings


class ConnectionStateMachine:
    def __init__(self, recorder: AuditRecorder = audit_recorder, stale_after_seconds: int = settings.stale_after_seconds) -> None:
        self.recorder = recorder
        self.stale_after_seconds = stale_after_seconds
        self.state = ConnectionState(
            status=Freshness.OFFLINE,
            scope=ConnectionScope.COINBASE,
            reason="market data not connected",
        )

    def mark_healthy(
        self,
        *,
        product_id: ProductId | None = None,
        interval: ChartInterval | None = None,
        reason: str = "fresh market data received",
    ) -> ConnectionState:
        self.state = ConnectionState(
            status=Freshness.FRESH,
            scope=ConnectionScope.CHART if interval else ConnectionScope.COINBASE,
            product_id=product_id,
            interval=interval,
            last_update_at=datetime.now(timezone.utc),
            last_heartbeat_at=datetime.now(timezone.utc),
            reason=reason,
        )
        self.recorder.record(AuditCategory.CONNECTION, "marked_healthy", product_id=product_id, interval=interval)
        return self.state

    def mark_stale(self, *, product_id: ProductId | None = None, interval: ChartInterval | None = None) -> ConnectionState:
        self.state = self.state.model_copy(
            update={
                "status": Freshness.STALE,
                "scope": ConnectionScope.CHART if interval else ConnectionScope.SYMBOL,
                "product_id": product_id,
                "interval": interval,
                "reason": "no fresh update within stale threshold",
            }
        )
        self.recorder.record(AuditCategory.CONNECTION, "marked_stale", product_id=product_id, interval=interval)
        return self.state

    def mark_reconnecting(self, *, product_id: ProductId | None = None, interval: ChartInterval | None = None) -> ConnectionState:
        self.state = self.state.model_copy(
            update={
                "status": Freshness.RECONNECTING,
                "scope": ConnectionScope.CHART if interval else ConnectionScope.COINBASE,
                "product_id": product_id,
                "interval": interval,
                "reason": "reconnecting to market data",
            }
        )
        self.recorder.record(AuditCategory.CONNECTION, "reconnect_attempted", product_id=product_id, interval=interval)
        return self.state

    def mark_offline(self, reason: str = "market data unavailable") -> ConnectionState:
        self.state = self.state.model_copy(
            update={"status": Freshness.OFFLINE, "scope": ConnectionScope.COINBASE, "reason": reason}
        )
        self.recorder.record(AuditCategory.CONNECTION, "marked_offline", details={"reason": reason})
        return self.state

    def evaluate_staleness(self, now: datetime | None = None) -> ConnectionState:
        current_time = now or datetime.now(timezone.utc)
        if self.state.last_update_at is None:
            return self.mark_offline("no market update received")
        elapsed = (current_time - self.state.last_update_at).total_seconds()
        if elapsed >= self.stale_after_seconds and self.state.status == Freshness.FRESH:
            return self.mark_stale(product_id=self.state.product_id, interval=self.state.interval)
        return self.state
