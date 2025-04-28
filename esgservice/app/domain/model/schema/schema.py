from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class CompanyNameRequest(BaseModel):
    company_name: str = Field(..., description="검색할 회사명")

class ESGScores(BaseModel):
    environmental: List[float] = Field(..., description="환경(E) 점수 (최근 3년)")
    social: List[float] = Field(..., description="사회(S) 점수 (최근 3년)")
    governance: List[float] = Field(..., description="지배구조(G) 점수 (최근 3년)")
    totalScore: List[float] = Field(..., description="ESG 종합 점수 (최근 3년)")
    years: List[str] = Field(..., description="해당 연도")

class ScoreComparison(BaseModel):
    companyScore: float = Field(..., description="회사 점수")
    industryAvg: float = Field(..., description="산업 평균 점수")

class IndustryComparison(BaseModel):
    environmental: ScoreComparison = Field(..., description="환경(E) 점수 산업 비교")
    social: ScoreComparison = Field(..., description="사회(S) 점수 산업 비교")
    governance: ScoreComparison = Field(..., description="지배구조(G) 점수 산업 비교")
    totalScore: ScoreComparison = Field(..., description="ESG 종합 점수 산업 비교")

class Metric(BaseModel):
    value: float = Field(..., description="지표 값")
    unit: str = Field(..., description="단위")
    yearOverYearChange: float = Field(..., description="전년 대비 변화율 (%)")
    scale: Optional[str] = Field(None, description="점수 스케일 (있는 경우)")

class KeyMetrics(BaseModel):
    carbonEmissions: Metric = Field(..., description="탄소 배출량")
    energyConsumption: Metric = Field(..., description="에너지 소비량")
    diversityScore: Metric = Field(..., description="다양성 점수")
    boardIndependence: Metric = Field(..., description="이사회 독립성 점수")

class ESGMetricsResponse(BaseModel):
    companyName: str = Field(..., description="회사명")
    esgScores: ESGScores = Field(..., description="ESG 점수")
    industryComparison: IndustryComparison = Field(..., description="산업 비교")
    keyMetrics: KeyMetrics = Field(..., description="핵심 ESG 지표") 