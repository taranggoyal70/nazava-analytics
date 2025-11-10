"""
Reports schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class ReportRequest(BaseModel):
    """Report generation request"""
    report_type: str = Field(..., regex="^(daily|weekly|monthly|custom)$")
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    format: str = Field("pdf", regex="^(pdf|excel|csv|json)$")
    sections: Optional[List[str]] = None


class ReportResponse(BaseModel):
    """Report response"""
    report_id: int
    report_type: str
    status: str
    created_at: datetime
    file_path: Optional[str] = None


class AlertResponse(BaseModel):
    """Alert response"""
    id: int
    alert_type: str
    severity: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    metadata: Optional[Dict] = None


class ExportRequest(BaseModel):
    """Data export request"""
    data_type: str
    format: str = Field("csv", regex="^(csv|excel|json)$")
    filters: Optional[Dict] = None
