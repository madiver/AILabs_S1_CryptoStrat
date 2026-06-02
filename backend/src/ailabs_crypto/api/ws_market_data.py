from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ailabs_crypto.market_data.backfill import BackfillCoordinator
from ailabs_crypto.market_data.catalog import validate_interval, validate_symbol
from ailabs_crypto.market_data.connection_state import ConnectionStateMachine
from ailabs_crypto.market_data.summary_service import MarketSummaryService
from ailabs_crypto.models.constants import AuditCategory, DashboardEventType
from ailabs_crypto.models.market import DashboardEvent
from ailabs_crypto.runtime.audit import audit_recorder

router = APIRouter()
summary_service = MarketSummaryService()
backfill = BackfillCoordinator()
state_machine = ConnectionStateMachine()


def event(event_type: DashboardEventType, payload: dict) -> dict:
    return DashboardEvent(type=event_type, payload=payload).model_dump(mode="json")


@router.websocket("/ws/market-data")
async def market_data_socket(websocket: WebSocket) -> None:
    await websocket.accept()
    state = state_machine.mark_healthy(reason="frontend connected to backend")
    await websocket.send_json(event(DashboardEventType.CONNECTION_STATE, state.model_dump(mode="json")))
    try:
        while True:
            message = await websocket.receive_json()
            if message.get("type") == "subscribe":
                summaries = await summary_service.get_summaries()
                for summary in summaries:
                    await websocket.send_json(event(DashboardEventType.MARKET_SUMMARY, summary.model_dump(mode="json")))
                product_id = validate_symbol(message.get("active_symbol", "BTC-USD"))
                interval = validate_interval(message.get("active_interval", "1m"))
                audit_recorder.record(AuditCategory.SELECTION, "symbol_selected", product_id=product_id)
                audit_recorder.record(AuditCategory.SELECTION, "interval_selected", product_id=product_id, interval=interval)
                snapshot = await backfill.candle_service.get_snapshot(product_id, interval)
                await websocket.send_json(event(DashboardEventType.CANDLE_SNAPSHOT, snapshot.model_dump(mode="json")))
            elif message.get("type") == "set_active_chart":
                product_id = validate_symbol(message.get("symbol", "BTC-USD"))
                interval = validate_interval(message.get("interval", "1m"))
                audit_recorder.record(AuditCategory.SELECTION, "symbol_selected", product_id=product_id)
                audit_recorder.record(AuditCategory.SELECTION, "interval_selected", product_id=product_id, interval=interval)
                snapshot = await backfill.backfill_before_healthy(product_id, interval)
                await websocket.send_json(event(DashboardEventType.CANDLE_SNAPSHOT, snapshot.model_dump(mode="json")))
                await websocket.send_json(event(DashboardEventType.CONNECTION_STATE, state_machine.state.model_dump(mode="json")))
            else:
                await websocket.send_json(
                    event(
                        DashboardEventType.ERROR,
                        {"code": "unsupported_message", "message": "Unsupported market data message."},
                    )
                )
    except WebSocketDisconnect:
        state_machine.mark_offline("frontend disconnected")
