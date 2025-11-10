"""
Script to check all dashboard pages for data consistency
Compares with Jupyter notebook expected values
"""

import pandas as pd
import sys
from pathlib import Path

# Add parent to path
sys.path.append(str(Path(__file__).parent.parent))

from dashboard.utils.data_loader import (
    load_traffic_data,
    load_product_data,
    load_chat_data,
    load_flash_sale_data,
    load_voucher_data,
    load_game_data,
    load_live_data,
    load_mass_chat_data,
    load_off_platform_data,
    load_paylater_data
)

def check_data_quality():
    """Check all data sources for quality issues"""
    
    print("="*60)
    print("DASHBOARD DATA QUALITY CHECK")
    print("="*60)
    print()
    
    results = {}
    
    # 1. Traffic Data
    print("1. Checking Traffic Data...")
    try:
        traffic_df = load_traffic_data()
        results['traffic'] = {
            'status': 'OK',
            'rows': len(traffic_df),
            'total_visitors': traffic_df['Total_Visitors'].sum(),
            'date_range': f"{traffic_df['Date'].min().date()} to {traffic_df['Date'].max().date()}",
            'issues': []
        }
        
        # Check for string columns that should be numeric
        for col in ['Total_Visitors', 'New_Visitors', 'Returning_Visitors', 'Average_Views']:
            if col in traffic_df.columns:
                if traffic_df[col].dtype == 'object':
                    results['traffic']['issues'].append(f"{col} is string, should be numeric")
        
        print(f"   ✅ Loaded {len(traffic_df)} rows")
        print(f"   Total Visitors: {traffic_df['Total_Visitors'].sum():,.0f}")
        
    except Exception as e:
        results['traffic'] = {'status': 'ERROR', 'error': str(e)}
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 2. Product Data
    print("2. Checking Product Data...")
    try:
        product_df = load_product_data()
        total_sales = product_df['Total Sales (Orders Created) (IDR)'].sum()
        results['product'] = {
            'status': 'OK',
            'rows': len(product_df),
            'total_sales': total_sales,
            'date_range': f"{product_df['Date'].min().date()} to {product_df['Date'].max().date()}",
            'issues': []
        }
        print(f"   ✅ Loaded {len(product_df)} rows")
        print(f"   Total Sales: IDR {total_sales/1e6:.1f}M")
        
    except Exception as e:
        results['product'] = {'status': 'ERROR', 'error': str(e)}
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 3. Chat Data
    print("3. Checking Chat Data...")
    try:
        chat_df = load_chat_data()
        total_sales = pd.to_numeric(chat_df['Sales_IDR'], errors='coerce').sum()
        avg_csat = pd.to_numeric(chat_df['CSAT_Percent'], errors='coerce').mean()
        results['chat'] = {
            'status': 'OK',
            'rows': len(chat_df),
            'total_sales': total_sales,
            'avg_csat': avg_csat,
            'issues': []
        }
        print(f"   ✅ Loaded {len(chat_df)} rows")
        print(f"   Total Sales: IDR {total_sales/1e6:.1f}M")
        print(f"   Avg CSAT: {avg_csat:.1f}%")
        
    except Exception as e:
        results['chat'] = {'status': 'ERROR', 'error': str(e)}
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 4. Flash Sale Data
    print("4. Checking Flash Sale Data...")
    try:
        flash_df = load_flash_sale_data()
        total_sales = pd.to_numeric(flash_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
        results['flash_sale'] = {
            'status': 'OK',
            'rows': len(flash_df),
            'total_sales': total_sales,
            'issues': []
        }
        print(f"   ✅ Loaded {len(flash_df)} rows")
        print(f"   Total Sales: IDR {total_sales/1e6:.1f}M")
        
    except Exception as e:
        results['flash_sale'] = {'status': 'ERROR', 'error': str(e)}
        print(f"   ❌ Error: {e}")
    
    print()
    
    # 5. Off-Platform Data
    print("5. Checking Off-Platform Data...")
    try:
        off_df = load_off_platform_data()
        total_visitors = off_df['Visitors'].sum()
        results['off_platform'] = {
            'status': 'OK',
            'rows': len(off_df),
            'total_visitors': total_visitors,
            'issues': []
        }
        print(f"   ✅ Loaded {len(off_df)} rows")
        print(f"   Total Visitors: {total_visitors:,.0f}")
        
    except Exception as e:
        results['off_platform'] = {'status': 'ERROR', 'error': str(e)}
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Summary
    print("="*60)
    print("SUMMARY")
    print("="*60)
    
    ok_count = sum(1 for r in results.values() if r.get('status') == 'OK')
    error_count = sum(1 for r in results.values() if r.get('status') == 'ERROR')
    
    print(f"\n✅ OK: {ok_count}")
    print(f"❌ Errors: {error_count}")
    
    # Key Metrics
    print("\n" + "="*60)
    print("KEY METRICS (vs Notebook)")
    print("="*60)
    
    if 'traffic' in results and results['traffic']['status'] == 'OK':
        print(f"\nTotal Visitors: {results['traffic']['total_visitors']:,.0f}")
        print(f"  Expected: ~125,000")
        print(f"  Match: {'✅' if 100000 < results['traffic']['total_visitors'] < 150000 else '❌'}")
    
    if 'chat' in results and results['chat']['status'] == 'OK':
        print(f"\nAvg CSAT: {results['chat']['avg_csat']:.1f}%")
        print(f"  Expected: ~94.2%")
        print(f"  Match: {'✅' if 90 < results['chat']['avg_csat'] < 98 else '❌'}")
    
    # Combined sales
    total_sales = 0
    if 'chat' in results and results['chat']['status'] == 'OK':
        total_sales += results['chat']['total_sales']
    if 'flash_sale' in results and results['flash_sale']['status'] == 'OK':
        total_sales += results['flash_sale']['total_sales']
    
    if total_sales > 0:
        print(f"\nTotal Sales (Chat + Flash): IDR {total_sales/1e9:.2f}B")
        print(f"  Expected: ~IDR 0.65B (for available data)")
        print(f"  Match: {'✅' if 0.5e9 < total_sales < 1.0e9 else '❌'}")
    
    print("\n" + "="*60)
    
    return results

if __name__ == "__main__":
    results = check_data_quality()
