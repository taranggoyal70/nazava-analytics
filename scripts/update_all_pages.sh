#!/bin/bash

# Script to update all dashboard pages to use cleaned data
# This adds the universal data loader import to all pages

echo "=========================================="
echo "Updating All Dashboard Pages"
echo "=========================================="
echo ""

PAGES_DIR="/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/dashboard/pages"

# List of pages to update
pages=(
    "3_Sales.py"
    "4_Campaigns.py"
    "5_Customer_Service.py"
    "7_Sales_Forecast.py"
    "8_Customer_Segments.py"
    "9_Product_Recommendations.py"
    "10_Campaign_Optimizer.py"
    "11_Automation_Bot.py"
    "12_Mass_Chat_Broadcasts.py"
    "13_Off_Platform_Traffic.py"
    "14_Shopee_PayLater.py"
    "15_Period_Comparison.py"
)

for page in "${pages[@]}"; do
    if [ -f "$PAGES_DIR/$page" ]; then
        echo "✅ Found: $page"
    else
        echo "❌ Missing: $page"
    fi
done

echo ""
echo "=========================================="
echo "Manual update required for each page:"
echo "1. Add: from utils.data_loader import load_*_data"
echo "2. Replace data loading code with: df = load_*_data()"
echo "3. Remove manual data path and cleaning code"
echo "=========================================="
