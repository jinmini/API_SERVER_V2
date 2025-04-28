from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from app.domain.model.schema.schema import (
    CompanyNameRequest,
    ESGMetricsResponse
)

# 로거 설정
logger = logging.getLogger("esg_router")
logger.setLevel(logging.INFO)
router = APIRouter()

# GET
@router.get("/metrics", summary="회사명으로 ESG 평가 조회 (GET 방식)", response_model=ESGMetricsResponse)
async def get_esg_metrics_by_path(
    company_name: str = "샘플전자"
):
    """
    회사명으로 ESG 평가 데이터를 조회합니다. (GET 방식)
    - 환경(E), 사회(S), 지배구조(G) 영역별 평가점수를 반환합니다.
    - 연도별 ESG 점수 추이를 보여줍니다.
    - 동종업계 평균과 비교 정보를 제공합니다.
    """
    print(f"🌱🌱🌱get_esg_metrics_by_path 호출 (GET) - 회사명: {company_name}")
    logger.info(f"🌱🌱🌱get_esg_metrics_by_path 호출 (GET) - 회사명: {company_name}")
    
    if company_name == "샘플전자":
        return_model = {
            "companyName": company_name,
            "esgScores": {
                "environmental": [85, 82, 78],  # 최근 3년 데이터
                "social": [78, 75, 72],
                "governance": [90, 88, 85],
                "totalScore": [84, 81, 78],
                "years": ["2023", "2022", "2021"]
            },
            "industryComparison": {
                "environmental": {"companyScore": 85, "industryAvg": 75},
                "social": {"companyScore": 78, "industryAvg": 72},
                "governance": {"companyScore": 90, "industryAvg": 80},
                "totalScore": {"companyScore": 84, "industryAvg": 76},
            },
            "keyMetrics": {
                "carbonEmissions": {"value": 120000, "unit": "tCO2e", "yearOverYearChange": -5.2},
                "energyConsumption": {"value": 450000, "unit": "MWh", "yearOverYearChange": -3.1},
                "diversityScore": {"value": 78, "unit": "점", "scale": "0-100", "yearOverYearChange": 4.5},
                "boardIndependence": {"value": 85, "unit": "점", "scale": "0-100", "yearOverYearChange": 2.0}
            }
        }
    else:
        return_model = {
            "companyName": "존재하지 않는 회사",
            "esgScores": {
                "environmental": [75, 73, 70],
                "social": [68, 65, 63],
                "governance": [72, 70, 68],
                "totalScore": [72, 69, 67],
                "years": ["2023", "2022", "2021"]
            },
            "industryComparison": {
                "environmental": {"companyScore": 75, "industryAvg": 75},
                "social": {"companyScore": 68, "industryAvg": 72},
                "governance": {"companyScore": 72, "industryAvg": 80},
                "totalScore": {"companyScore": 72, "industryAvg": 76},
            },
            "keyMetrics": {
                "carbonEmissions": {"value": 200000, "unit": "tCO2e", "yearOverYearChange": -2.1},
                "energyConsumption": {"value": 600000, "unit": "MWh", "yearOverYearChange": -1.5},
                "diversityScore": {"value": 65, "unit": "점", "scale": "0-100", "yearOverYearChange": 2.0},
                "boardIndependence": {"value": 70, "unit": "점", "scale": "0-100", "yearOverYearChange": 1.0}
            }
        }
    
    return return_model

# POST
@router.post("/metrics", summary="회사명으로 ESG 평가 조회", response_model=ESGMetricsResponse)
async def get_esg_metrics_by_name(
    payload: CompanyNameRequest,
):
    """
    회사명으로 ESG 평가 데이터를 조회합니다.
    - 환경(E), 사회(S), 지배구조(G) 영역별 평가점수를 반환합니다.
    - 연도별 ESG 점수 추이를 보여줍니다.
    - 동종업계 평균과 비교 정보를 제공합니다.
    """
    print(f"🌱🌱🌱get_esg_metrics_by_name 호출 - 회사명: {payload.company_name}")
    logger.info(f"🌱🌱🌱get_esg_metrics_by_name 호출 - 회사명: {payload.company_name}")
    
    if payload.company_name == "샘플전자":
        return_model = {
            "companyName": payload.company_name,
            "esgScores": {
                "environmental": [85, 82, 78],  # 최근 3년 데이터
                "social": [78, 75, 72],
                "governance": [90, 88, 85],
                "totalScore": [84, 81, 78],
                "years": ["2023", "2022", "2021"]
            },
            "industryComparison": {
                "environmental": {"companyScore": 85, "industryAvg": 75},
                "social": {"companyScore": 78, "industryAvg": 72},
                "governance": {"companyScore": 90, "industryAvg": 80},
                "totalScore": {"companyScore": 84, "industryAvg": 76},
            },
            "keyMetrics": {
                "carbonEmissions": {"value": 120000, "unit": "tCO2e", "yearOverYearChange": -5.2},
                "energyConsumption": {"value": 450000, "unit": "MWh", "yearOverYearChange": -3.1},
                "diversityScore": {"value": 78, "unit": "점", "scale": "0-100", "yearOverYearChange": 4.5},
                "boardIndependence": {"value": 85, "unit": "점", "scale": "0-100", "yearOverYearChange": 2.0}
            }
        }
    else:
        return_model = {
            "companyName": "존재하지 않는 회사",
            "esgScores": {
                "environmental": [75, 73, 70],
                "social": [68, 65, 63],
                "governance": [72, 70, 68],
                "totalScore": [72, 69, 67],
                "years": ["2023", "2022", "2021"]
            },
            "industryComparison": {
                "environmental": {"companyScore": 75, "industryAvg": 75},
                "social": {"companyScore": 68, "industryAvg": 72},
                "governance": {"companyScore": 72, "industryAvg": 80},
                "totalScore": {"companyScore": 72, "industryAvg": 76},
            },
            "keyMetrics": {
                "carbonEmissions": {"value": 200000, "unit": "tCO2e", "yearOverYearChange": -2.1},
                "energyConsumption": {"value": 600000, "unit": "MWh", "yearOverYearChange": -1.5},
                "diversityScore": {"value": 65, "unit": "점", "scale": "0-100", "yearOverYearChange": 2.0},
                "boardIndependence": {"value": 70, "unit": "점", "scale": "0-100", "yearOverYearChange": 1.0}
            }
        }
    
    return return_model
