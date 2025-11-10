"""
Database models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, Text
from sqlalchemy.sql import func
from app.db.database import Base


class RawData(Base):
    """Raw data from CSV files"""
    __tablename__ = "raw_data"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    source_file = Column(String)
    data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProcessedData(Base):
    """Processed analytics data"""
    __tablename__ = "processed_data"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    date = Column(DateTime, index=True)
    metric_name = Column(String, index=True)
    metric_value = Column(Float)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    """ML predictions"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String, index=True)  # sales_forecast, traffic_prediction, etc.
    prediction_date = Column(DateTime, index=True)
    predicted_value = Column(Float)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Alert(Base):
    """System alerts"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String, index=True)  # anomaly, threshold, performance
    severity = Column(String)  # low, medium, high, critical
    title = Column(String)
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Report(Base):
    """Generated reports"""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String, index=True)  # daily, weekly, monthly, custom
    title = Column(String)
    content = Column(JSON)
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CustomerSegment(Base):
    """Customer segmentation results"""
    __tablename__ = "customer_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    segment_id = Column(Integer, index=True)
    segment_name = Column(String)
    description = Column(Text)
    customer_count = Column(Integer)
    avg_order_value = Column(Float)
    characteristics = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
