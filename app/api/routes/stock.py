from fastapi import APIRouter

from app.services.stock import get_stock_data

router = APIRouter()


@router.get("/stock/{ticker}")
def get_stock_data_by_ticker(ticker: str) -> dict[str, str | float]:
    try:
        return get_stock_data(ticker)
    except Exception as exc:
        return {"error": str(exc), "message": "Symbol not found or API error"}
