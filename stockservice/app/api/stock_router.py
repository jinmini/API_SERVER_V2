from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.domain.model.schemas.stock_schema import (
    CompanyNameRequest,
    StockDataResponse
)

# 로거 설정
logger = logging.getLogger("stock_router")
logger.setLevel(logging.INFO)
router = APIRouter()

# GET
@router.get("/price", summary="회사명으로 주가 정보 조회 (GET 방식)", response_model=StockDataResponse)
async def get_stock_price_by_path(
    company_name: str = "샘플전자"
):
    """
    회사명으로 주가 정보를 조회합니다. (GET 방식)
    - 현재가, 등락율, 거래량 등 기본 주가 정보를 반환합니다.
    - 과거 주가 데이터를 차트 표시용으로 제공합니다.
    - 기술적 지표와 재무 비율 정보를 함께 제공합니다.
    """
    print(f"📈📈📈get_stock_price_by_path 호출 (GET) - 회사명: {company_name}")
    logger.info(f"📈📈📈get_stock_price_by_path 호출 (GET) - 회사명: {company_name}")
    
    if company_name == "샘플전자":
        # 샘플 데이터 반환
        return_model = {
            "companyName": company_name,
            "currentPrice": 68500,
            "priceChange": 1500,
            "changeRate": 2.24,
            "tradingVolume": 12345678,
            "marketCap": 4090000000000,
            "highPrice": 69000,
            "lowPrice": 67000,
            "openPrice": 67200,
            "previousClose": 67000,
            "historicalPrices": [
                {"date": "2023-04-28", "price": 68500, "volume": 12345678},
                {"date": "2023-04-27", "price": 67000, "volume": 10234567},
                {"date": "2023-04-26", "price": 66800, "volume": 9876543},
                {"date": "2023-04-25", "price": 67200, "volume": 11234567},
                {"date": "2023-04-24", "price": 67800, "volume": 10987654},
                {"date": "2023-04-21", "price": 68200, "volume": 9876543},
                {"date": "2023-04-20", "price": 67900, "volume": 8765432}
            ],
            "technicalIndicators": [
                {"name": "이동평균선(MA5)", "value": 67500, "unit": "원", "description": "5일 이동평균선"},
                {"name": "이동평균선(MA20)", "value": 66800, "unit": "원", "description": "20일 이동평균선"},
                {"name": "RSI", "value": 58.5, "unit": "%", "description": "상대강도지수"},
                {"name": "MACD", "value": 245.3, "unit": "포인트", "description": "이동평균수렴확산지수"}
            ],
            "financialRatios": [
                {"name": "PER", "value": 12.5, "industry_avg": 15.2, "unit": "배"},
                {"name": "PBR", "value": 1.8, "industry_avg": 2.1, "unit": "배"},
                {"name": "ROE", "value": 14.2, "industry_avg": 12.5, "unit": "%"},
                {"name": "배당수익률", "value": 3.2, "industry_avg": 2.8, "unit": "%"}
            ]
        }
    else:
        # 존재하지 않는 회사에 대한 샘플 데이터
        return_model = {
            "companyName": "존재하지 않는 회사",
            "currentPrice": 25000,
            "priceChange": -500,
            "changeRate": -1.96,
            "tradingVolume": 5678901,
            "marketCap": 1250000000000,
            "highPrice": 25500,
            "lowPrice": 24800,
            "openPrice": 25500,
            "previousClose": 25500,
            "historicalPrices": [
                {"date": "2023-04-28", "price": 25000, "volume": 5678901},
                {"date": "2023-04-27", "price": 25500, "volume": 5432109},
                {"date": "2023-04-26", "price": 25300, "volume": 4567890},
                {"date": "2023-04-25", "price": 25400, "volume": 5678901},
                {"date": "2023-04-24", "price": 25600, "volume": 5432109},
                {"date": "2023-04-21", "price": 25800, "volume": 4321098},
                {"date": "2023-04-20", "price": 25700, "volume": 4567890}
            ],
            "technicalIndicators": [
                {"name": "이동평균선(MA5)", "value": 25400, "unit": "원", "description": "5일 이동평균선"},
                {"name": "이동평균선(MA20)", "value": 25200, "unit": "원", "description": "20일 이동평균선"},
                {"name": "RSI", "value": 42.5, "unit": "%", "description": "상대강도지수"},
                {"name": "MACD", "value": -75.3, "unit": "포인트", "description": "이동평균수렴확산지수"}
            ],
            "financialRatios": [
                {"name": "PER", "value": 9.5, "industry_avg": 15.2, "unit": "배"},
                {"name": "PBR", "value": 1.2, "industry_avg": 2.1, "unit": "배"},
                {"name": "ROE", "value": 8.7, "industry_avg": 12.5, "unit": "%"},
                {"name": "배당수익률", "value": 2.1, "industry_avg": 2.8, "unit": "%"}
            ]
        }
    
    return return_model

# POST
@router.post("/price", summary="회사명으로 주가 정보 조회", response_model=StockDataResponse)
async def get_stock_price_by_name(
    payload: CompanyNameRequest,
):
    """
    회사명으로 주가 정보를 조회합니다.
    - 현재가, 등락율, 거래량 등 기본 주가 정보를 반환합니다.
    - 과거 주가 데이터를 차트 표시용으로 제공합니다.
    - 기술적 지표와 재무 비율 정보를 함께 제공합니다.
    """
    print(f"📈📈📈get_stock_price_by_name 호출 - 회사명: {payload.company_name}")
    logger.info(f"📈📈📈get_stock_price_by_name 호출 - 회사명: {payload.company_name}")
    
    if payload.company_name == "샘플전자":
        # 샘플 데이터 반환
        return_model = {
            "companyName": payload.company_name,
            "currentPrice": 68500,
            "priceChange": 1500,
            "changeRate": 2.24,
            "tradingVolume": 12345678,
            "marketCap": 4090000000000,
            "highPrice": 69000,
            "lowPrice": 67000,
            "openPrice": 67200,
            "previousClose": 67000,
            "historicalPrices": [
                {"date": "2023-04-28", "price": 68500, "volume": 12345678},
                {"date": "2023-04-27", "price": 67000, "volume": 10234567},
                {"date": "2023-04-26", "price": 66800, "volume": 9876543},
                {"date": "2023-04-25", "price": 67200, "volume": 11234567},
                {"date": "2023-04-24", "price": 67800, "volume": 10987654},
                {"date": "2023-04-21", "price": 68200, "volume": 9876543},
                {"date": "2023-04-20", "price": 67900, "volume": 8765432}
            ],
            "technicalIndicators": [
                {"name": "이동평균선(MA5)", "value": 67500, "unit": "원", "description": "5일 이동평균선"},
                {"name": "이동평균선(MA20)", "value": 66800, "unit": "원", "description": "20일 이동평균선"},
                {"name": "RSI", "value": 58.5, "unit": "%", "description": "상대강도지수"},
                {"name": "MACD", "value": 245.3, "unit": "포인트", "description": "이동평균수렴확산지수"}
            ],
            "financialRatios": [
                {"name": "PER", "value": 12.5, "industry_avg": 15.2, "unit": "배"},
                {"name": "PBR", "value": 1.8, "industry_avg": 2.1, "unit": "배"},
                {"name": "ROE", "value": 14.2, "industry_avg": 12.5, "unit": "%"},
                {"name": "배당수익률", "value": 3.2, "industry_avg": 2.8, "unit": "%"}
            ]
        }
    else:
        # 존재하지 않는 회사에 대한 샘플 데이터
        return_model = {
            "companyName": "존재하지 않는 회사",
            "currentPrice": 25000,
            "priceChange": -500,
            "changeRate": -1.96,
            "tradingVolume": 5678901,
            "marketCap": 1250000000000,
            "highPrice": 25500,
            "lowPrice": 24800,
            "openPrice": 25500,
            "previousClose": 25500,
            "historicalPrices": [
                {"date": "2023-04-28", "price": 25000, "volume": 5678901},
                {"date": "2023-04-27", "price": 25500, "volume": 5432109},
                {"date": "2023-04-26", "price": 25300, "volume": 4567890},
                {"date": "2023-04-25", "price": 25400, "volume": 5678901},
                {"date": "2023-04-24", "price": 25600, "volume": 5432109},
                {"date": "2023-04-21", "price": 25800, "volume": 4321098},
                {"date": "2023-04-20", "price": 25700, "volume": 4567890}
            ],
            "technicalIndicators": [
                {"name": "이동평균선(MA5)", "value": 25400, "unit": "원", "description": "5일 이동평균선"},
                {"name": "이동평균선(MA20)", "value": 25200, "unit": "원", "description": "20일 이동평균선"},
                {"name": "RSI", "value": 42.5, "unit": "%", "description": "상대강도지수"},
                {"name": "MACD", "value": -75.3, "unit": "포인트", "description": "이동평균수렴확산지수"}
            ],
            "financialRatios": [
                {"name": "PER", "value": 9.5, "industry_avg": 15.2, "unit": "배"},
                {"name": "PBR", "value": 1.2, "industry_avg": 2.1, "unit": "배"},
                {"name": "ROE", "value": 8.7, "industry_avg": 12.5, "unit": "%"},
                {"name": "배당수익률", "value": 2.1, "industry_avg": 2.8, "unit": "%"}
            ]
        }
    
    return return_model
