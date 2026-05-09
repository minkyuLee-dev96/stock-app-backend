from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# CORS 설정: 어떤 주소에서 오는 요청을 허용할지 정의
origins = [
    "http://localhost:5173",  # 로컬 개발 환경
    "https://korea-stock-app-zeta.vercel.app",  # 네 Vercel 프론트엔드 주소 (확인 후 수정 필요)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST 등 모든 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

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
        return {"error": str(e), "message": "Internal Server Error"}