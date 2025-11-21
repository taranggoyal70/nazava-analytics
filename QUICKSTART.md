# 🚀 Quick Start Guide

Get the Shopee Analytics Platform running in 5 minutes!

---

## ⚡ Super Quick Start (Streamlit Dashboard Only)

If you just want to see the dashboard with your data:

```bash
# 1. Navigate to dashboard
cd shopee-analytics-platform/dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run dashboard
streamlit run app.py
```

**That's it!** Open http://localhost:8501 in your browser.

---

## 🐳 Docker Quick Start (Full Platform)

Run the complete platform with all components:

```bash
# 1. Navigate to project
cd shopee-analytics-platform

# 2. Start all services
docker-compose up -d

# 3. Wait for services to be ready (~30 seconds)
docker-compose logs -f

# 4. Access applications
# Dashboard: http://localhost:8501
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

To stop:
```bash
docker-compose down
```

---

## 💻 Manual Setup (Development)

### Prerequisites
- Python 3.11+
- PostgreSQL 14+ (optional for full features)
- Redis 7+ (optional for caching)

### Step 1: Install Backend

```bash
cd shopee-analytics-platform/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example ../.env

# Edit .env if needed
nano ../.env
```

### Step 2: Install Dashboard

```bash
cd ../dashboard

# Install dependencies (in same venv)
pip install -r requirements.txt
```

### Step 3: Run Services

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Dashboard:**
```bash
cd dashboard
streamlit run app.py
```

### Step 4: Access

- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000/api

---

## 📊 What You'll See

### Dashboard Pages

1. **Overview** - Main KPIs and trends
2. **Traffic** - Visitor analytics
3. **Sales** - Revenue metrics
4. **Campaigns** - Marketing performance
5. **Customer Service** - Support metrics
6. **Products** - Product insights
7. **Predictions** - ML forecasts
8. **ML Insights** - Advanced analytics

### Sample Data

The platform uses your cleaned data from:
```
analytical-showdown-pipeline/cleaned_data/
```

Make sure you've run the data cleaning pipeline first!

---

## 🔧 Troubleshooting

### Issue: "Module not found"
```bash
# Make sure you're in the right directory and venv is activated
pip install -r requirements.txt
```

### Issue: "Connection refused" (Backend)
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start it:
cd backend
uvicorn app.main:app --reload
```

### Issue: "Data not loading"
```bash
# Verify data path in .env
DATA_PATH=/path/to/analytical-showdown-pipeline/cleaned_data

# Check if CSV files exist
ls -la $DATA_PATH
```

### Issue: "Port already in use"
```bash
# Find process using port
lsof -i :8501  # or :8000

# Kill process
kill -9 <PID>

# Or use different port
streamlit run app.py --server.port 8502
```

---

## 🎯 Next Steps

1. **Explore Dashboard** - Navigate through all pages
2. **Try API** - Visit http://localhost:8000/docs
3. **Customize** - Modify dashboard pages in `dashboard/pages/`
4. **Add Features** - Extend API endpoints in `backend/app/api/`
5. **Train Models** - Run ML notebooks in `ml/notebooks/`

---

## 📚 Learn More

- **[README.md](README.md)** - Full documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design
- **[API Docs](http://localhost:8000/docs)** - Interactive API reference

---

## ✅ Verification Checklist

- [ ] Dashboard loads at http://localhost:8501
- [ ] Overview page shows KPIs
- [ ] Charts render correctly
- [ ] API responds at http://localhost:8000/health
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] No errors in terminal logs

---

**Need Help?** Check the troubleshooting section or open an issue!

**Happy Analyzing! 📊**
