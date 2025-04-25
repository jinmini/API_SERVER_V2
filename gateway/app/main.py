from typing import Any, Dict, Optional
from fastapi import APIRouter, FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import httpx
import os
import logging
import sys
import time
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("gateway_api")

# .env 파일 로드
load_dotenv()

# ✅ FastAPI 앱 생성 
app = FastAPI(
    title="Gateway API",
    description="Gateway API for jinmini.com",
    version="0.1.0",
)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 URL을 상수로 직접 정의 (전역 변수에 의존하지 않음)
STOCK_SERVICE_URL = os.getenv("STOCK_SERVICE_URL", "http://stock-service:8000")
ESG_SERVICE_URL = os.getenv("ESG_SERVICE_URL", "http://esg-service:8002")
FINANCE_SERVICE_URL = os.getenv("FINANCE_SERVICE_URL", "http://finance-service:8000")

# 요청 처리 시간 측정 미들웨어
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request to {request.url.path} processed in {process_time:.4f} seconds")
    return response

# ✅ 애플리케이션 시작 시 실행
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Gateway API 서비스 시작")
    # 서비스 URL 로깅
    logger.info(f"서비스 URL 구성: STOCK={STOCK_SERVICE_URL}, ESG={ESG_SERVICE_URL}, FINANCE={FINANCE_SERVICE_URL}")
    yield
    logger.info("🛑 Gateway API 서비스 종료")

app.lifespan = lifespan

# 공통 프록시 함수
async def proxy_to_service(path: str, request: Request, service_name: str, service_url: str):
    method = request.method
    logger.info(f"Gateway: {method} 요청 처리 - 서비스: {service_name}, 경로: /{path}, URL: {service_url}")
    
    try:
        # 헤더 처리
        headers = dict(request.headers)
        # 자동 생성되는 헤더 제거
        for header in ["host", "content-length"]:
            headers.pop(header, None)
        
        # 요청 본문 획득
        body = await request.body()
        
        # 타임아웃 설정으로 비동기 클라이언트 생성
        async with httpx.AsyncClient(timeout=30.0) as client:
            target_url = f"{service_url}/{service_name}/{path}"
            logger.info(f"요청 전달: {method} {target_url}")
            
            response = await client.request(
                method=method,
                url=target_url,
                headers=headers,
                content=body
            )
            
            logger.info(f"{service_name} 서비스 응답: {response.status_code}")
            return JSONResponse(
                content=response.json(), 
                status_code=response.status_code
            )
            
    except httpx.TimeoutException:
        logger.error(f"{service_name} 서비스 요청 타임아웃")
        raise HTTPException(status_code=504, detail=f"Gateway 타임아웃: {service_name} 서비스 연결 실패")
    except httpx.RequestError as e:
        logger.error(f"{service_name} 서비스 요청 오류: {str(e)}")
        raise HTTPException(status_code=502, detail=f"Gateway 오류: {service_name} 서비스 연결 실패")
    except Exception as e:
        logger.error(f"예기치 않은 오류: {str(e)}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")

# 메소드별로 분리된 새 코드
@app.get("/e/stock/{path:path}")
async def proxy_stock_get(path: str, request: Request):
    return await proxy_to_service(path, request, "stock", STOCK_SERVICE_URL)

@app.post("/e/stock/{path:path}")
async def proxy_stock_post(path: str, request: Request):
    return await proxy_to_service(path, request, "stock", STOCK_SERVICE_URL)

@app.put("/e/stock/{path:path}")
async def proxy_stock_put(path: str, request: Request):
    return await proxy_to_service(path, request, "stock", STOCK_SERVICE_URL)

@app.delete("/e/stock/{path:path}")
async def proxy_stock_delete(path: str, request: Request):
    return await proxy_to_service(path, request, "stock", STOCK_SERVICE_URL)

@app.get("/e/esg/{path:path}")
async def proxy_esg_get(path: str, request: Request):
    return await proxy_to_service(path, request, "esg", ESG_SERVICE_URL)

@app.post("/e/esg/{path:path}")
async def proxy_esg_post(path: str, request: Request):
    return await proxy_to_service(path, request, "esg", ESG_SERVICE_URL)

@app.put("/e/esg/{path:path}")
async def proxy_esg_put(path: str, request: Request):
    return await proxy_to_service(path, request, "esg", ESG_SERVICE_URL)

@app.delete("/e/esg/{path:path}")
async def proxy_esg_delete(path: str, request: Request):
    return await proxy_to_service(path, request, "esg", ESG_SERVICE_URL)

# @app.api_route("/e/fin/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
# async def proxy_finance(path: str, request: Request):
#     logger.info(f"***** Received request for /e/fin/{path} with method: {request.method} *****")
#     return await proxy_to_service(path, request, "fin", FINANCE_SERVICE_URL)

@app.get("/e/fin/{path:path}")
async def proxy_finance_get(path: str, request: Request):
    # logger.info(...) # 필요시 로깅 추가
    return await proxy_to_service(path, request, "fin", FINANCE_SERVICE_URL)

@app.post("/e/fin/{path:path}")
async def proxy_finance_post(path: str, request: Request):
    # logger.info(...)
    return await proxy_to_service(path, request, "fin", FINANCE_SERVICE_URL)

@app.put("/e/fin/{path:path}")
async def proxy_finance_put(path: str, request: Request):
    # logger.info(...)
    return await proxy_to_service(path, request, "fin", FINANCE_SERVICE_URL)

@app.delete("/e/fin/{path:path}")
async def proxy_finance_delete(path: str, request: Request):
    # logger.info(...)
    return await proxy_to_service(path, request, "fin", FINANCE_SERVICE_URL)

# ✅ 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True) 

