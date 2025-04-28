from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, date

class CompanyNameRequest(BaseModel):
    company_name: str = Field(..., description="검색할 회사명")

class PricePoint(BaseModel):
    date: str = Field(..., description="날짜")
    price: float = Field(..., description="주가")
    volume: int = Field(..., description="거래량")

class TechnicalIndicator(BaseModel):
    name: str = Field(..., description="지표명")
    value: float = Field(..., description="지표값")
    unit: str = Field(..., description="단위")
    description: str = Field(..., description="설명")

class FinancialRatio(BaseModel):
    name: str = Field(..., description="비율명")
    value: float = Field(..., description="값")
    industry_avg: float = Field(..., description="업종 평균")
    unit: str = Field(..., description="단위")

class StockDataResponse(BaseModel):
    companyName: str = Field(..., description="회사명")
    currentPrice: float = Field(..., description="현재가")
    priceChange: float = Field(..., description="등락폭")
    changeRate: float = Field(..., description="등락률")
    tradingVolume: int = Field(..., description="거래량")
    marketCap: int = Field(..., description="시가총액")
    highPrice: float = Field(..., description="고가")
    lowPrice: float = Field(..., description="저가")
    openPrice: float = Field(..., description="시가")
    previousClose: float = Field(..., description="전일 종가")
    historicalPrices: List[PricePoint] = Field(..., description="히스토리컬 데이터")
    technicalIndicators: List[TechnicalIndicator] = Field(..., description="기술적 지표")
    financialRatios: List[FinancialRatio] = Field(..., description="재무 비율")
