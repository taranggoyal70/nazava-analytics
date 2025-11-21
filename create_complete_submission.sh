#!/bin/bash

echo "📦 Creating COMPLETE submission package with all files..."

# Remove old package
rm -rf shopee-analytics-submission
rm -f shopee-analytics-submission.zip

# Create fresh directory
mkdir -p shopee-analytics-submission

echo "📋 Copying all essential files..."

# Main files
cp README.md shopee-analytics-submission/
cp SETUP.md shopee-analytics-submission/
cp SUBMISSION_README.md shopee-analytics-submission/
cp requirements.txt shopee-analytics-submission/

# Dashboard (complete)
cp -r dashboard shopee-analytics-submission/

# Data files (IMPORTANT!)
mkdir -p shopee-analytics-submission/data/cleaned
cp -r data/cleaned/* shopee-analytics-submission/data/cleaned/

# ML models
cp -r ml_models shopee-analytics-submission/ 2>/dev/null || true

# Backend
mkdir -p shopee-analytics-submission/backend
cp -r backend/app shopee-analytics-submission/backend/ 2>/dev/null || true
cp backend/requirements.txt shopee-analytics-submission/backend/ 2>/dev/null || true

# Notebooks (if you want to include them)
mkdir -p shopee-analytics-submission/notebooks
cp *.ipynb shopee-analytics-submission/notebooks/ 2>/dev/null || true

# .env example
cat > shopee-analytics-submission/.env.example << 'EOF'
# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
EOF

echo "🗜️  Creating zip file..."

# Create zip
zip -r shopee-analytics-submission.zip shopee-analytics-submission \
  -x "*.pyc" \
  -x "*__pycache__*" \
  -x "*.git*" \
  -x "*node_modules*" \
  -x "*.DS_Store" \
  -x "*/.ipynb_checkpoints/*"

# Get size
SIZE=$(du -h shopee-analytics-submission.zip | cut -f1)

echo ""
echo "✅ COMPLETE submission package created!"
echo ""
echo "📦 File: shopee-analytics-submission.zip"
echo "📏 Size: $SIZE"
echo ""
echo "📂 Contents:"
echo "  ✅ Dashboard (all 15 pages)"
echo "  ✅ Data files (12 CSV files)"
echo "  ✅ ML models"
echo "  ✅ Backend API"
echo "  ✅ Notebooks"
echo "  ✅ Documentation"
echo ""

# Copy to Downloads
cp shopee-analytics-submission.zip ~/Downloads/
echo "📥 Copied to Downloads folder!"
echo ""
echo "🎉 Ready to upload to Google Drive!"
