# 🚀 Nazava Analytics - Streamlit Cloud Deployment Guide

## Quick Deploy (5 Minutes)

### Step 1: Go to Streamlit Cloud
Visit: https://share.streamlit.io/

### Step 2: Sign In
- Click "Sign in with GitHub"
- Authorize Streamlit Cloud to access your repositories

### Step 3: Deploy New App
Click **"New app"** button

### Step 4: Configure Deployment
Fill in these exact values:

```
Repository: taranggoyal70/nazava-analytics
Branch: main
Main file path: dashboard/app.py
```

### Step 5: Deploy!
Click **"Deploy!"** and wait 2-3 minutes

---

## 🎯 Your Live URL
After deployment, your app will be available at:
**https://nazava-analytics.streamlit.app**

Or a similar URL provided by Streamlit Cloud.

---

## 📦 What's Included

✅ **Full Analytics Dashboard**
- Sales forecasting with ML models
- Product performance tracking
- Interactive visualizations
- Real-time data updates

✅ **Authentication System**
- Secure login page
- User management
- Session handling

✅ **Beautiful UI**
- Custom theme (purple/blue gradient)
- Responsive design
- Professional charts with Plotly

---

## 🔐 Default Login Credentials

**Username:** `admin`  
**Password:** `admin123`

**Note:** Change these in production! Edit `dashboard/users.json` to update credentials.

---

## 🛠️ Technical Details

**Python Version:** 3.11  
**Main Dependencies:**
- streamlit >= 1.28.0
- pandas >= 2.0.0
- plotly >= 5.17.0
- scikit-learn >= 1.3.0
- xgboost >= 2.0.0

**Entry Point:** `dashboard/app.py`  
**Config:** `.streamlit/config.toml`

---

## 🎨 Custom Domain (Optional)

To use a custom domain:
1. Go to app settings in Streamlit Cloud
2. Click "Custom domain"
3. Follow the DNS configuration steps

---

## 🐛 Troubleshooting

### App won't start?
- Check that `dashboard/app.py` exists
- Verify all dependencies in `requirements.txt`
- Check Streamlit Cloud logs

### Login not working?
- Ensure `dashboard/users.json` exists
- Check file permissions

### Data not loading?
- Verify data files are in the repository
- Check file paths in the code

---

## 📊 Features

1. **Sales Analytics**
   - Historical sales trends
   - Revenue forecasting
   - Product performance metrics

2. **ML Forecasting**
   - XGBoost models
   - 6-month predictions
   - Accuracy metrics

3. **Interactive Dashboards**
   - Filterable charts
   - Export capabilities
   - Real-time updates

---

## 🔄 Updates

To update your deployed app:
1. Push changes to GitHub (`git push origin main`)
2. Streamlit Cloud auto-deploys within 1-2 minutes
3. No manual redeployment needed!

---

## 📞 Support

- **Streamlit Docs:** https://docs.streamlit.io/
- **Community Forum:** https://discuss.streamlit.io/
- **GitHub Issues:** https://github.com/taranggoyal70/nazava-analytics/issues

---

**Happy Deploying! 🎉**
