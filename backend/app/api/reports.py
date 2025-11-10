"""
Reports API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from app.db.database import get_db
from app.services.report_service import ReportService
from app.schemas.reports import (
    ReportRequest,
    ReportResponse,
    AlertResponse,
    ExportRequest
)

router = APIRouter()


@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a new report"""
    service = ReportService(db)
    return await service.generate_report(
        report_type=request.report_type,
        start_date=request.start_date,
        end_date=request.end_date,
        format=request.format,
        background_tasks=background_tasks
    )


@router.get("/list")
async def list_reports(
    report_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List generated reports"""
    service = ReportService(db)
    return await service.list_reports(report_type, limit)


@router.get("/{report_id}")
async def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific report"""
    service = ReportService(db)
    return await service.get_report(report_id)


@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Download report file"""
    service = ReportService(db)
    file_path = await service.get_report_file_path(report_id)
    
    if not file_path:
        raise HTTPException(status_code=404, detail="Report file not found")
    
    return FileResponse(
        path=file_path,
        filename=f"report_{report_id}.pdf",
        media_type="application/pdf"
    )


@router.post("/export")
async def export_data(
    request: ExportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Export data in various formats"""
    service = ReportService(db)
    return await service.export_data(
        data_type=request.data_type,
        format=request.format,
        filters=request.filters,
        background_tasks=background_tasks
    )


@router.get("/alerts/list")
async def list_alerts(
    severity: Optional[str] = None,
    is_read: Optional[bool] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """List system alerts"""
    service = ReportService(db)
    return await service.list_alerts(severity, is_read, limit)


@router.post("/alerts/{alert_id}/mark-read")
async def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db)
):
    """Mark an alert as read"""
    service = ReportService(db)
    return await service.mark_alert_read(alert_id)


@router.post("/alerts/create")
async def create_alert(
    alert_type: str,
    severity: str,
    title: str,
    message: str,
    metadata: Optional[dict] = None,
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    service = ReportService(db)
    return await service.create_alert(
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
        metadata=metadata
    )


@router.post("/schedule")
async def schedule_report(
    report_type: str,
    frequency: str = Query(..., regex="^(daily|weekly|monthly)$"),
    recipients: List[str] = Query(...),
    db: Session = Depends(get_db)
):
    """Schedule recurring reports"""
    service = ReportService(db)
    return await service.schedule_report(report_type, frequency, recipients)
