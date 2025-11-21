"""
Application configuration
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Nazava Analytics Platform"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/shopee_analytics"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501",  # Streamlit default
        "http://localhost:8000"
    ]
    
    # Data paths
    DATA_PATH: str = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    MODEL_PATH: str = "/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/ml/models/trained_models"
    
    # ML Settings
    FORECAST_DAYS: int = 30
    CONFIDENCE_INTERVAL: float = 0.95
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
