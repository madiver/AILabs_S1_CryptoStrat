from ailabs_crypto.market_data.candle_service import CandleService
from ailabs_crypto.market_data.coinbase_client import CoinbasePublicClient
from ailabs_crypto.models.constants import CandleSource, ChartInterval, Freshness, HistoryStatus, ProductId
from ailabs_crypto.models.market import Candle


def test_coinbase_candle_parser_sorts_and_validates_snapshot() -> None:
    payload = {"start": "1780401600", "open": "100", "high": "105", "low": "95", "close": "102", "volume": "3.5"}

    candle = CoinbasePublicClient.parse_candle(ProductId.BTC_USD, ChartInterval.ONE_MINUTE, payload)

    assert candle.product_id == ProductId.BTC_USD
    assert candle.interval == ChartInterval.ONE_MINUTE
    assert candle.time == 1_780_401_600
    assert candle.source == CandleSource.HISTORICAL


def test_snapshot_requires_100_for_complete_history() -> None:
    candles = [
        Candle(
            product_id=ProductId.BTC_USD,
            interval=ChartInterval.ONE_MINUTE,
            time=idx * 60,
            open="100",
            high="101",
            low="99",
            close="100",
            volume=None,
            complete=True,
            source=CandleSource.HISTORICAL,
        )
        for idx in range(99)
    ]

    partial = CandleService.snapshot_from_candles(ProductId.BTC_USD, ChartInterval.ONE_MINUTE, candles)
    complete = CandleService.snapshot_from_candles(ProductId.BTC_USD, ChartInterval.ONE_MINUTE, candles + [candles[-1].model_copy(update={"time": 99 * 60})])

    assert partial.history_status == HistoryStatus.PARTIAL
    assert partial.freshness == Freshness.STALE
    assert complete.history_status == HistoryStatus.COMPLETE
