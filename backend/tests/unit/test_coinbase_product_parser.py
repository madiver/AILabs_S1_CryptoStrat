from ailabs_crypto.market_data.coinbase_client import CoinbasePublicClient
from ailabs_crypto.models.constants import Freshness, ProductId


def test_parse_public_product_into_market_summary() -> None:
    payload = {
        "product_id": "BTC-USD",
        "price": "68450.12",
        "price_percentage_change_24h": "2.13",
    }

    summary = CoinbasePublicClient.parse_product_summary(payload)

    assert summary.product_id == ProductId.BTC_USD
    assert summary.price == "68450.12"
    assert summary.price_change_24h_percent == "2.13"
    assert summary.freshness == Freshness.FRESH


def test_parse_public_product_defaults_missing_change_to_zero() -> None:
    payload = {"product_id": "ETH-USD", "price": "3500.00"}

    summary = CoinbasePublicClient.parse_product_summary(payload)

    assert summary.product_id == ProductId.ETH_USD
    assert summary.price_change_24h_percent == "0"
