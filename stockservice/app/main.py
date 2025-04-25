from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from contextlib import asynccontextmanager
import os

# stock_router.py에서 라우터 가져오기
from app.api.stock_router import router as stock_api_router

# FastAPI 앱 생성
app = FastAPI(
    title="Stock Service API",
    description="Stock service for LIF platform",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 경로 설정
stock_router = APIRouter(prefix="/stock")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Stock Service 시작됩니다.")
    yield
    print("🛑 Stock Service 종료됩니다.")

app.lifespan = lifespan

# stock_api_router를 stock_router에 포함
stock_router.include_router(stock_api_router)

# 기본 상태 확인 엔드포인트
@stock_router.get("/status")
async def status() -> Dict[str, Any]:
    return {"status": "Stock Service is running"}

# 라우터 등록
app.include_router(stock_router)

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 