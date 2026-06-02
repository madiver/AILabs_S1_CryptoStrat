from datetime import datetime, timedelta, timezone

from ailabs_crypto.market_data.connection_state import ConnectionStateMachine
from ailabs_crypto.models.constants import Freshness, ProductId
from ailabs_crypto.runtime.audit import AuditRecorder


def test_stale_detection_after_15_seconds() -> None:
    machine = ConnectionStateMachine(recorder=AuditRecorder(), stale_after_seconds=15)
    state = machine.mark_healthy(product_id=ProductId.BTC_USD)

    stale = machine.evaluate_staleness(state.last_update_at + timedelta(seconds=15))

    assert stale.status == Freshness.STALE


def test_reconnecting_and_offline_transitions_record_audit_events() -> None:
    recorder = AuditRecorder()
    machine = ConnectionStateMachine(recorder=recorder)

    machine.mark_reconnecting(product_id=ProductId.BTC_USD)
    machine.mark_offline()

    assert "reconnect_attempted" in list(recorder.actions())
    assert "marked_offline" in list(recorder.actions())
