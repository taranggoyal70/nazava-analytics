"""
ML Insights schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class SegmentationResponse(BaseModel):
    """Customer segmentation response"""
    n_segments: int
    segments: List[Dict]
    algorithm: str
    silhouette_score: Optional[float] = None


class RecommendationRequest(BaseModel):
    """Product recommendation request"""
    customer_id: Optional[str] = None
    n_recommendations: int = Field(10, ge=1, le=50)
    algorithm: str = Field("collaborative", regex="^(collaborative|content|hybrid)$")


class ProductRecommendation(BaseModel):
    """Single product recommendation"""
    product_id: str
    product_name: str
    score: float
    reason: str


class RecommendationResponse(BaseModel):
    """Product recommendations response"""
    customer_id: Optional[str]
    recommendations: List[ProductRecommendation]
    algorithm: str


class PriceOptimization(BaseModel):
    """Price optimization result"""
    product_id: str
    current_price: float
    recommended_price: float
    expected_revenue_increase: float
    confidence: float


class OptimizationResponse(BaseModel):
    """General optimization response"""
    optimization_type: str
    recommendations: List[Dict]
    expected_impact: Dict[str, float]
    confidence: float
