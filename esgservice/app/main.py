from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from contextlib import asynccontextmanager
import os

# esg_router.py에서 라우터 가져오기
from app.api.esg_router import router as esg_api_router

# FastAPI 앱 생성
app = FastAPI(
    title="ESG Service API",
    description="ESG Service API for jinmini.com",
    version="0.1.0"
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
esg_router = APIRouter(prefix="/esg")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 ESG Service 시작됩니다.")
    yield
    print("🛑 ESG Service 종료됩니다.")

app.lifespan = lifespan

# esg_api_router를 esg_router에 포함
esg_router.include_router(esg_api_router)

# 기본 상태 확인 엔드포인트
@esg_router.get("/status")
async def status() -> Dict[str, Any]:
    return {"status": "ESG Service is running"}

# 라우터 등록
app.include_router(esg_router)

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
