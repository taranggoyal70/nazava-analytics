# Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the dashboard:
```bash
cd dashboard
streamlit run app.py
```

Login: `admin` / `admin123`

Data files are in `data/cleaned/` and load automatically.

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
