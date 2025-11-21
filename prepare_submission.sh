#!/bin/bash

# Prepare submission package for Google Drive upload

echo "📦 Preparing Shopee Analytics submission package..."

# Create submission directory
SUBMISSION_DIR="shopee-analytics-submission"
rm -rf $SUBMISSION_DIR
mkdir -p $SUBMISSION_DIR

echo "📋 Copying essential files..."

# Copy main files
cp README.md $SUBMISSION_DIR/
cp SETUP.md $SUBMISSION_DIR/
cp SUBMISSION_README.md $SUBMISSION_DIR/README_SUBMISSION.md
cp requirements.txt $SUBMISSION_DIR/
cp -r dashboard $SUBMISSION_DIR/

# Copy data (only essential files)
mkdir -p $SUBMISSION_DIR/data
cp data/*.csv $SUBMISSION_DIR/data/ 2>/dev/null || echo "No CSV files to copy"

# Copy ML models and notebooks (selective)
mkdir -p $SUBMISSION_DIR/ml
cp -r ml_models $SUBMISSION_DIR/ 2>/dev/null || echo "No ml_models directory"
cp ml/*.py $SUBMISSION_DIR/ml/ 2>/dev/null || echo "No ML scripts"

# Copy backend (optional)
mkdir -p $SUBMISSION_DIR/backend
cp -r backend/app $SUBMISSION_DIR/backend/ 2>/dev/null || echo "No backend app"
cp backend/requirements.txt $SUBMISSION_DIR/backend/ 2>/dev/null || echo "No backend requirements"

# Create .env.example
cat > $SUBMISSION_DIR/.env.example << 'EOF'
# Google OAuth (Optional)
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here

# Database (Optional)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
EOF

echo "🗜️  Creating zip file..."

# Create zip file
zip -r shopee-analytics-submission.zip $SUBMISSION_DIR -x "*.pyc" -x "*__pycache__*" -x "*.git*" -x "*node_modules*" -x "*.DS_Store"

echo "✅ Submission package created!"
echo ""
echo "📦 File: shopee-analytics-submission.zip"
echo "📏 Size: $(du -h shopee-analytics-submission.zip | cut -f1)"
echo ""
echo "📤 Ready to upload to Google Drive!"
echo ""
echo "To upload:"
echo "1. Open Google Drive in your browser"
echo "2. Click 'New' → 'File upload'"
echo "3. Select: shopee-analytics-submission.zip"
echo "4. Share the link with your instructor"
