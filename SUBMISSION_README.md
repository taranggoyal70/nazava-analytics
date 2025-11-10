# Shopee Analytics Platform - Submission Package

## Project Overview

This is an analytics dashboard for e-commerce data analysis with machine learning capabilities.

## What's Included

### 1. Dashboard Application
- **Location:** `dashboard/`
- **Main file:** `dashboard/app.py`
- **Pages:** 8 interactive pages (Overview, Traffic, Sales, Campaigns, etc.)

### 2. Data Files
- **Location:** `data/`
- **Files:** CSV files with cleaned e-commerce data

### 3. ML Models
- **Location:** `ml/` and `ml_models/`
- **Notebooks:** Jupyter notebooks with analysis
- **Models:** Trained forecasting models

### 4. Backend API (Optional)
- **Location:** `backend/`
- **Framework:** FastAPI

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the dashboard:
   ```bash
   cd dashboard
   streamlit run app.py
   ```

3. Open browser at: http://localhost:8501

## Features Implemented

- Real-time KPI dashboard
- Sales forecasting (Prophet, XGBoost)
- Customer segmentation
- Campaign performance tracking
- Product recommendations
- Interactive visualizations

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **ML:** scikit-learn, Prophet, XGBoost
- **Visualization:** Plotly
- **Data:** Pandas, NumPy

## GitHub Repository

https://github.com/taranggoyal70/nazava-analytics

## Notes

- The dashboard works in demo mode without authentication
- Sample data is included for testing
- All ML models are pre-trained and ready to use
