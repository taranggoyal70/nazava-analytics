"""
Predictions API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.db.database import get_db
from app.services.prediction_service import PredictionService
from app.schemas.predictions import (
    ForecastRequest,
    ForecastResponse,
    AnomalyResponse,
    ChurnPredictionResponse
)

router = APIRouter()


@router.post("/forecast/sales", response_model=ForecastResponse)
async def forecast_sales(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    """Forecast future sales"""
    service = PredictionService(db)
    return await service.forecast_sales(
        days=request.days,
        confidence_interval=request.confidence_interval
    )


@router.post("/forecast/traffic", response_model=ForecastResponse)
async def forecast_traffic(
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    """Forecast future traffic"""
    service = PredictionService(db)
    return await service.forecast_traffic(
        days=request.days,
        confidence_interval=request.confidence_interval
    )


@router.get("/anomalies")
async def detect_anomalies(
    metric: str = Query(..., description="Metric to analyze"),
    lookback_days: int = Query(30, ge=7, le=90),
    sensitivity: float = Query(0.95, ge=0.8, le=0.99),
    db: Session = Depends(get_db)
):
    """Detect anomalies in metrics"""
    service = PredictionService(db)
    return await service.detect_anomalies(metric, lookback_days, sensitivity)


@router.post("/churn/predict")
async def predict_churn(
    db: Session = Depends(get_db)
):
    """Predict customer churn probability"""
    service = PredictionService(db)
    return await service.predict_churn()


@router.get("/demand/forecast")
async def forecast_demand(
    category: Optional[str] = None,
    days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db)
):
    """Forecast product demand"""
    service = PredictionService(db)
    return await service.forecast_demand(category, days)


@router.get("/models/performance")
async def get_model_performance(
    model_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get ML model performance metrics"""
    service = PredictionService(db)
    return await service.get_model_performance(model_type)
