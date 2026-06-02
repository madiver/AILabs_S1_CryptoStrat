from collections.abc import AsyncIterator

import websockets

from ailabs_crypto.models.constants import ChartInterval, ProductId
from ailabs_crypto.runtime.settings import settings


class CoinbaseWebSocketConsumer:
    """Public market-data WebSocket consumer.

    Phase 1 never sends credentials. The dashboard WebSocket manager can use this class
    for live feed expansion while REST seeded candles remain the deterministic source
    for initial loads and reconnect backfill.
    """

    def __init__(self, ws_url: str = settings.coinbase_ws_url) -> None:
        self.ws_url = ws_url

    async def stream_public_events(
        self,
        symbols: list[ProductId],
        interval: ChartInterval,
    ) -> AsyncIterator[dict]:
        subscribe = {
            "type": "subscribe",
            "product_ids": [symbol.value for symbol in symbols],
            "channel": "heartbeats",
        }
        async with websockets.connect(self.ws_url) as websocket:
            await websocket.send(str(subscribe))
            async for message in websocket:
                yield {"interval": interval.value, "raw": message}
