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
logger = logging.getLogger("finance_api")

router = APIRouter()

# 단순화된 요청 모델
class CompanyNameRequest(BaseModel):
    company_name: str

# finance 경로로 변경하고 request 객체 받기
@router.post("/financial")
async def get_financial_by_name(request: Request):
    """
    회사명으로 재무제표를 조회합니다.
    - 최근 3개년(당기, 전기, 전전기)의 재무제표 데이터를 반환합니다.
    """
    # 여러 방식으로 로깅 시도
    print("🔥🔥🔥 /financial 엔드포인트가 호출되었습니다!")
    logger.info("🕞🕞🕞🕞🕞🕞 hello - financial 엔드포인트 호출됨")
    
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
        "message": "finance 엔드포인트 호출 성공",
        "status": "success"
    }

  