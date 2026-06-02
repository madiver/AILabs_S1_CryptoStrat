from fastapi.testclient import TestClient

from ailabs_crypto.api.app import create_app


def test_market_websocket_contract_emits_connection_summary_and_snapshot() -> None:
    client = TestClient(create_app())

    with client.websocket_connect("/ws/market-data") as websocket:
        first = websocket.receive_json()
        assert first["type"] == "connection_state"

        websocket.send_json({
            "type": "subscribe",
            "symbols": ["BTC-USD", "ETH-USD", "SOL-USD"],
            "active_symbol": "BTC-USD",
            "active_interval": "1m",
        })

        event_types = {websocket.receive_json()["type"] for _ in range(4)}
        assert "market_summary" in event_types
        assert "candle_snapshot" in event_types
