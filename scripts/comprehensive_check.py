"""
Comprehensive check for all dashboard pages
Identifies small issues, bugs, and improvements needed
"""

import pandas as pd
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from dashboard.utils.data_loader import *

def check_all_issues():
    """Check for common issues across all data sources"""
    
    print("="*70)
    print("COMPREHENSIVE DASHBOARD ISSUE CHECK")
    print("="*70)
    print()
    
    issues = []
    warnings_list = []
    
    # 1. Check Traffic Data
    print("1️⃣  Checking Traffic Data...")
    try:
        traffic_df = load_traffic_data()
        
        # Check for string columns that should be numeric
        for col in ['Total_Visitors', 'New_Visitors', 'Returning_Visitors', 'Average_Views']:
            if col in traffic_df.columns and traffic_df[col].dtype == 'object':
                issues.append(f"❌ Traffic: {col} is string type")
        
        # Check for negative values
        if (traffic_df['Total_Visitors'] < 0).any():
            issues.append("❌ Traffic: Negative visitor counts found")
        
        # Check for NaN in critical columns
        if traffic_df['Total_Visitors'].isna().any():
            warnings_list.append("⚠️  Traffic: NaN values in Total_Visitors")
        
        print(f"   ✅ Loaded {len(traffic_df)} rows")
        print(f"   Total Visitors: {traffic_df['Total_Visitors'].sum():,.0f}")
        
    except Exception as e:
        issues.append(f"❌ Traffic: {str(e)}")
    
    print()
    
    # 2. Check Product Data
    print("2️⃣  Checking Product Data...")
    try:
        product_df = load_product_data()
        
        # Check for string columns
        sales_col = 'Total Sales (Orders Created) (IDR)'
        if sales_col in product_df.columns and product_df[sales_col].dtype == 'object':
            issues.append(f"❌ Product: Sales column is string type")
        
        # Check for negative sales
        if sales_col in product_df.columns:
            if (product_df[sales_col] < 0).any():
                issues.append("❌ Product: Negative sales found")
        
        print(f"   ✅ Loaded {len(product_df)} rows")
        
    except Exception as e:
        issues.append(f"❌ Product: {str(e)}")
    
    print()
    
    # 3. Check Chat Data (CSAT)
    print("3️⃣  Checking Chat Data (CSAT)...")
    try:
        chat_df = load_chat_data()
        
        # Check CSAT range
        if 'CSAT_Percent' in chat_df.columns:
            avg_csat = chat_df['CSAT_Percent'].mean()
            if avg_csat < 50 or avg_csat > 100:
                issues.append(f"❌ Chat: CSAT out of range (0-100): {avg_csat:.1f}%")
            elif avg_csat < 2:
                issues.append(f"❌ Chat: CSAT too low, might need *100: {avg_csat:.1f}%")
            else:
                print(f"   ✅ CSAT: {avg_csat:.1f}% (within range)")
        
        print(f"   ✅ Loaded {len(chat_df)} rows")
        
    except Exception as e:
        issues.append(f"❌ Chat: {str(e)}")
    
    print()
    
    # 4. Check Flash Sale Data
    print("4️⃣  Checking Flash Sale Data...")
    try:
        flash_df = load_flash_sale_data()
        
        # Check for negative sales
        if 'Sales_Ready_To_Ship_IDR' in flash_df.columns:
            if (pd.to_numeric(flash_df['Sales_Ready_To_Ship_IDR'], errors='coerce') < 0).any():
                issues.append("❌ Flash Sale: Negative sales found")
        
        print(f"   ✅ Loaded {len(flash_df)} rows")
        
    except Exception as e:
        issues.append(f"❌ Flash Sale: {str(e)}")
    
    print()
    
    # 5. Check Off-Platform Data
    print("5️⃣  Checking Off-Platform Data...")
    try:
        off_df = load_off_platform_data()
        
        # Check for header rows
        if 'Platform' in off_df.columns:
            if (off_df['Platform'] == 'Platform').any():
                issues.append("❌ Off-Platform: Header rows not removed")
        
        # Check for string visitors
        if 'Visitors' in off_df.columns and off_df['Visitors'].dtype == 'object':
            issues.append("❌ Off-Platform: Visitors is string type")
        
        print(f"   ✅ Loaded {len(off_df)} rows")
        
    except Exception as e:
        issues.append(f"❌ Off-Platform: {str(e)}")
    
    print()
    
    # 6. Check Mass Chat Data
    print("6️⃣  Checking Mass Chat Data...")
    try:
        mass_chat_df = load_mass_chat_data()
        
        # Check for rate columns (should be 0-100 or 0-1)
        for col in ['Read_Rate', 'Click_Rate']:
            if col in mass_chat_df.columns:
                max_val = mass_chat_df[col].max()
                if max_val > 100:
                    warnings_list.append(f"⚠️  Mass Chat: {col} > 100 ({max_val})")
        
        print(f"   ✅ Loaded {len(mass_chat_df)} rows")
        
    except Exception as e:
        issues.append(f"❌ Mass Chat: {str(e)}")
    
    print()
    
    # 7. Check PayLater Data
    print("7️⃣  Checking PayLater Data...")
    try:
        paylater_df = load_paylater_data()
        
        # Check for header rows
        if 'Periode Data' in paylater_df.columns:
            if (paylater_df['Periode Data'] == 'Periode Data').any():
                issues.append("❌ PayLater: Header rows not removed")
        
        print(f"   ✅ Loaded {len(paylater_df)} rows")
        
    except Exception as e:
        issues.append(f"❌ PayLater: {str(e)}")
    
    print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    
    if not issues and not warnings_list:
        print("🎉 NO ISSUES FOUND! Dashboard is in excellent condition!")
    else:
        if issues:
            print(f"❌ CRITICAL ISSUES ({len(issues)}):")
            for issue in issues:
                print(f"   {issue}")
            print()
        
        if warnings_list:
            print(f"⚠️  WARNINGS ({len(warnings_list)}):")
            for warning in warnings_list:
                print(f"   {warning}")
            print()
    
    # Recommendations
    print("="*70)
    print("RECOMMENDATIONS")
    print("="*70)
    print()
    
    if issues:
        print("🔧 FIXES NEEDED:")
        print("   1. Update data_loader.py to handle all edge cases")
        print("   2. Add data validation in loaders")
        print("   3. Ensure all numeric columns are properly typed")
        print()
    
    print("💡 IMPROVEMENTS:")
    print("   1. Add error handling in dashboard pages")
    print("   2. Add data quality checks before display")
    print("   3. Add user-friendly error messages")
    print("   4. Add data refresh timestamp")
    print()
    
    return issues, warnings_list

if __name__ == "__main__":
    issues, warnings = check_all_issues()
    
    # Exit code
    if issues:
        sys.exit(1)
    else:
        sys.exit(0)
