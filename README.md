# Nazava Analytics

Analytics dashboard built for Shopee e-commerce data analysis. Tracks sales, traffic, campaigns, and customer service metrics.

## What it does

- Sales forecasting with ML models
- Traffic and conversion analysis
- Campaign performance tracking
- Customer service metrics
- Product performance insights

## Running locally

```bash
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

Login with `admin` / `admin123`

## Tech used

- Streamlit for the dashboard
- XGBoost and scikit-learn for forecasting
- Plotly for charts
- Pandas for data processing

## Project structure

```
dashboard/    # Main app and pages
ml/          # ML models
backend/     # API (optional)
data/        # CSV data files
```

## Deployment

Works on Streamlit Cloud, Render, or Railway. Just point to `dashboard/app.py` as the entry point.

For Render: `render.yaml` is already configured
For others: Use `streamlit run dashboard/app.py --server.port=$PORT`
