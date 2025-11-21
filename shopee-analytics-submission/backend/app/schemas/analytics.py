"""
Analytics schemas
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class KPIResponse(BaseModel):
    """KPI response model"""
    total_sales: float
    total_orders: int
    total_visitors: int
    conversion_rate: float
    average_order_value: float
    customer_satisfaction: float
    period: str
    comparison: Optional[Dict[str, float]] = None


class TrendDataPoint(BaseModel):
    """Single data point in a trend"""
    date: str
    value: float
    label: Optional[str] = None


class TrendResponse(BaseModel):
    """Trend response model"""
    metric: str
    data: List[TrendDataPoint]
    period: str
    trend_direction: str  # up, down, stable
    change_percentage: float


class FunnelStage(BaseModel):
    """Funnel stage data"""
    stage: str
    count: int
    percentage: float
    conversion_rate: Optional[float] = None


class FunnelResponse(BaseModel):
    """Funnel response model"""
    stages: List[FunnelStage]
    overall_conversion: float


class CategoryMetrics(BaseModel):
    """Metrics by category"""
    category: str
    sales: float
    orders: int
    conversion_rate: float
    avg_order_value: float
