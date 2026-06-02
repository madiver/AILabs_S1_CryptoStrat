import pytest
from fastapi import HTTPException

from ailabs_crypto.market_data.catalog import coinbase_granularity, interval_seconds, validate_interval
from ailabs_crypto.models.constants import ChartInterval


@pytest.mark.parametrize(
    ("value", "seconds", "granularity"),
    [
        ("1m", 60, "ONE_MINUTE"),
        ("5m", 300, "FIVE_MINUTE"),
        ("15m", 900, "FIFTEEN_MINUTE"),
        ("1h", 3600, "ONE_HOUR"),
    ],
)
def test_supported_interval_mapping(value: str, seconds: int, granularity: str) -> None:
    interval = validate_interval(value)

    assert interval_seconds(interval) == seconds
    assert coinbase_granularity(interval) == granularity


def test_unsupported_interval_rejected() -> None:
    with pytest.raises(HTTPException):
        validate_interval("2m")


def test_chart_interval_enum_values() -> None:
    assert [interval.value for interval in ChartInterval] == ["1m", "5m", "15m", "1h"]
