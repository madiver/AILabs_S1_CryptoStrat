from pydantic import BaseModel, ConfigDict

from ailabs_crypto.models.constants import MARKET_DATA_MODE, STALE_AFTER_SECONDS


class RuntimeSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    mode: str = MARKET_DATA_MODE
    trading_enabled: bool = False
    coinbase_rest_url: str = "https://api.coinbase.com/api/v3/brokerage"
    coinbase_ws_url: str = "wss://advanced-trade-ws.coinbase.com"
    stale_after_seconds: int = STALE_AFTER_SECONDS


settings = RuntimeSettings()
