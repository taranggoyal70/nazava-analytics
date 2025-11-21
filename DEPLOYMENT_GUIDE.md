# Deployment Guide

## Deploy to Streamlit Cloud

Your code is ready to deploy. Follow these steps:

### Step 1: Go to Streamlit Cloud

Open: https://share.streamlit.io/

### Step 2: Sign In

Click "Sign in with GitHub" and authorize Streamlit Cloud.

### Step 3: Deploy New App

1. Click "New app" button
2. Fill in the details:
   - Repository: `taranggoyal70/nazava-analytics`
   - Branch: `main`
   - Main file path: `dashboard/app.py`
   - App URL: Choose a custom name (e.g., `nazava-analytics`)

### Step 4: Advanced Settings (Optional)

If you want Google OAuth login, add these secrets:

```toml
GOOGLE_CLIENT_ID = "your_client_id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your_client_secret"
GOOGLE_REDIRECT_URI = "https://your-app-name.streamlit.app"
```

Get credentials from: https://console.cloud.google.com/apis/credentials

### Step 5: Deploy

Click "Deploy!" button.

Your app will be live in 3-5 minutes at:
`https://your-app-name.streamlit.app`

---

## Demo Mode

Without Google OAuth configured, the app runs in demo mode:
- Username: `admin`
- Password: `admin123`

---

## Troubleshooting

### Build Fails

Check the build logs in Streamlit Cloud dashboard. Common issues:
- Missing dependencies in `requirements.txt`
- Python version mismatch
- File path errors

### App Crashes

Check the app logs. Usually caused by:
- Missing data files (expected - app uses demo data)
- Environment variable issues
- Import errors

### Can't Access App

- Wait 5 minutes for initial deployment
- Check if build completed successfully
- Try clearing browser cache
- Check app logs for errors

---

## Update Deployed App

Any push to GitHub main branch will auto-deploy:

```bash
git add .
git commit -m "Update message"
git push origin main
```

Streamlit Cloud will automatically rebuild and redeploy.

---

## Alternative Deployment Options

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: streamlit run dashboard/app.py --server.port=$PORT
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Railway

1. Go to https://railway.app
2. Connect GitHub repo
3. Set start command: `streamlit run dashboard/app.py`
4. Deploy

### Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run dashboard/app.py`

---

## Current Status

- GitHub: https://github.com/taranggoyal70/nazava-analytics
- Local: http://localhost:8501
- Ready for cloud deployment
