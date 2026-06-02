from fastapi.testclient import TestClient

from ailabs_crypto.api.app import create_app


def test_no_trading_routes_are_exposed() -> None:
    app = create_app()
    route_paths = {route.path for route in app.routes}

    forbidden_terms = (
        "order",
        "orders",
        "account",
        "accounts",
        "balance",
        "balances",
        "position",
        "positions",
        "trade",
        "trading",
    )

    assert not any(term in path.lower() for path in route_paths for term in forbidden_terms)


def test_health_reports_market_data_only_mode() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["mode"] == "market-data-only"
    assert response.json()["trading_enabled"] is False
