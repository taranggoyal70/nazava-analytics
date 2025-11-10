"""
ML Insights API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.database import get_db
from app.services.insights_service import InsightsService
from app.schemas.insights import (
    SegmentationResponse,
    RecommendationRequest,
    RecommendationResponse,
    OptimizationResponse
)

router = APIRouter()


@router.post("/segment/customers")
async def segment_customers(
    n_clusters: int = Query(5, ge=2, le=10),
    algorithm: str = Query("kmeans", regex="^(kmeans|dbscan|hierarchical)$"),
    db: Session = Depends(get_db)
):
    """Segment customers using ML clustering"""
    service = InsightsService(db)
    return await service.segment_customers(n_clusters, algorithm)


@router.get("/segments")
async def get_segments(
    db: Session = Depends(get_db)
):
    """Get existing customer segments"""
    service = InsightsService(db)
    return await service.get_segments()


@router.get("/segments/{segment_id}")
async def get_segment_details(
    segment_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a segment"""
    service = InsightsService(db)
    return await service.get_segment_details(segment_id)


@router.post("/recommend/products")
async def recommend_products(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get product recommendations"""
    service = InsightsService(db)
    return await service.recommend_products(
        customer_id=request.customer_id,
        n_recommendations=request.n_recommendations,
        algorithm=request.algorithm
    )


@router.post("/optimize/price")
async def optimize_price(
    product_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get optimal price recommendations"""
    service = InsightsService(db)
    return await service.optimize_price(product_id)


@router.post("/optimize/marketing")
async def optimize_marketing_mix(
    budget: float = Query(..., gt=0),
    channels: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Optimize marketing budget allocation"""
    service = InsightsService(db)
    return await service.optimize_marketing_mix(budget, channels)


@router.get("/insights/summary")
async def get_insights_summary(
    db: Session = Depends(get_db)
):
    """Get summary of all ML insights"""
    service = InsightsService(db)
    return await service.get_insights_summary()


@router.post("/analyze/cohort")
async def analyze_cohort(
    cohort_type: str = Query("monthly", regex="^(daily|weekly|monthly)$"),
    metric: str = Query("retention", regex="^(retention|revenue|orders)$"),
    db: Session = Depends(get_db)
):
    """Perform cohort analysis"""
    service = InsightsService(db)
    return await service.analyze_cohort(cohort_type, metric)
