"""
Period Comparison Dashboard
Compare performance across different time periods
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.date_filter import (
    create_date_filter, 
    display_comparison_metric,
    create_comparison_chart
)

st.set_page_config(page_title="Period Comparison", page_icon="📊", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_15periodcomparison"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Header
st.markdown("# 📊 Period Comparison Analysis")
st.markdown("### Compare Performance Across Different Time Periods")
st.markdown("---")

# Load data
@st.cache_data
def load_all_data():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    
    traffic_df = pd.read_csv(f"{data_path}/traffic_overview_cleaned.csv")
    product_df = pd.read_csv(f"{data_path}/product_overview_cleaned.csv")
    chat_df = pd.read_csv(f"{data_path}/chat_data_cleaned.csv")
    flash_sale_df = pd.read_csv(f"{data_path}/flash_sale_cleaned.csv")
    
    return traffic_df, product_df, chat_df, flash_sale_df

traffic_df, product_df, chat_df, flash_sale_df = load_all_data()

# Date filter for traffic data
st.markdown("## 🚦 Traffic Analysis")
filtered_traffic, comparison_traffic, date_range = create_date_filter(traffic_df, 'Date', key_prefix='traffic')

st.markdown("---")

# Traffic metrics comparison
st.markdown("### 📊 Traffic Metrics Comparison")

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_visitors = pd.to_numeric(filtered_traffic['Total_Visitors'], errors='coerce').sum()
    previous_visitors = pd.to_numeric(comparison_traffic['Total_Visitors'], errors='coerce').sum()
    display_comparison_metric("Total Visitors", current_visitors, previous_visitors, 'number', '👥')

with col2:
    current_new = pd.to_numeric(filtered_traffic['New_Visitors'], errors='coerce').sum()
    previous_new = pd.to_numeric(comparison_traffic['New_Visitors'], errors='coerce').sum()
    display_comparison_metric("New Visitors", current_new, previous_new, 'number', '🆕')

with col3:
    current_returning = pd.to_numeric(filtered_traffic['Returning_Visitors'], errors='coerce').sum()
    previous_returning = pd.to_numeric(comparison_traffic['Returning_Visitors'], errors='coerce').sum()
    display_comparison_metric("Returning Visitors", current_returning, previous_returning, 'number', '🔄')

with col4:
    current_followers = pd.to_numeric(filtered_traffic['New_Followers'], errors='coerce').sum()
    previous_followers = pd.to_numeric(comparison_traffic['New_Followers'], errors='coerce').sum()
    display_comparison_metric("New Followers", current_followers, previous_followers, 'number', '⭐')

st.markdown("---")

# Traffic trend comparison chart
st.markdown("### 📈 Traffic Trend Comparison")

# Prepare traffic data for comparison
filtered_traffic['Total_Visitors_Numeric'] = pd.to_numeric(filtered_traffic['Total_Visitors'], errors='coerce')
comparison_traffic['Total_Visitors_Numeric'] = pd.to_numeric(comparison_traffic['Total_Visitors'], errors='coerce')

fig = create_comparison_chart(
    filtered_traffic, 
    comparison_traffic, 
    'Total_Visitors_Numeric',
    'Date',
    'Total Visitors: Current vs Previous Period'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Product performance comparison
st.markdown("## 📦 Product Performance")

# Filter product data
filtered_product, comparison_product, _ = create_date_filter(product_df, 'Date', key_prefix='product')

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_sales = pd.to_numeric(filtered_product['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
    previous_sales = pd.to_numeric(comparison_product['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
    display_comparison_metric("Total Sales", current_sales, previous_sales, 'currency', '💰')

with col2:
    current_orders = pd.to_numeric(filtered_product['Total Buyers (Orders Created)'], errors='coerce').sum()
    previous_orders = pd.to_numeric(comparison_product['Total Buyers (Orders Created)'], errors='coerce').sum()
    display_comparison_metric("Total Orders", current_orders, previous_orders, 'number', '🛒')

with col3:
    current_visits = pd.to_numeric(filtered_product['Product Visitors (Visits)'], errors='coerce').sum()
    previous_visits = pd.to_numeric(comparison_product['Product Visitors (Visits)'], errors='coerce').sum()
    display_comparison_metric("Product Visits", current_visits, previous_visits, 'number', '👁️')

with col4:
    current_conv = pd.to_numeric(filtered_product['Order Conversion Rate (Orders Created)'], errors='coerce').mean()
    previous_conv = pd.to_numeric(comparison_product['Order Conversion Rate (Orders Created)'], errors='coerce').mean()
    display_comparison_metric("Conversion Rate", current_conv, previous_conv, 'percent', '📈')

st.markdown("---")

# Sales trend comparison
st.markdown("### 💰 Sales Trend Comparison")

filtered_product['Sales_Numeric'] = pd.to_numeric(filtered_product['Total Sales (Orders Created) (IDR)'], errors='coerce')
comparison_product['Sales_Numeric'] = pd.to_numeric(comparison_product['Total Sales (Orders Created) (IDR)'], errors='coerce')

fig = create_comparison_chart(
    filtered_product,
    comparison_product,
    'Sales_Numeric',
    'Date',
    'Sales: Current vs Previous Period'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Summary insights
st.markdown("## 💡 Period Comparison Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10b981;">
        <h4 style="color: #0f172a; margin-top: 0;">📈 Growth Areas</h4>
        <ul style="color: #64748b;">
            <li>Compare visitor growth trends</li>
            <li>Identify high-performing periods</li>
            <li>Track conversion rate improvements</li>
            <li>Monitor sales momentum</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe;">
        <h4 style="color: #0f172a; margin-top: 0;">🎯 Actionable Insights</h4>
        <ul style="color: #64748b;">
            <li>Replicate successful strategies from high-growth periods</li>
            <li>Investigate causes of performance dips</li>
            <li>Optimize campaigns based on seasonal patterns</li>
            <li>Adjust inventory for demand fluctuations</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Export comparison data
st.markdown("## 📥 Export Comparison Data")

col1, col2 = st.columns(2)

with col1:
    # Export current period
    current_export = pd.DataFrame({
        'Metric': ['Total Visitors', 'Total Sales', 'Total Orders', 'Conversion Rate'],
        'Current Period': [current_visitors, current_sales, current_orders, current_conv],
        'Previous Period': [previous_visitors, previous_sales, previous_orders, previous_conv],
        'Change (%)': [
            ((current_visitors - previous_visitors) / previous_visitors * 100) if previous_visitors > 0 else 0,
            ((current_sales - previous_sales) / previous_sales * 100) if previous_sales > 0 else 0,
            ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0,
            ((current_conv - previous_conv) / previous_conv * 100) if previous_conv > 0 else 0
        ]
    })
    
    csv = current_export.to_csv(index=False)
    st.download_button(
        label="📊 Download Comparison Summary (CSV)",
        data=csv,
        file_name="period_comparison_summary.csv",
        mime="text/csv"
    )

with col2:
    st.info("""
    **💡 Tip**: Use this comparison data to:
    - Track month-over-month growth
    - Identify seasonal trends
    - Measure campaign effectiveness
    - Report to stakeholders
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>📊 Period Comparison Analysis | 📈 Track Growth Over Time</p>
    <p>💡 Compare any two periods to identify trends and opportunities</p>
</div>
""", unsafe_allow_html=True)
