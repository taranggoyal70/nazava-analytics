"""
Reusable Date Filter Component
Provides 6-month comparison functionality across all dashboard pages
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def create_date_filter(df, date_column='Date', key_prefix=''):
    """
    Create a date range filter with preset options
    
    Args:
        df: DataFrame with date column
        date_column: Name of the date column
        key_prefix: Unique prefix for widget keys to avoid duplicates
    
    Returns:
        filtered_df: Filtered DataFrame
        comparison_df: Comparison period DataFrame (previous 6 months)
        date_range: Selected date range tuple
    """
    
    # Convert date column to datetime
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df = df.dropna(subset=[date_column])
    else:
        st.error(f"Column '{date_column}' not found in data")
        return df, pd.DataFrame(), (None, None)
    
    # Get min and max dates
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    
    # Create filter UI
    st.markdown("### 📅 Date Range Filter")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        filter_type = st.selectbox(
            "Select Period",
            ["Last 6 Months", "Last 3 Months", "Last Month", "Custom Range", "All Time"],
            key=f"filter_type_{key_prefix}_{date_column}"
        )
    
    # Calculate date ranges based on selection
    if filter_type == "Last 6 Months":
        end_date = max_date
        start_date = end_date - timedelta(days=180)
        comparison_start = start_date - timedelta(days=180)
        comparison_end = start_date - timedelta(days=1)
        
    elif filter_type == "Last 3 Months":
        end_date = max_date
        start_date = end_date - timedelta(days=90)
        comparison_start = start_date - timedelta(days=90)
        comparison_end = start_date - timedelta(days=1)
        
    elif filter_type == "Last Month":
        end_date = max_date
        start_date = end_date - timedelta(days=30)
        comparison_start = start_date - timedelta(days=30)
        comparison_end = start_date - timedelta(days=1)
        
    elif filter_type == "Custom Range":
        with col2:
            start_date = st.date_input(
                "Start Date",
                value=max_date - timedelta(days=180),
                min_value=min_date.date(),
                max_value=max_date.date(),
                key=f"start_date_{key_prefix}_{date_column}"
            )
            start_date = pd.to_datetime(start_date)
        
        with col3:
            end_date = st.date_input(
                "End Date",
                value=max_date.date(),
                min_value=min_date.date(),
                max_value=max_date.date(),
                key=f"end_date_{key_prefix}_{date_column}"
            )
            end_date = pd.to_datetime(end_date)
        
        # Calculate comparison period (same length, previous period)
        period_length = (end_date - start_date).days
        comparison_start = start_date - timedelta(days=period_length)
        comparison_end = start_date - timedelta(days=1)
    
    else:  # All Time
        start_date = min_date
        end_date = max_date
        comparison_start = min_date
        comparison_end = min_date  # No comparison for all time
    
    # Filter data
    filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
    comparison_df = df[(df[date_column] >= comparison_start) & (df[date_column] <= comparison_end)]
    
    # Display date range info
    st.markdown(f"""
    <div style="background: #e6f3ff; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>📊 Current Period:</strong> {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}
                <span style="color: #64748b; margin-left: 1rem;">({len(filtered_df)} records)</span>
            </div>
            <div>
                <strong>📈 Comparison Period:</strong> {comparison_start.strftime('%Y-%m-%d')} to {comparison_end.strftime('%Y-%m-%d')}
                <span style="color: #64748b; margin-left: 1rem;">({len(comparison_df)} records)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return filtered_df, comparison_df, (start_date, end_date)


def calculate_comparison_metrics(current_value, previous_value):
    """
    Calculate comparison metrics between two periods
    
    Args:
        current_value: Current period value
        previous_value: Previous period value
    
    Returns:
        dict with change_value, change_percent, and trend
    """
    if previous_value == 0 or pd.isna(previous_value):
        return {
            'change_value': current_value,
            'change_percent': 0,
            'trend': 'neutral'
        }
    
    change_value = current_value - previous_value
    change_percent = (change_value / previous_value) * 100
    
    trend = 'up' if change_value > 0 else 'down' if change_value < 0 else 'neutral'
    
    return {
        'change_value': change_value,
        'change_percent': change_percent,
        'trend': trend
    }


def display_comparison_metric(label, current_value, previous_value, format_type='number', icon='📊'):
    """
    Display a metric with comparison to previous period
    
    Args:
        label: Metric label
        current_value: Current period value
        previous_value: Previous period value
        format_type: 'number', 'currency', 'percent'
        icon: Emoji icon
    """
    comparison = calculate_comparison_metrics(current_value, previous_value)
    
    # Format values based on type
    if format_type == 'currency':
        current_display = f"IDR {current_value/1e6:.1f}M"
        delta_display = f"IDR {abs(comparison['change_value'])/1e6:.1f}M"
    elif format_type == 'percent':
        current_display = f"{current_value:.1f}%"
        delta_display = f"{abs(comparison['change_value']):.1f}pp"
    else:
        current_display = f"{int(current_value):,}"
        delta_display = f"{int(abs(comparison['change_value'])):,}"
    
    # Determine delta color
    delta_color = '#10b981' if comparison['trend'] == 'up' else '#ef4444' if comparison['trend'] == 'down' else '#64748b'
    delta_symbol = '▲' if comparison['trend'] == 'up' else '▼' if comparison['trend'] == 'down' else '='
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe;">
        <div style="color: #64748b; font-size: 0.9rem; margin-bottom: 0.5rem;">{icon} {label}</div>
        <div style="font-size: 2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem;">{current_display}</div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: {delta_color}; font-weight: 600; font-size: 0.9rem;">
                {delta_symbol} {delta_display} ({comparison['change_percent']:+.1f}%)
            </span>
            <span style="color: #94a3b8; font-size: 0.85rem;">vs previous period</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def create_comparison_chart(current_df, comparison_df, metric_column, date_column='Date', title='Metric Comparison'):
    """
    Create a comparison chart showing current vs previous period
    
    Args:
        current_df: Current period DataFrame
        comparison_df: Comparison period DataFrame
        metric_column: Column to plot
        date_column: Date column name
        title: Chart title
    
    Returns:
        Plotly figure
    """
    import plotly.graph_objects as go
    
    # Prepare data
    current_data = current_df.groupby(date_column)[metric_column].sum().reset_index()
    current_data.columns = ['Date', 'Value']
    current_data['Period'] = 'Current Period'
    
    comparison_data = comparison_df.groupby(date_column)[metric_column].sum().reset_index()
    comparison_data.columns = ['Date', 'Value']
    comparison_data['Period'] = 'Previous Period'
    
    # Create figure
    fig = go.Figure()
    
    # Add current period
    fig.add_trace(go.Scatter(
        x=current_data['Date'],
        y=current_data['Value'],
        name='Current Period',
        line=dict(color='#4facfe', width=3),
        fill='tozeroy',
        fillcolor='rgba(79, 172, 254, 0.1)'
    ))
    
    # Add comparison period
    fig.add_trace(go.Scatter(
        x=comparison_data['Date'],
        y=comparison_data['Value'],
        name='Previous Period',
        line=dict(color='#94a3b8', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=metric_column,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        hovermode='x unified'
    )
    
    return fig
