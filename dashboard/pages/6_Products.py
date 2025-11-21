"""
Product Analytics Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_product_data

st.set_page_config(page_title="Products", page_icon="📦", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_6products"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load cleaned data
product_df = load_product_data()

# Header
st.markdown("# 📦 Product Analytics")
st.markdown("### Product Performance & Insights")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_visits = pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').sum()
total_views = pd.to_numeric(product_df['Product Page Views'], errors='coerce').sum()
total_sales = pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
total_orders = pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').sum()

with col1:
    st.metric(
        label="👁️ Product Visits",
        value=f"{int(total_visits/1000):.1f}K",
        help="Total product page visits"
    )

with col2:
    st.metric(
        label="📄 Page Views",
        value=f"{int(total_views/1000):.1f}K",
        help="Total product pages viewed"
    )

with col3:
    st.metric(
        label="💰 Total Sales",
        value=f"IDR {total_sales/1e6:.1f}M",
        help="Total product sales"
    )

with col4:
    conversion = (total_orders / total_visits * 100) if total_visits > 0 else 0
    st.metric(
        label="📈 Conversion Rate",
        value=f"{conversion:.2f}%",
        help="Visit to purchase conversion"
    )

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Product Funnel")
    
    # Create funnel data
    funnel_data = pd.DataFrame({
        'Stage': ['Visits', 'Added to Cart', 'Orders Created', 'Orders Shipped'],
        'Count': [
            total_visits,
            pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce').sum(),
            pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').sum(),
            pd.to_numeric(product_df['Total Buyers (Orders Ready to Ship)'], errors='coerce').sum()
        ]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        marker=dict(color=['#667eea', '#7c6fdc', '#9260ce', '#a851c0'])
    ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🛒 Cart & Purchase Behavior")
    
    behavior_data = pd.DataFrame({
        'Metric': ['Added to Cart', 'Orders Created', 'Orders Shipped'],
        'Count': [
            pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce').sum(),
            pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').sum(),
            pd.to_numeric(product_df['Total Buyers (Orders Ready to Ship)'], errors='coerce').sum()
        ]
    })
    
    fig = px.bar(
        behavior_data,
        x='Metric',
        y='Count',
        title='Shopping Behavior Metrics',
        color='Metric',
        color_discrete_sequence=['#667eea', '#764ba2', '#9260ce']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Daily Product Views")
    
    daily_views = product_df.groupby('Date')['Product Page Views'].apply(lambda x: pd.to_numeric(x, errors='coerce').sum()).reset_index()
    daily_views.columns = ['Date', 'Product_Pages_Viewed']
    daily_views = daily_views.sort_values('Date')
    
    fig = px.area(
        daily_views,
        x='Date',
        y='Product_Pages_Viewed',
        title='Product Page Views Over Time'
    )
    fig.update_traces(line_color='#667eea', fillcolor='rgba(102, 126, 234, 0.3)')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💰 Daily Sales")
    
    daily_sales = product_df.groupby('Date')['Total Sales (Orders Created) (IDR)'].apply(lambda x: pd.to_numeric(x, errors='coerce').sum()).reset_index()
    daily_sales.columns = ['Date', 'Total_Sales']
    daily_sales = daily_sales.sort_values('Date')
    
    fig = px.bar(
        daily_sales,
        x='Date',
        y='Total_Sales',
        title='Daily Product Sales'
    )
    fig.update_traces(marker_color='#764ba2')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Conversion Metrics
st.markdown("### 📊 Conversion Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    cart_conversion = pd.to_numeric(product_df['Product Add-to-Cart Conversion Rate'], errors='coerce').mean()
    st.metric(
        label="Visit to Cart",
        value=f"{cart_conversion:.2f}%",
        help="% of visitors who add to cart"
    )

with col2:
    order_conversion = pd.to_numeric(product_df['Order Conversion Rate (Orders Created)'], errors='coerce').mean()
    st.metric(
        label="Visit to Order",
        value=f"{order_conversion:.2f}%",
        help="% of visitors who place order"
    )

with col3:
    ship_conversion = pd.to_numeric(product_df['Order Conversion Rate (Orders Ready to Ship)'], errors='coerce').mean()
    st.metric(
        label="Visit to Ship",
        value=f"{ship_conversion:.2f}%",
        help="% of visitors whose orders ship"
    )

st.markdown("---")

# Engagement Metrics
st.markdown("### 💡 Engagement Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_likes = pd.to_numeric(product_df['Likes'], errors='coerce').sum()
    st.metric(
        label="❤️ Total Likes",
        value=f"{int(total_likes):,}"
    )

with col2:
    search_clicks = pd.to_numeric(product_df['Search Clicks'], errors='coerce').sum()
    st.metric(
        label="🔍 Search Clicks",
        value=f"{int(search_clicks):,}"
    )

with col3:
    products_visited = pd.to_numeric(product_df['Products Visited'], errors='coerce').sum()
    st.metric(
        label="📦 Products Visited",
        value=f"{int(products_visited):,}"
    )

with col4:
    browse_without_buy = pd.to_numeric(product_df['Visitors Viewed Without Purchase'], errors='coerce').sum()
    browse_rate = (browse_without_buy / total_visits * 100) if total_visits > 0 else 0
    st.metric(
        label="👀 Browse Rate",
        value=f"{browse_rate:.1f}%"
    )

st.markdown("---")

# Detailed Metrics
st.markdown("### 📋 Detailed Product Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Traffic Metrics")
    st.write(f"**Total Visits:** {int(total_visits):,}")
    st.write(f"**Page Views:** {int(total_views):,}")
    st.write(f"**Products Visited:** {int(products_visited):,}")
    st.write(f"**Avg Views per Visit:** {(total_views/total_visits):.1f}")

with col2:
    st.markdown("#### Cart Metrics")
    added_to_cart = pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce').sum()
    cart_products = pd.to_numeric(product_df['Added to Cart (Products)'], errors='coerce').sum()
    st.write(f"**Added to Cart:** {int(added_to_cart):,}")
    st.write(f"**Products in Cart:** {int(cart_products):,}")
    st.write(f"**Cart Conversion:** {cart_conversion:.2f}%")

with col3:
    st.markdown("#### Sales Metrics")
    st.write(f"**Total Orders:** {int(total_orders):,}")
    st.write(f"**Total Sales:** IDR {total_sales/1e6:.1f}M")
    st.write(f"**Avg Order Value:** IDR {(total_sales/total_orders)/1000:.0f}K" if total_orders > 0 else "N/A")
    st.write(f"**Order Conversion:** {order_conversion:.2f}%")

st.markdown("---")

# Insights
st.markdown("### 💡 Product Insights")

col1, col2 = st.columns(2)

with col1:
    if cart_conversion >= 5:
        st.success(f"✅ **Strong Cart Conversion:** {cart_conversion:.2f}%")
    else:
        st.warning(f"⚠️ **Cart Conversion:** {cart_conversion:.2f}% - Optimize product pages")
    
    if browse_rate <= 50:
        st.success(f"✅ **Good Engagement:** {browse_rate:.1f}% browse without buying")
    else:
        st.info(f"📊 **Browse Rate:** {browse_rate:.1f}%")

with col2:
    products_ordered = pd.to_numeric(product_df['Products Ordered'], errors='coerce').sum()
    st.info(f"📦 **Total Products Sold:** {int(products_ordered):,}")
    st.info(f"💰 **Revenue per Visit:** IDR {(total_sales/total_visits):.0f}" if total_visits > 0 else "N/A")
