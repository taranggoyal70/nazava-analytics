"""
Comprehensive Data Cleaning Script
Fixes European number formats in ALL dataset files
"""

import pandas as pd
import re
import os
from pathlib import Path

def clean_european_number(value):
    """
    Convert European number format to standard format
    Handles: 1.234 → 1234, 1.234,56 → 1234.56
    """
    if pd.isna(value):
        return value
    
    if isinstance(value, (int, float)):
        return float(value)
    
    value_str = str(value).strip()
    value_str = value_str.replace(' ', '')
    
    # If has both period and comma, it's European format
    if '.' in value_str and ',' in value_str:
        value_str = value_str.replace('.', '').replace(',', '.')
    # If has only period and looks like thousands (e.g., 1.234)
    elif '.' in value_str:
        if re.match(r'^\d{1,3}(\.\d{3})+$', value_str):
            value_str = value_str.replace('.', '')
    # If has only comma, replace with period
    elif ',' in value_str:
        value_str = value_str.replace(',', '.')
    
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return value  # Return original if can't convert

def clean_dataframe(df, skip_columns=None):
    """
    Clean all numeric columns in a DataFrame
    """
    if skip_columns is None:
        skip_columns = ['Date', 'Time_Period', 'Source_File', 'Category', 'Processed_Date', 
                       'Platform', 'Channel', 'Tenor', 'Periode Data', 'Data_Period']
    
    df_clean = df.copy()
    
    for col in df_clean.columns:
        # Skip non-numeric columns
        if any(skip in col for skip in skip_columns):
            continue
        
        # Try to clean the column
        try:
            df_clean[col] = df_clean[col].apply(clean_european_number)
        except:
            continue
    
    return df_clean

def process_file(file_path, output_path):
    """
    Process a single CSV file
    """
    print(f"Processing: {file_path.name}")
    
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Skip empty or header-only rows
        df = df.dropna(how='all')
        
        # Clean the data
        df_clean = clean_dataframe(df)
        
        # Save cleaned data
        df_clean.to_csv(output_path, index=False)
        
        print(f"  ✅ Cleaned and saved to: {output_path.name}")
        print(f"  Rows: {len(df_clean)}, Columns: {len(df_clean.columns)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    """
    Main function to process all data files
    """
    # Paths
    data_dir = Path("/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data")
    output_dir = Path("/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/data/cleaned")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to process
    files_to_process = [
        'traffic_overview_cleaned.csv',
        'product_overview_cleaned.csv',
        'chat_data_cleaned.csv',
        'flash_sale_cleaned.csv',
        'voucher_cleaned.csv',
        'game_cleaned.csv',
        'live_cleaned.csv',
        'mass_chat_data_cleaned.csv',
        'off_platform_cleaned.csv',
        'shopee_paylater_cleaned.csv',
        'revenue_2_cleaned.csv'
    ]
    
    print("=" * 60)
    print("COMPREHENSIVE DATA CLEANING")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for filename in files_to_process:
        file_path = data_dir / filename
        output_path = output_dir / filename
        
        if file_path.exists():
            if process_file(file_path, output_path):
                success_count += 1
            else:
                fail_count += 1
        else:
            print(f"⚠️  File not found: {filename}")
            fail_count += 1
        
        print()
    
    print("=" * 60)
    print(f"SUMMARY: ✅ {success_count} successful, ❌ {fail_count} failed")
    print("=" * 60)
    print()
    print(f"Cleaned data saved to: {output_dir}")
    print()
    
    # Create a summary report
    summary_path = output_dir / "cleaning_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("Data Cleaning Summary\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total files processed: {success_count + fail_count}\n")
        f.write(f"Successful: {success_count}\n")
        f.write(f"Failed: {fail_count}\n\n")
        f.write("Cleaning applied:\n")
        f.write("- European number format conversion (1.234 → 1234)\n")
        f.write("- Decimal separator normalization (1,5 → 1.5)\n")
        f.write("- Whitespace removal\n")
        f.write("- Empty row removal\n")
    
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
