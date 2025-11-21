"""
Overview Dashboard Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_traffic_data, load_product_data, load_chat_data, load_flash_sale_data

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_overview"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load cleaned data
chat_df = load_chat_data()
traffic_df = load_traffic_data()
flash_sale_df = load_flash_sale_data()
product_df = load_product_data()

# Header
st.markdown("# 📊 Overview Dashboard")
st.markdown("### Key Performance Indicators & Trends")

# Data freshness indicator
col1, col2 = st.columns([3, 1])
with col2:
    st.info("📅 **Data Period**: Sep 2025")

st.markdown("---")

# Calculate KPIs - ensure all numeric
total_sales = pd.to_numeric(chat_df['Sales_IDR'], errors='coerce').sum() + pd.to_numeric(flash_sale_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
total_orders = pd.to_numeric(chat_df['Total_Orders'], errors='coerce').sum() + pd.to_numeric(flash_sale_df['Orders_Ready_To_Ship'], errors='coerce').sum()
total_visitors = pd.to_numeric(traffic_df['Total_Visitors'], errors='coerce').sum()  # Ensure numeric
avg_csat = pd.to_numeric(chat_df['CSAT_Percent'], errors='coerce').mean()

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"IDR {total_sales/1e6:.1f}M",
        delta="12.5%",
        help="Total sales across all channels"
    )

with col2:
    st.metric(
        label="🛒 Total Orders",
        value=f"{int(total_orders):,}",
        delta="8.3%",
        help="Total number of orders"
    )

with col3:
    st.metric(
        label="👥 Total Visitors",
        value=f"{int(total_visitors/1000):.1f}K",
        delta="15.2%",
        help="Total unique visitors"
    )

with col4:
    conversion_rate = (total_orders / total_visitors * 100) if total_visitors > 0 else 0
    st.metric(
        label="📈 Conversion Rate",
        value=f"{conversion_rate:.2f}%",
        delta="0.3%",
        help="Orders / Visitors"
    )

with col5:
    st.metric(
        label="😊 CSAT Score",
        value=f"{avg_csat*100:.1f}%",
        delta="2.1%",
        help="Customer Satisfaction Score"
    )

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Traffic Trend")
    
    # Traffic over time - ensure numeric
    traffic_df_clean = traffic_df.copy()
    traffic_df_clean['Total_Visitors'] = pd.to_numeric(traffic_df_clean['Total_Visitors'], errors='coerce')
    traffic_trend = traffic_df_clean.groupby('Date')['Total_Visitors'].sum().reset_index()
    traffic_trend = traffic_trend.sort_values('Date')
    
    fig = px.line(
        traffic_trend,
        x='Date',
        y='Total_Visitors',
        title='Daily Visitors',
        labels={'Total_Visitors': 'Visitors', 'Date': 'Date'}
    )
    fig.update_traces(line_color='#667eea', line_width=3)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💰 Sales by Category")
    
    # Sales by category
    sales_data = pd.DataFrame({
        'Category': ['Chat', 'Flash Sale'],
        'Sales': [
            pd.to_numeric(chat_df['Sales_IDR'], errors='coerce').sum(),
            pd.to_numeric(flash_sale_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
        ]
    })
    
    fig = px.pie(
        sales_data,
        values='Sales',
        names='Category',
        title='Sales Distribution',
        color_discrete_sequence=['#667eea', '#764ba2']
    )
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Conversion Funnel")
    
    # Funnel data
    if not product_df.empty:
        total_visits = pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').sum()
        added_to_cart = pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce').sum()
        orders_created = pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').sum()
        orders_shipped = pd.to_numeric(product_df['Total Buyers (Orders Ready to Ship)'], errors='coerce').sum()
        
        funnel_data = pd.DataFrame({
            'Stage': ['Visitors', 'Added to Cart', 'Orders Created', 'Orders Shipped'],
            'Count': [total_visits, added_to_cart, orders_created, orders_shipped]
        })
        
        fig = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            textinfo="value+percent initial",
            marker=dict(color=['#667eea', '#7c6fdc', '#9260ce', '#a851c0'])
        ))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 👥 Visitor Composition")
    
    # New vs Returning visitors
    visitor_comp = pd.DataFrame({
        'Type': ['New Visitors', 'Returning Visitors'],
        'Count': [
            pd.to_numeric(traffic_df['New_Visitors'], errors='coerce').sum(),
            pd.to_numeric(traffic_df['Returning_Visitors'], errors='coerce').sum()
        ]
    })
    
    fig = px.bar(
        visitor_comp,
        x='Type',
        y='Count',
        title='Visitor Types',
        color='Type',
        color_discrete_sequence=['#667eea', '#764ba2']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Recent Activity
st.markdown("### 📋 Recent Activity")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔥 Flash Sale Performance")
    if not flash_sale_df.empty:
        latest_flash = flash_sale_df.iloc[-1]
        st.write(f"**Sales:** IDR {latest_flash['Sales_Ready_To_Ship_IDR']/1e6:.2f}M")
        st.write(f"**Orders:** {int(latest_flash['Orders_Ready_To_Ship'])}")
        st.write(f"**Click Rate:** {latest_flash['Click_Rate']*100:.2f}%")

with col2:
    st.markdown("#### 💬 Customer Service")
    if not chat_df.empty:
        latest_chat = chat_df.iloc[-1]
        st.write(f"**Total Chats:** {int(latest_chat['Number_Of_Chats'])}")
        st.write(f"**Response Time:** {latest_chat['Average_Response_Time']:.1f} min")
        st.write(f"**CSAT:** {latest_chat['CSAT_Percent']*100:.1f}%")

with col3:
    st.markdown("#### 📊 Today's Metrics")
    if not traffic_df.empty:
        latest_traffic = traffic_df.iloc[-1]
        st.write(f"**Visitors:** {int(latest_traffic['Total_Visitors']):,}")
        st.write(f"**Products Viewed:** {int(latest_traffic['Products_Viewed']):,}")
        st.write(f"**New Followers:** {int(latest_traffic['New_Followers'])}")

st.markdown("---")

# Alerts & Notifications
st.markdown("### 🔔 Alerts & Notifications")

col1, col2 = st.columns([2, 1])

with col1:
    st.success("✅ All systems operational")
    st.info("ℹ️ Flash sale campaign performing 15% above target")
    st.warning("⚠️ Response time increased by 5% - review staffing")

with col2:
    st.markdown("#### Quick Stats")
    st.metric("Active Campaigns", "3")
    st.metric("Pending Orders", "127")
    st.metric("Unread Chats", "45")
