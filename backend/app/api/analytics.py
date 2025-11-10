"""
Analytics API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd

from app.db.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    KPIResponse,
    TrendResponse,
    FunnelResponse,
    CategoryMetrics
)

router = APIRouter()


@router.get("/kpis", response_model=KPIResponse)
async def get_kpis(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get key performance indicators"""
    service = AnalyticsService(db)
    return await service.get_kpis(start_date, end_date)


@router.get("/trends/{metric}")
async def get_trend(
    metric: str,
    category: Optional[str] = None,
    period: str = Query("daily", regex="^(daily|weekly|monthly)$"),
    db: Session = Depends(get_db)
):
    """Get trend data for a specific metric"""
    service = AnalyticsService(db)
    return await service.get_trend(metric, category, period)


@router.get("/funnel")
async def get_funnel(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get conversion funnel data"""
    service = AnalyticsService(db)
    return await service.get_funnel(start_date, end_date)


@router.get("/categories")
async def get_category_metrics(
    db: Session = Depends(get_db)
):
    """Get metrics by category"""
    service = AnalyticsService(db)
    return await service.get_category_metrics()


@router.get("/traffic/sources")
async def get_traffic_sources(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get traffic by source"""
    service = AnalyticsService(db)
    return await service.get_traffic_sources(start_date, end_date)


@router.get("/campaigns/performance")
async def get_campaign_performance(
    campaign_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get campaign performance metrics"""
    service = AnalyticsService(db)
    return await service.get_campaign_performance(campaign_type)


@router.get("/products/top")
async def get_top_products(
    limit: int = Query(10, ge=1, le=100),
    metric: str = Query("sales", regex="^(sales|orders|views)$"),
    db: Session = Depends(get_db)
):
    """Get top performing products"""
    service = AnalyticsService(db)
    return await service.get_top_products(limit, metric)


@router.get("/customer-service/metrics")
async def get_customer_service_metrics(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get customer service metrics"""
    service = AnalyticsService(db)
    return await service.get_customer_service_metrics(start_date, end_date)
