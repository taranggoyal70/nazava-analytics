"""
Predictions schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ForecastRequest(BaseModel):
    """Forecast request model"""
    days: int = Field(30, ge=7, le=90, description="Number of days to forecast")
    confidence_interval: float = Field(0.95, ge=0.8, le=0.99)


class ForecastDataPoint(BaseModel):
    """Single forecast data point"""
    date: str
    predicted_value: float
    lower_bound: float
    upper_bound: float


class ForecastResponse(BaseModel):
    """Forecast response model"""
    metric: str
    forecast: List[ForecastDataPoint]
    model_type: str
    accuracy_metrics: dict
    generated_at: datetime


class AnomalyDataPoint(BaseModel):
    """Anomaly detection data point"""
    date: str
    value: float
    is_anomaly: bool
    anomaly_score: float
    expected_range: dict


class AnomalyResponse(BaseModel):
    """Anomaly detection response"""
    metric: str
    anomalies: List[AnomalyDataPoint]
    total_anomalies: int
    detection_method: str


class ChurnPredictionResponse(BaseModel):
    """Churn prediction response"""
    customer_id: str
    churn_probability: float
    risk_level: str  # low, medium, high
    factors: List[dict]
    recommended_actions: List[str]
