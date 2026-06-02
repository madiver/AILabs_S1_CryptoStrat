from fastapi.testclient import TestClient

import ailabs_crypto.api.routes_market as routes_market
from ailabs_crypto.api.app import create_app
from ailabs_crypto.models.constants import CandleSource, ChartInterval, Freshness, HistoryStatus, ProductId
from ailabs_crypto.models.market import Candle, CandleSnapshot


def make_candles(count: int) -> list[Candle]:
    return [
        Candle(
            product_id=ProductId.BTC_USD,
            interval=ChartInterval.ONE_MINUTE,
            time=1_780_401_000 + (idx * 60),
            open="100",
            high="105",
            low="95",
            close="101",
            volume="10",
            complete=True,
            source=CandleSource.HISTORICAL,
        )
        for idx in range(count)
    ]


class FakeCandleService:
    def __init__(self, count: int) -> None:
        self.count = count

    async def get_snapshot(self, product_id: ProductId, interval: ChartInterval, limit: int) -> CandleSnapshot:
        candles = make_candles(self.count)
        history_status = HistoryStatus.COMPLETE if self.count >= 100 else HistoryStatus.PARTIAL
        freshness = Freshness.FRESH if history_status == HistoryStatus.COMPLETE else Freshness.STALE
        return CandleSnapshot(
            product_id=product_id,
            interval=interval,
            freshness=freshness,
            history_status=history_status,
            candles=candles,
        )


class UnavailableCandleService:
    async def get_snapshot(self, product_id: ProductId, interval: ChartInterval, limit: int) -> CandleSnapshot:
        return CandleSnapshot(
            product_id=product_id,
            interval=interval,
            freshness=Freshness.OFFLINE,
            history_status=HistoryStatus.UNAVAILABLE,
            candles=[],
        )


def test_candles_contract_complete_history(monkeypatch) -> None:
    monkeypatch.setattr(routes_market, "candle_service", FakeCandleService(100))
    client = TestClient(create_app())

    response = client.get("/api/candles?symbol=BTC-USD&interval=1m&limit=100")

    assert response.status_code == 200
    body = response.json()
    assert body["history_status"] == "complete"
    assert len(body["candles"]) == 100


def test_candles_contract_partial_history(monkeypatch) -> None:
    monkeypatch.setattr(routes_market, "candle_service", FakeCandleService(12))
    client = TestClient(create_app())

    response = client.get("/api/candles?symbol=BTC-USD&interval=1m&limit=100")

    assert response.status_code == 200
    assert response.json()["history_status"] == "partial"


def test_candles_contract_unavailable_history(monkeypatch) -> None:
    monkeypatch.setattr(routes_market, "candle_service", UnavailableCandleService())
    client = TestClient(create_app())

    response = client.get("/api/candles?symbol=BTC-USD&interval=1m&limit=100")

    assert response.status_code == 200
    body = response.json()
    assert body["history_status"] == "unavailable"
    assert body["candles"] == []


def test_candles_contract_rejects_unsupported_symbol_and_interval() -> None:
    client = TestClient(create_app())

    assert client.get("/api/candles?symbol=DOGE-USD&interval=1m&limit=100").status_code == 400
    assert client.get("/api/candles?symbol=BTC-USD&interval=2m&limit=100").status_code == 400
