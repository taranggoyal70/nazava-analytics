"""
Data cleaning utilities for handling European number formats
"""

import pandas as pd
import re

def clean_european_number(value):
    """
    Convert European number format to standard format
    European: 1.234,56 (period as thousands, comma as decimal)
    Standard: 1234.56
    
    Args:
        value: String or numeric value
    
    Returns:
        float: Cleaned numeric value
    """
    if pd.isna(value):
        return 0.0
    
    # If already a number, return it
    if isinstance(value, (int, float)):
        return float(value)
    
    # Convert to string
    value_str = str(value).strip()
    
    # Remove any whitespace
    value_str = value_str.replace(' ', '')
    
    # Check if it's European format (has period as thousands separator)
    # European format: 1.234 or 1.234,56
    # Standard format: 1234 or 1234.56
    
    # If has both period and comma, it's European format
    if '.' in value_str and ',' in value_str:
        # Remove periods (thousands separator)
        value_str = value_str.replace('.', '')
        # Replace comma with period (decimal separator)
        value_str = value_str.replace(',', '.')
    # If has only period and looks like thousands (e.g., 1.234)
    elif '.' in value_str:
        # Check if it's likely a thousands separator
        # If the period is followed by exactly 3 digits, it's likely thousands
        if re.match(r'^\d{1,3}(\.\d{3})+$', value_str):
            # Remove periods (thousands separator)
            value_str = value_str.replace('.', '')
        # Otherwise it's a decimal point, keep it
    # If has only comma, replace with period (decimal separator)
    elif ',' in value_str:
        value_str = value_str.replace(',', '.')
    
    try:
        return float(value_str)
    except (ValueError, TypeError):
        return 0.0


def clean_dataframe_numbers(df, columns):
    """
    Clean European number format in specified columns of a DataFrame
    
    Args:
        df: pandas DataFrame
        columns: list of column names to clean
    
    Returns:
        DataFrame with cleaned numeric columns
    """
    df_clean = df.copy()
    
    for col in columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].apply(clean_european_number)
    
    return df_clean


def auto_clean_numeric_columns(df):
    """
    Automatically detect and clean all numeric columns in a DataFrame
    
    Args:
        df: pandas DataFrame
    
    Returns:
        DataFrame with all numeric columns cleaned
    """
    df_clean = df.copy()
    
    for col in df_clean.columns:
        # Skip date columns
        if 'date' in col.lower() or col.lower() in ['source_file', 'category', 'processed_date']:
            continue
        
        # Try to clean the column
        try:
            # Check if column might contain numbers
            sample = df_clean[col].dropna().head(10)
            if len(sample) > 0:
                # Check if any value contains digits
                has_digits = any(str(val) for val in sample if re.search(r'\d', str(val)))
                if has_digits:
                    df_clean[col] = df_clean[col].apply(clean_european_number)
        except:
            # If cleaning fails, skip this column
            continue
    
    return df_clean
