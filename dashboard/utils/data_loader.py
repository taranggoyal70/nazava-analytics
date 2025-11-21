"""
Universal Data Loader
Loads cleaned data with proper formatting for all dashboard pages
"""

import pandas as pd
import streamlit as st
from pathlib import Path
import os

# Get the project root directory (works both locally and on Streamlit Cloud)
DASHBOARD_DIR = Path(__file__).parent.parent
PROJECT_ROOT = DASHBOARD_DIR.parent

# Try multiple possible data paths
def get_data_path():
    """Get the appropriate data path (use cleaned if available, otherwise original)"""
    possible_paths = [
        PROJECT_ROOT / "data" / "cleaned",
        Path("/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"),
        PROJECT_ROOT / ".." / "analytical-showdown-pipeline" / "cleaned_data",
        DASHBOARD_DIR / "sample_data",  # Fallback to sample data in dashboard
    ]
    
    for path in possible_paths:
        if path.exists() and any(path.glob("*.csv")):
            return path
    
    # If no data found, return first path (will generate sample data)
    return possible_paths[0]

@st.cache_data
def load_traffic_data():
    """
    Load traffic overview data
    Returns: DataFrame with Date as datetime and numeric columns
    """
    data_path = get_data_path()
    # Try processed first, then cleaned
    if (data_path / "traffic_overview_processed.csv").exists():
        df = pd.read_csv(data_path / "traffic_overview_processed.csv")
    else:
        df = pd.read_csv(data_path / "traffic_overview_cleaned.csv")
    
    # Convert date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
    
    # Ensure ALL numeric columns are properly typed
    numeric_cols = ['Total_Visitors', 'New_Visitors', 'Returning_Visitors', 'New_Followers', 
                   'Products_Viewed', 'Average_Views', 'Average_Time_Spent', 
                   'Rate_Visitors_Viewing_Without_Buying']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

@st.cache_data
def load_product_data():
    """
    Load product overview data
    Returns: DataFrame with Date as datetime and numeric columns
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "product_overview_cleaned.csv")
    
    # Convert date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
    
    # Ensure key numeric columns are properly typed
    numeric_cols = [
        'Product Visitors (Visits)', 'Product Page Views', 'Likes',
        'Product Visitors (Added to Cart)', 'Total Buyers (Orders Created)',
        'Products Ordered', 'Total Sales (Orders Created) (IDR)',
        'Total Buyers (Orders Ready to Ship)', 'Sales (Orders Ready to Ship) (IDR)'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

@st.cache_data
def load_chat_data():
    """
    Load chat data with proper CSAT conversion
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "chat_data_cleaned.csv")
    
    # Fix CSAT - if values are < 2, they're decimals that need *100
    if 'CSAT_Percent' in df.columns:
        df['CSAT_Percent'] = pd.to_numeric(df['CSAT_Percent'], errors='coerce')
        # If average is very low (< 2), it's likely in decimal form (0.95 = 95%)
        if df['CSAT_Percent'].mean() < 2:
            df['CSAT_Percent'] = df['CSAT_Percent'] * 100
    
    return df

@st.cache_data
def load_flash_sale_data():
    """
    Load flash sale data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "flash_sale_cleaned.csv")
    return df

@st.cache_data
def load_voucher_data():
    """
    Load voucher data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "voucher_cleaned.csv")
    return df

@st.cache_data
def load_game_data():
    """
    Load game/prize data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "game_cleaned.csv")
    return df

@st.cache_data
def load_live_data():
    """
    Load live streaming data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "live_cleaned.csv")
    return df

@st.cache_data
def load_mass_chat_data():
    """
    Load mass chat broadcast data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "mass_chat_data_cleaned.csv")
    return df

@st.cache_data
def load_off_platform_data():
    """
    Load off-platform traffic data
    Returns: DataFrame with Date as datetime and numeric columns
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "off_platform_cleaned.csv")
    
    # Remove header rows
    df = df[df['Date'].notna() & (df['Date'] != 'Date') & (df['Date'] != 'Tanggal')]
    
    # Convert date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
    
    # Ensure numeric columns
    numeric_cols = ['Sales_IDR', 'Orders', 'Products', 'Visits', 'Visitors', 
                   'Total_Buyers', 'New_Buyers', 'Users_Added_To_Cart']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

@st.cache_data
def load_paylater_data():
    """
    Load Shopee PayLater data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "shopee_paylater_cleaned.csv")
    
    # Skip header rows
    df = df[df['Periode Data'].notna() & (df['Periode Data'] != 'Periode Data')]
    
    return df

@st.cache_data
def load_revenue_data():
    """
    Load revenue data
    Returns: DataFrame
    """
    data_path = get_data_path()
    df = pd.read_csv(data_path / "revenue_2_cleaned.csv")
    return df

@st.cache_data
def load_all_campaign_data():
    """
    Load all campaign data (flash sale, voucher, game, live)
    Returns: Dictionary with campaign type as key
    """
    return {
        'flash_sale': load_flash_sale_data(),
        'voucher': load_voucher_data(),
        'game': load_game_data(),
        'live': load_live_data()
    }

def get_numeric_value(df, column, default=0):
    """
    Safely get numeric value from DataFrame column
    
    Args:
        df: DataFrame
        column: Column name
        default: Default value if column doesn't exist or has no data
    
    Returns:
        float: Numeric value
    """
    if column not in df.columns:
        return default
    
    try:
        value = pd.to_numeric(df[column], errors='coerce').sum()
        return value if not pd.isna(value) else default
    except:
        return default

def get_numeric_mean(df, column, default=0):
    """
    Safely get numeric mean from DataFrame column
    
    Args:
        df: DataFrame
        column: Column name
        default: Default value if column doesn't exist or has no data
    
    Returns:
        float: Mean value
    """
    if column not in df.columns:
        return default
    
    try:
        value = pd.to_numeric(df[column], errors='coerce').mean()
        return value if not pd.isna(value) else default
    except:
        return default
