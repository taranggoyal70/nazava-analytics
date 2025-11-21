# Shopee Analytics Platform

Analytics dashboard for e-commerce data with ML forecasting.

## Features

- Real-time KPI dashboard
- Sales forecasting
- Customer segmentation
- Product recommendations
- Campaign tracking

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **ML**: scikit-learn, Prophet
- **Database**: PostgreSQL

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
cd dashboard
streamlit run app.py
```

Dashboard: http://localhost:8501

## Project Structure

```
shopee-analytics-platform/
├── dashboard/          # Streamlit dashboard
├── backend/            # FastAPI backend
├── ml/                 # ML models
└── data/               # Data files
```

## License

MIT
