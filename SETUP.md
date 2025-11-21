# Setup Guide

## Requirements

- Python 3.11+
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Running the Dashboard

```bash
cd dashboard
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Google OAuth (Optional)

If you want to enable Google login:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add to `.env`:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_secret
   ```

## Demo Mode

Without OAuth configured, the app runs in demo mode with sample data.
