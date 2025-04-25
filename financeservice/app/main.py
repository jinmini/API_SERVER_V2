from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from contextlib import asynccontextmanager
import os

# fin_router.py에서 라우터 가져오기
from app.api.fin_router import router as fin_api_router

# FastAPI 앱 생성
app = FastAPI(
    title="Finance Service API",
    description="Finance Service API for jinmini.com",
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
fin_router = APIRouter(prefix="/fin")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Finance Service 시작됩니다.")
    yield
    print("🛑 Finance Service 종료됩니다.")

app.lifespan = lifespan

# fin_api_router를 fin_router에 포함 (중요!)
fin_router.include_router(fin_api_router)

# 기존 특정 경로 핸들러들
@fin_router.get("/status")
async def status() -> Dict[str, Any]:
    return {"status": "Finance Service is running"}

@fin_router.get("/balance/{user_id}")
async def get_balance(user_id: str) -> Dict[str, Any]:
    return {"user_id": user_id, "balance": 10000}

@fin_router.post("/transfer")
async def transfer(request: Request) -> Dict[str, Any]:
    data = await request.json()
    return {
        "status": "success",
        "message": "Transfer processed",
        "data": data
    }

# 라우터 등록
app.include_router(fin_router)

# 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 