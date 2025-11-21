#!/bin/bash

echo "🚀 NAZAVA ANALYTICS - DEPLOYMENT HELPER"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo "📝 GitHub Setup Required:"
    echo ""
    echo "1. Create a new repository on GitHub:"
    echo "   https://github.com/new"
    echo ""
    echo "2. Name it: nazava-analytics"
    echo ""
    echo "3. Then run:"
    read -p "   Enter your GitHub username: " username
    git remote add origin https://github.com/$username/nazava-analytics.git
    echo "✅ Remote added!"
fi

# Commit any changes
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
