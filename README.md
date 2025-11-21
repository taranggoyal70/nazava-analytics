# 💧 Nazava Analytics Platform

Professional analytics dashboard for Shopee e-commerce data. Features ML-powered sales forecasting, customer insights, and real-time performance tracking.

## 🚀 Quick Deploy

**Deploy to Streamlit Cloud in 5 minutes:**

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

See [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md) for detailed deployment instructions.

## ✨ Features

- 📊 **Sales Analytics** - Historical trends, revenue tracking, product performance
- 🤖 **ML Forecasting** - 6-month sales predictions using XGBoost
- 👥 **Customer Insights** - Behavior segmentation and analysis
- 📈 **Campaign Tracking** - Marketing performance metrics
- 🎯 **Product Recommendations** - AI-powered suggestions

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **ML Models:** scikit-learn, XGBoost
- **Visualization:** Plotly
- **Data Processing:** Pandas, NumPy

## 💻 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
cd dashboard
streamlit run app.py
```

Open http://localhost:8501 in your browser.

**Default Login:**
- Username: `admin`
- Password: `admin123`

## 📁 Project Structure

```
├── dashboard/          # Main Streamlit app
│   ├── app.py         # Entry point
│   ├── pages/         # Multi-page dashboard
│   └── utils/         # Helper functions
├── ml/                # ML models and notebooks
├── backend/           # API server (optional)
├── data/              # Sample data files
└── .streamlit/        # Streamlit configuration
```

## 🌐 Live Demo

**Coming Soon:** https://nazava-analytics.streamlit.app

## 📖 Documentation

- [Deployment Guide](STREAMLIT_DEPLOY.md)
- [Setup Instructions](SETUP.md)
- [Dashboard Test Report](DASHBOARD_TEST_REPORT.md)

## 🔐 Security Note

Change default credentials before deploying to production. Edit `dashboard/users.json` to update login credentials.

---

**Built with ❤️ for Shopee Analytics Challenge**
