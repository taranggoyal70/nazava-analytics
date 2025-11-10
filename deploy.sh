#!/bin/bash

echo "========================================"
echo "  Nazava Analytics Dashboard Startup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "Please run this script from the shopee-analytics-platform directory"
    exit 1
fi
echo ""
echo "📦 Committing changes..."
git add .
git commit -m "Prepare for deployment" || echo "No changes to commit"

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ CODE PUSHED TO GITHUB!"
echo ""
echo "🎯 NEXT STEPS:"
echo ""
echo "1. Go to: https://share.streamlit.io/"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository: $username/nazava-analytics"
echo "5. Main file: dashboard/app.py"
echo "6. Add secrets (Advanced settings):"
echo "   GOOGLE_CLIENT_ID = \"YOUR_CLIENT_ID_HERE.apps.googleusercontent.com\""
echo "   GOOGLE_CLIENT_SECRET = \"YOUR_CLIENT_SECRET_HERE\""
echo "   (Get from: https://console.cloud.google.com/apis/credentials)"
echo "7. Click 'Deploy!'"
echo ""
echo "🎉 Your dashboard will be live in ~5 minutes!"
