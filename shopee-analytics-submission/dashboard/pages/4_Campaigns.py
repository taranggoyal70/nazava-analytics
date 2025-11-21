"""
Campaign Performance Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Campaigns", page_icon="🎯", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_4campaigns"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load data
@st.cache_data
def load_campaign_data():
    """Load campaign data"""
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    
    flash_sale_df = pd.read_csv(f"{data_path}/flash_sale_cleaned.csv")
    voucher_df = pd.read_csv(f"{data_path}/voucher_cleaned.csv")
    game_df = pd.read_csv(f"{data_path}/game_cleaned.csv")
    live_df = pd.read_csv(f"{data_path}/live_cleaned.csv")
    
    return flash_sale_df, voucher_df, game_df, live_df

flash_sale_df, voucher_df, game_df, live_df = load_campaign_data()

# Header
st.markdown("# 🎯 Campaign Performance")
st.markdown("### Marketing & Promotional Analytics")
st.markdown("---")

# Campaign selector
campaign_type = st.selectbox(
    "Select Campaign Type",
    ["All Campaigns", "Flash Sales", "Vouchers", "Games/Prizes", "Live Streaming"]
)

st.markdown("---")

# Overview KPIs
col1, col2, col3, col4 = st.columns(4)

total_flash_sales = pd.to_numeric(flash_sale_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
total_voucher_sales = pd.to_numeric(voucher_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum() if not voucher_df.empty else 0
total_game_sales = pd.to_numeric(game_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum() if not game_df.empty else 0
total_live_sales = pd.to_numeric(live_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum() if not live_df.empty else 0

with col1:
    st.metric(
        label="🔥 Flash Sale Revenue",
        value=f"IDR {total_flash_sales/1e6:.1f}M"
    )

with col2:
    st.metric(
        label="🎟️ Voucher Revenue",
        value=f"IDR {total_voucher_sales/1e6:.1f}M"
    )

with col3:
    st.metric(
        label="🎮 Game Revenue",
        value=f"IDR {total_game_sales/1e6:.1f}M"
    )

with col4:
    st.metric(
        label="📺 Live Stream Revenue",
        value=f"IDR {total_live_sales/1e6:.1f}M"
    )

st.markdown("---")

# Campaign comparison
st.markdown("### 📊 Campaign Comparison")

col1, col2 = st.columns(2)

with col1:
    # Revenue by campaign type
    campaign_revenue = pd.DataFrame({
        'Campaign': ['Flash Sale', 'Voucher', 'Game', 'Live Stream'],
        'Revenue': [total_flash_sales, total_voucher_sales, total_game_sales, total_live_sales]
    })
    
    fig = px.bar(
        campaign_revenue,
        x='Campaign',
        y='Revenue',
        title='Revenue by Campaign Type',
        color='Campaign',
        color_discrete_sequence=['#667eea', '#764ba2', '#9260ce', '#a851c0']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Revenue distribution pie
    fig = px.pie(
        campaign_revenue,
        values='Revenue',
        names='Campaign',
        title='Revenue Share by Campaign',
        color_discrete_sequence=['#667eea', '#764ba2', '#9260ce', '#a851c0']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Flash Sale Details
if campaign_type in ["All Campaigns", "Flash Sales"]:
    st.markdown("### 🔥 Flash Sale Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_click_rate = pd.to_numeric(flash_sale_df['Click_Rate'], errors='coerce').mean() * 100
        st.metric(
            label="Avg Click Rate",
            value=f"{avg_click_rate:.2f}%"
        )
    
    with col2:
        total_flash_orders = pd.to_numeric(flash_sale_df['Orders_Ready_To_Ship'], errors='coerce').sum()
        st.metric(
            label="Total Orders",
            value=f"{int(total_flash_orders):,}"
        )
    
    with col3:
        avg_order_value = pd.to_numeric(flash_sale_df['Sales_Per_Buyer_Ready_To_Ship_IDR'], errors='coerce').mean()
        st.metric(
            label="Avg Order Value",
            value=f"IDR {avg_order_value/1000:.0f}K"
        )
    
    # Flash sale trend
    flash_trend = flash_sale_df.copy()
    flash_trend['Period'] = range(1, len(flash_trend) + 1)
    flash_trend['Sales_Ready_To_Ship_IDR'] = pd.to_numeric(flash_trend['Sales_Ready_To_Ship_IDR'], errors='coerce')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=flash_trend['Period'],
        y=flash_trend['Sales_Ready_To_Ship_IDR'],
        name='Sales',
        fill='tozeroy',
        line=dict(color='#667eea', width=2)
    ))
    fig.update_layout(
        title='Flash Sale Revenue Trend',
        xaxis_title='Campaign Period',
        yaxis_title='Revenue (IDR)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

# Voucher Details
if campaign_type in ["All Campaigns", "Vouchers"] and not voucher_df.empty:
    st.markdown("---")
    st.markdown("### 🎟️ Voucher Campaign Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_claims = pd.to_numeric(voucher_df['Claims'], errors='coerce').sum()
        st.metric(
            label="Total Claims",
            value=f"{int(total_claims):,}"
        )
    
    with col2:
        usage_rate = pd.to_numeric(voucher_df['Usage_Rate_Ready_To_Ship'], errors='coerce').mean() * 100
        st.metric(
            label="Avg Usage Rate",
            value=f"{usage_rate:.1f}%"
        )
    
    with col3:
        voucher_cost = pd.to_numeric(voucher_df['Total_Cost_Ready_To_Ship_IDR'], errors='coerce').sum()
        st.metric(
            label="Total Cost",
            value=f"IDR {voucher_cost/1e6:.1f}M"
        )
    
    with col4:
        voucher_roi = ((total_voucher_sales - voucher_cost) / voucher_cost * 100) if voucher_cost > 0 else 0
        st.metric(
            label="ROI",
            value=f"{voucher_roi:.1f}%"
        )

# Game/Prize Details
if campaign_type in ["All Campaigns", "Games/Prizes"] and not game_df.empty:
    st.markdown("---")
    st.markdown("### 🎮 Game/Prize Campaign Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_played = pd.to_numeric(game_df['Total_Played'], errors='coerce').sum()
        st.metric(
            label="Total Games Played",
            value=f"{int(total_played):,}"
        )
    
    with col2:
        total_players = pd.to_numeric(game_df['Players'], errors='coerce').sum()
        st.metric(
            label="Total Players",
            value=f"{int(total_players):,}"
        )
    
    with col3:
        prizes_claimed = pd.to_numeric(game_df['Prizes_Claimed'], errors='coerce').sum()
        st.metric(
            label="Prizes Claimed",
            value=f"{int(prizes_claimed):,}"
        )
    
    with col4:
        participation_rate = pd.to_numeric(game_df['Participation_Rate'], errors='coerce').mean() * 100
        st.metric(
            label="Participation Rate",
            value=f"{participation_rate:.1f}%"
        )

# Live Streaming Details
if campaign_type in ["All Campaigns", "Live Streaming"] and not live_df.empty:
    st.markdown("---")
    st.markdown("### 📺 Live Streaming Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_visitors_live = pd.to_numeric(live_df['Visitors'], errors='coerce').sum()
        st.metric(
            label="Total Viewers",
            value=f"{int(total_visitors_live):,}"
        )
    
    with col2:
        peak_viewers = pd.to_numeric(live_df['Peak_Viewers'], errors='coerce').max()
        st.metric(
            label="Peak Viewers",
            value=f"{int(peak_viewers):,}"
        )
    
    with col3:
        avg_watch_time = pd.to_numeric(live_df['Average_Watch_Duration'], errors='coerce').mean()
        st.metric(
            label="Avg Watch Time",
            value=f"{avg_watch_time:.1f} min"
        )
    
    with col4:
        total_live_orders = pd.to_numeric(live_df['Orders_COD_Created_Plus_NonCOD_Paid'], errors='coerce').sum()
        st.metric(
            label="Total Orders",
            value=f"{int(total_live_orders):,}"
        )

st.markdown("---")

# Campaign insights
st.markdown("### 💡 Campaign Insights")

col1, col2 = st.columns(2)

with col1:
    st.success("✅ **Top Performing Campaign:** Flash Sales")
    st.info(f"📊 **Total Campaign Revenue:** IDR {(total_flash_sales + total_voucher_sales + total_game_sales + total_live_sales)/1e6:.1f}M")

with col2:
    best_campaign = campaign_revenue.loc[campaign_revenue['Revenue'].idxmax(), 'Campaign']
    st.success(f"🏆 **Best ROI Campaign:** {best_campaign}")
    st.info(f"📈 **Flash Sale Click Rate:** {avg_click_rate:.2f}%")
