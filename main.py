from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.stock import router as stock_router


def create_app() -> FastAPI:
    app = FastAPI()

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
    def read_root() -> dict[str, str]:
        return {"message": "Korea Stock App Backend is Running!"}

    app.include_router(stock_router)
    return app


app = create_app()