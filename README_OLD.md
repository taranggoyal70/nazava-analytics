# Shopee Analytics Platform

Analytics dashboard for e-commerce data with ML-powered insights and forecasting.

## Features

- Real-time KPI dashboard
- Sales forecasting

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
cd dashboard
streamlit run app.py
```

Access at: http://localhost:8501

## Project Structure

```
shopee-analytics-platform/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   ├── analytics.py
│   │   │   ├── predictions.py
│   │   │   ├── insights.py
│   │   │   └── reports.py
│   │   ├── services/          # Business logic
│   │   │   ├── analytics_service.py
│   │   │   ├── prediction_service.py
│   │   │   ├── insights_service.py
│   │   │   └── report_service.py
│   │   ├── ml/                # ML models
│   │   │   ├── forecasting.py
│   │   │   ├── segmentation.py
│   │   │   └── recommendation.py
│   │   ├── db/                # Database
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── core/              # Config
│   │   └── main.py            # App entry point
│   ├── requirements.txt
│   └── Dockerfile
│
├── dashboard/                  # Streamlit dashboard
│   ├── pages/                 # Dashboard pages
│   │   ├── 1_Overview.py
│   │   ├── 2_Traffic.py
│   │   ├── 3_Sales.py
│   │   ├── 4_Campaigns.py
│   │   ├── 5_Customer_Service.py
│   │   ├── 6_Products.py
│   │   ├── 7_Predictions.py
│   │   └── 8_ML_Insights.py
│   ├── components/            # Reusable components
│   ├── utils/                 # Utilities
│   ├── app.py                 # Main app
│   └── requirements.txt
│
├── ml/                        # ML experiments
│   ├── notebooks/             # Jupyter notebooks
│   ├── models/                # Trained models
│   └── scripts/               # Training scripts
│
├── database/                  # Database files
│   ├── migrations/            # Alembic migrations
│   └── schema.sql             # Database schema
│
├── docker-compose.yml         # Docker setup
├── .env.example               # Environment template
├── ARCHITECTURE.md            # Architecture docs
└── README.md                  # This file
```

---

## 📊 API Endpoints

### Analytics
```
GET  /api/analytics/kpis                    # Get KPIs
GET  /api/analytics/trends/{metric}         # Get trends
GET  /api/analytics/funnel                  # Conversion funnel
GET  /api/analytics/categories              # Category metrics
GET  /api/analytics/traffic/sources         # Traffic sources
GET  /api/analytics/campaigns/performance   # Campaign metrics
```

### Predictions
```
POST /api/predictions/forecast/sales        # Forecast sales
POST /api/predictions/forecast/traffic      # Forecast traffic
GET  /api/predictions/anomalies             # Detect anomalies
POST /api/predictions/churn/predict         # Predict churn
```

### ML Insights
```
POST /api/insights/segment/customers        # Segment customers
GET  /api/insights/segments                 # Get segments
POST /api/insights/recommend/products       # Product recommendations
POST /api/insights/optimize/price           # Price optimization
POST /api/insights/optimize/marketing       # Marketing optimization
```

### Reports
```
POST /api/reports/generate                  # Generate report
GET  /api/reports/list                      # List reports
GET  /api/reports/{id}/download             # Download report
GET  /api/reports/alerts/list               # List alerts
```

---

## 📈 Dashboard Pages

| Page | Description | Key Features |
|------|-------------|--------------|
| **Overview** | Main KPIs & trends | Sales, orders, visitors, conversion |
| **Traffic** | Visitor analytics | Daily trends, sources, new vs returning |
| **Sales** | Revenue metrics | Sales trends, AOV, category breakdown |
| **Campaigns** | Marketing performance | Flash sales, vouchers, ROI |
| **Customer Service** | Support metrics | Response time, CSAT, chat conversion |
| **Products** | Product insights | Top products, cart abandonment |
| **Predictions** | ML forecasts | Sales/traffic forecasting, anomalies |
| **ML Insights** | Advanced analytics | Segmentation, recommendations |

---

## 🔧 Configuration

### Environment Variables

```bash
# Application
APP_NAME=Shopee Analytics Platform
DEBUG=True

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/shopee_analytics

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Data Paths
DATA_PATH=/path/to/cleaned_data
MODEL_PATH=/path/to/ml/models

# ML Settings
FORECAST_DAYS=30
CONFIDENCE_INTERVAL=0.95
```

---

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## 📦 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up SSL/TLS
- [ ] Configure CORS properly
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

---

## 📚 Documentation

- **[Architecture](ARCHITECTURE.md)** - System design and components
- **[API Docs](http://localhost:8000/docs)** - Interactive API documentation
- **[Data Dictionary](../analytical-showdown-pipeline/DATA_DICTIONARY.md)** - Data reference

---

## 🎓 Learning Outcomes

This project demonstrates:

- ✅ Full-stack development (FastAPI + Streamlit)
- ✅ RESTful API design
- ✅ Database design & ORM (SQLAlchemy)
- ✅ ML model integration
- ✅ Data visualization (Plotly)
- ✅ Async programming
- ✅ Docker containerization
- ✅ Business intelligence concepts
- ✅ Real-world data processing

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - Educational Project

---

## 🙏 Acknowledgments

- Data source: Shopee seller analytics
- Built with: FastAPI, Streamlit, Plotly, scikit-learn
- Inspired by: Modern BI platforms

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check documentation
- Review API docs at `/docs`

---

**Built with ❤️ for demonstrating comprehensive analytics platform development**

**Status**: 🚧 In Development | 📊 Dashboard Ready | 🔮 ML Models In Progress
