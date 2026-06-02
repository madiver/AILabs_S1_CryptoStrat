from collections import deque
from threading import Lock
from typing import Iterable

from ailabs_crypto.models.constants import AuditCategory, ChartInterval, ProductId
from ailabs_crypto.models.market import AuditEvent


class AuditRecorder:
    def __init__(self, max_events: int = 500) -> None:
        self._events: deque[AuditEvent] = deque(maxlen=max_events)
        self._lock = Lock()

    def record(
        self,
        category: AuditCategory,
        action: str,
        *,
        product_id: ProductId | None = None,
        interval: ChartInterval | None = None,
        details: dict | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            category=category,
            action=action,
            product_id=product_id,
            interval=interval,
            details=details or {},
        )
        with self._lock:
            self._events.append(event)
        return event

    def list_events(self) -> list[AuditEvent]:
        with self._lock:
            return list(self._events)

    def actions(self) -> Iterable[str]:
        return (event.action for event in self.list_events())


audit_recorder = AuditRecorder()
