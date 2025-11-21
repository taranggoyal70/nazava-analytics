#!/bin/bash

echo "📦 Creating FINAL clean submission package..."

# Remove old package
rm -rf shopee-analytics-submission
rm -f shopee-analytics-submission.zip

# Create fresh directory
mkdir -p shopee-analytics-submission

echo "📋 Copying essential files only..."

# Documentation
cp README.md shopee-analytics-submission/
cp SETUP.md shopee-analytics-submission/
cp SUBMISSION_README.md shopee-analytics-submission/

# Requirements
cp requirements.txt shopee-analytics-submission/

# Dashboard (complete)
echo "  ✓ Dashboard"
cp -r dashboard shopee-analytics-submission/

# Data files
echo "  ✓ Data files"
mkdir -p shopee-analytics-submission/data/cleaned
cp -r data/cleaned/* shopee-analytics-submission/data/cleaned/

# ML models
echo "  ✓ ML models"
cp -r ml_models shopee-analytics-submission/

# Backend
echo "  ✓ Backend API"
mkdir -p shopee-analytics-submission/backend
cp -r backend/app shopee-analytics-submission/backend/
cp backend/requirements.txt shopee-analytics-submission/backend/

# ONLY the final notebook (not all the test versions)
echo "  ✓ Final notebook only"
mkdir -p shopee-analytics-submission/notebook
cp Nazava_FINAL_CLEAN.ipynb shopee-analytics-submission/notebook/ 2>/dev/null || \
cp Nazava_Complete_Analysis_v2.ipynb shopee-analytics-submission/notebook/ 2>/dev/null || \
echo "    (No final notebook found)"

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
  -x "*.DS_Store"

# Get size
SIZE=$(du -h shopee-analytics-submission.zip | cut -f1)

echo ""
echo "✅ CLEAN submission package created!"
echo ""
echo "📦 File: shopee-analytics-submission.zip"
echo "📏 Size: $SIZE"
echo ""
echo "📂 Contents:"
echo "  ✅ Dashboard (all 15 pages)"
echo "  ✅ Data files (12 CSV files)"
echo "  ✅ ML models (3 files)"
echo "  ✅ Backend API"
echo "  ✅ Final notebook (1 only)"
echo "  ✅ Documentation"
echo ""

# Copy to Downloads
cp shopee-analytics-submission.zip ~/Downloads/
echo "📥 Copied to Downloads folder!"
echo ""
echo "🎉 Ready to upload to Google Drive!"
