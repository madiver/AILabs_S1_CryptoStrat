from datetime import datetime, timezone

from ailabs_crypto.market_data.coinbase_client import CoinbasePublicClient
from ailabs_crypto.models.constants import AuditCategory, Freshness, ProductId, SUPPORTED_SYMBOLS
from ailabs_crypto.models.market import MarketSummary
from ailabs_crypto.runtime.audit import AuditRecorder, audit_recorder


class MarketSummaryService:
    def __init__(
        self,
        client: CoinbasePublicClient | None = None,
        recorder: AuditRecorder = audit_recorder,
    ) -> None:
        self.client = client or CoinbasePublicClient()
        self.recorder = recorder

    async def get_summaries(self) -> list[MarketSummary]:
        summaries: list[MarketSummary] = []
        for product_id in SUPPORTED_SYMBOLS:
            summaries.append(await self.get_summary(product_id))
        return summaries

    async def get_summary(self, product_id: ProductId) -> MarketSummary:
        try:
            summary = await self.client.get_product_summary(product_id)
            self.recorder.record(
                AuditCategory.MARKET_DATA,
                "summary_refreshed",
                product_id=product_id,
            )
            return summary
        except Exception as exc:
            self.recorder.record(
                AuditCategory.MARKET_DATA,
                "summary_unavailable",
                product_id=product_id,
                details={"error": exc.__class__.__name__},
            )
            return MarketSummary(
                product_id=product_id,
                price="0",
                price_change_24h_percent="0",
                last_update_at=datetime.now(timezone.utc),
                freshness=Freshness.OFFLINE,
            )
