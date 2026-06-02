from fastapi.testclient import TestClient

from ailabs_crypto.api.app import create_app


def test_symbols_contract_lists_phase_one_products() -> None:
    client = TestClient(create_app())

    response = client.get("/api/symbols")

    assert response.status_code == 200
    symbols = response.json()["symbols"]
    assert [symbol["product_id"] for symbol in symbols] == ["BTC-USD", "ETH-USD", "SOL-USD"]
    assert all(symbol["enabled"] for symbol in symbols)


def test_market_summary_contract_contains_mode_and_tile_fields() -> None:
    client = TestClient(create_app())

    response = client.get("/api/markets/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "market-data-only"
    assert len(body["summaries"]) == 3
    for summary in body["summaries"]:
        assert summary["product_id"] in {"BTC-USD", "ETH-USD", "SOL-USD"}
        assert "price" in summary
        assert "price_change_24h_percent" in summary
        assert "last_update_at" in summary
        assert summary["freshness"] in {"fresh", "stale", "reconnecting", "offline"}
