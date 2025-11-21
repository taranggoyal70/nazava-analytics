"""
Sales Analysis Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Analysis", page_icon="💰", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_3sales"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load data
@st.cache_data
def load_sales_data():
    """Load sales data"""
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    
    chat_df = pd.read_csv(f"{data_path}/chat_data_cleaned.csv")
    flash_sale_df = pd.read_csv(f"{data_path}/flash_sale_cleaned.csv")
    voucher_df = pd.read_csv(f"{data_path}/voucher_cleaned.csv")
    
    return chat_df, flash_sale_df, voucher_df

chat_df, flash_sale_df, voucher_df = load_sales_data()

# Header
st.markdown("# 💰 Sales Analysis")
st.markdown("### Revenue Metrics & Performance")
st.markdown("---")

# Calculate totals
total_sales_chat = chat_df['Sales_IDR'].sum()
total_sales_flash = flash_sale_df['Sales_Ready_To_Ship_IDR'].sum()
total_sales = total_sales_chat + total_sales_flash

total_orders_chat = chat_df['Total_Orders'].sum()
total_orders_flash = flash_sale_df['Orders_Ready_To_Ship'].sum()
total_orders = total_orders_chat + total_orders_flash

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"IDR {total_sales/1e6:.1f}M",
        help="Total sales across all channels"
    )

with col2:
    st.metric(
        label="🛒 Total Orders",
        value=f"{int(total_orders):,}",
        help="Total number of orders"
    )

with col3:
    aov = total_sales / total_orders if total_orders > 0 else 0
    st.metric(
        label="📊 Average Order Value",
        value=f"IDR {aov/1000:.0f}K",
        help="Average revenue per order"
    )

with col4:
    st.metric(
        label="📈 Revenue per Buyer",
        value=f"IDR {flash_sale_df['Sales_Per_Buyer_Ready_To_Ship_IDR'].mean()/1000:.0f}K",
        help="Average revenue per customer"
    )

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Revenue by Channel")
    
    revenue_data = pd.DataFrame({
        'Channel': ['Chat Sales', 'Flash Sales'],
        'Revenue': [total_sales_chat, total_sales_flash]
    })
    
    fig = px.pie(
        revenue_data,
        values='Revenue',
        names='Channel',
        title='Revenue Distribution',
        color_discrete_sequence=['#667eea', '#764ba2']
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🛒 Orders by Channel")
    
    orders_data = pd.DataFrame({
        'Channel': ['Chat Orders', 'Flash Sale Orders'],
        'Orders': [total_orders_chat, total_orders_flash]
    })
    
    fig = px.bar(
        orders_data,
        x='Channel',
        y='Orders',
        title='Order Volume by Channel',
        color='Channel',
        color_discrete_sequence=['#667eea', '#764ba2']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Flash Sale Performance
st.markdown("### 🔥 Flash Sale Performance")

col1, col2 = st.columns(2)

with col1:
    # Flash sale metrics over time
    flash_metrics = flash_sale_df[['Sales_Ready_To_Ship_IDR', 'Orders_Ready_To_Ship']].copy()
    flash_metrics['Period'] = range(1, len(flash_metrics) + 1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=flash_metrics['Period'],
        y=flash_metrics['Sales_Ready_To_Ship_IDR'],
        name='Sales',
        line=dict(color='#667eea', width=3)
    ))
    fig.update_layout(
        title='Flash Sale Revenue Trend',
        xaxis_title='Period',
        yaxis_title='Sales (IDR)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Click rate and conversion
    flash_metrics_conv = flash_sale_df[['Click_Rate', 'Orders_Ready_To_Ship']].copy()
    flash_metrics_conv['Period'] = range(1, len(flash_metrics_conv) + 1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=flash_metrics_conv['Period'],
        y=flash_metrics_conv['Click_Rate'] * 100,
        name='Click Rate %',
        marker_color='#764ba2'
    ))
    fig.update_layout(
        title='Flash Sale Click Rate',
        xaxis_title='Period',
        yaxis_title='Click Rate (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Voucher Performance
if not voucher_df.empty:
    st.markdown("### 🎟️ Voucher Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_voucher_sales = voucher_df['Sales_Ready_To_Ship_IDR'].sum()
        st.metric(
            label="Voucher Sales",
            value=f"IDR {total_voucher_sales/1e6:.1f}M"
        )
    
    with col2:
        total_voucher_cost = voucher_df['Total_Cost_Ready_To_Ship_IDR'].sum()
        st.metric(
            label="Voucher Cost",
            value=f"IDR {total_voucher_cost/1e6:.1f}M"
        )
    
    with col3:
        voucher_roi = ((total_voucher_sales - total_voucher_cost) / total_voucher_cost * 100) if total_voucher_cost > 0 else 0
        st.metric(
            label="Voucher ROI",
            value=f"{voucher_roi:.1f}%"
        )

st.markdown("---")

# Summary Statistics
st.markdown("### 📊 Detailed Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Chat Sales")
    st.write(f"**Total Revenue:** IDR {total_sales_chat/1e6:.2f}M")
    st.write(f"**Total Orders:** {int(total_orders_chat):,}")
    st.write(f"**Avg Order Value:** IDR {(total_sales_chat/total_orders_chat)/1000:.0f}K")
    st.write(f"**Conversion Rate:** {chat_df['Conversion_Rate_Chats_Replied'].mean()*100:.2f}%")

with col2:
    st.markdown("#### Flash Sales")
    st.write(f"**Total Revenue:** IDR {total_sales_flash/1e6:.2f}M")
    st.write(f"**Total Orders:** {int(total_orders_flash):,}")
    st.write(f"**Avg Order Value:** IDR {(total_sales_flash/total_orders_flash)/1000:.0f}K")
    st.write(f"**Avg Click Rate:** {flash_sale_df['Click_Rate'].mean()*100:.2f}%")

with col3:
    st.markdown("#### Overall Performance")
    st.write(f"**Total Revenue:** IDR {total_sales/1e6:.2f}M")
    st.write(f"**Total Orders:** {int(total_orders):,}")
    st.write(f"**Avg Order Value:** IDR {aov/1000:.0f}K")
    st.write(f"**Revenue per Buyer:** IDR {flash_sale_df['Sales_Per_Buyer_Ready_To_Ship_IDR'].mean()/1000:.0f}K")
