from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ailabs_crypto.models.constants import AuditCategory, Freshness
from ailabs_crypto.models.market import HealthResponse
from ailabs_crypto.runtime.audit import audit_recorder
from ailabs_crypto.runtime.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(title="AI in the Lab Crypto Dashboard", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
    )

    app.state.settings = settings
    app.state.audit = audit_recorder
    audit_recorder.record(AuditCategory.SAFETY, "market_data_only_mode_initialized")

    @app.get("/api/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(
            mode=settings.mode,
            backend_status=Freshness.FRESH,
            trading_enabled=settings.trading_enabled,
        )

    try:
        from ailabs_crypto.api.routes_market import router as market_router

        app.include_router(market_router)
    except ImportError:
        pass

    try:
        from ailabs_crypto.api.ws_market_data import router as ws_router

        app.include_router(ws_router)
    except ImportError:
        pass

    return app
