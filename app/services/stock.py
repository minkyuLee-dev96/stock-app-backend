import yfinance as yf


def normalize_ticker(ticker: str) -> str:
    return ticker if "." in ticker else f"{ticker}.KS"


def calculate_change_percent(current_price: float, previous_close: float) -> float:
    if previous_close == 0:
        return 0
    return ((current_price - previous_close) / previous_close) * 100


def get_stock_data(ticker: str) -> dict[str, str | float]:
    full_ticker = normalize_ticker(ticker)
    stock = yf.Ticker(full_ticker)
    info = stock.fast_info

    current_price = info.last_price
    previous_close = info.previous_close
    name = stock.info.get("longName", ticker)
    change_percent = calculate_change_percent(current_price, previous_close)

    return {
        "name": name,
        "ticker": full_ticker,
        "current_price": round(current_price, 2),
        "change_percent": round(change_percent, 2),
    }
