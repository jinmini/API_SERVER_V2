import json
from typing import Any, Dict, Optional
from fastapi import APIRouter, FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging
import sys
import time
from dotenv import load_dotenv
from app.api.stock_router import router as stock_api_router

# ✅로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("stock_api")

# ✅.env 파일 로드
load_dotenv()

# ✅ 애플리케이션 시작 시 실행
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Stock API 서비스 시작")
    yield
    logger.info("🛑 Stock API 서비스 종료")

# ✅ FastAPI 앱 생성 
app = FastAPI(
    title="Stock API",
    description="Stock API for jinmini.com",
    version="0.1.0",
    lifespan=lifespan
)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 서브 라우터 생성
stock_router = APIRouter(prefix="/stock", tags=["Stock API"])

# ✅ 서브 라우터와 엔드포인트를 연결
app.include_router(stock_api_router, prefix="/stock")

# ✅ 서브라우터 등록
app.include_router(stock_router, tags=["Stock"])

# ✅ 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8082))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
