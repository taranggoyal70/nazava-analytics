# Shopee Analytics Dashboard

Analytics dashboard built for analyzing e-commerce data from Shopee. Includes sales forecasting, customer insights, and campaign performance tracking.

## What it does

- Shows key metrics (sales, orders, traffic)
- Forecasts future sales using ML
- Segments customers based on behavior
- Tracks marketing campaign performance
- Recommends products

## Tech used

- Streamlit for the dashboard
- FastAPI for backend API
- scikit-learn and Prophet for ML models
- Plotly for charts

## How to run

```bash
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

Then open http://localhost:8501

## Project structure

```
├── dashboard/     # Main dashboard app
├── backend/       # API server
├── ml/            # ML models and notebooks
└── data/          # CSV data files
```

See [SETUP.md](SETUP.md) for detailed setup instructions.
