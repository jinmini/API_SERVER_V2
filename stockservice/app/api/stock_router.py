from fastapi import APIRouter, Request
import logging
import sys
from pydantic import BaseModel

# 명시적 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("stock_api")

router = APIRouter()

# 요청 모델 정의
class StockRequest(BaseModel):
    ticker: str

# /stockservice 엔드포인트 구현
@router.post("/stockservice")
async def get_stock_service(request: Request):
    """
    주식 정보를 조회합니다.
    """
    # 로깅
    print("🔥🔥🔥 /stockservice 엔드포인트가 호출되었습니다!")
    logger.info("📈📈📈 hello - stockservice 엔드포인트 호출됨")
    
    # 함수 진입점 로깅
    print("함수 시작")
    
    # 요청 데이터 출력
    try:
        data = await request.json()
        print(f"받은 데이터: {data}")
    except Exception as e:
        print(f"요청 본문 파싱 실패: {e}")
    
    # 함수 종료점 로깅
    print("함수 종료, 응답 반환")
    
    return {
        "message": "Stock 서비스 호출 성공",
        "status": "success",
        "data": {
            "ticker": "SAMPLE",
            "price": 250.75,
            "change": 2.5,
            "change_percent": 1.01,
            "market_cap": "1.2T"
        }
    }
