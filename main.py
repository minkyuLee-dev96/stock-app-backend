from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Korea Stock App Backend is Running!"}

@app.get("/stock/samsung")
def get_samsung_stock():
    samsung = yf.Ticker("005930.KS")
    info = samsung.fast_info
    
    try:
        current_price = info.last_price
        previous_close = info.previous_close
        
        # 등락률 직접 계산
        if previous_close != 0:
            change_percent = ((current_price - previous_close) / previous_close) * 100
        else:
            change_percent = 0

        return {
            "name": "삼성전자",
            "current_price": round(current_price, 2),
            "change_percent": round(change_percent, 2)
        }
    except Exception as e:
        return {"error": str(e), "message": "데이터 가공 중 오류가 발생했습니다."}