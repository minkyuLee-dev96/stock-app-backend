from fastapi.testclient import TestClient

from main import app


class MockFastInfo:
    def __init__(self, last_price: float, previous_close: float) -> None:
        self.last_price = last_price
        self.previous_close = previous_close


class MockTickerSuccess:
    def __init__(self, _ticker: str) -> None:
        self.fast_info = MockFastInfo(last_price=75400.12, previous_close=74373.12)
        self.info = {"longName": "Samsung Electronics"}


class MockTickerFail:
    def __init__(self, _ticker: str) -> None:
        raise RuntimeError("mock symbol failure")


def test_root_endpoint_returns_running_message() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Korea Stock App Backend is Running!"}


def test_stock_endpoint_returns_normalized_ticker_data(monkeypatch) -> None:
    monkeypatch.setattr("app.services.stock.yf.Ticker", MockTickerSuccess)
    client = TestClient(app)

    response = client.get("/stock/005930")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Samsung Electronics"
    assert data["ticker"] == "005930.KS"
    assert data["current_price"] == 75400.12
    assert data["change_percent"] == 1.38


def test_stock_endpoint_returns_error_when_lookup_fails(monkeypatch) -> None:
    monkeypatch.setattr("app.services.stock.yf.Ticker", MockTickerFail)
    client = TestClient(app)

    response = client.get("/stock/INVALID")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "Symbol not found or API error"
    assert "mock symbol failure" in data["error"]
