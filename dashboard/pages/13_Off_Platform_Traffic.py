"""
Off-Platform Traffic Analytics
Track traffic and sales from external sources
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Off-Platform Traffic", page_icon="🌐", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_13offplatformtraffic"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load data
@st.cache_data
def load_off_platform_data():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    df = pd.read_csv(f"{data_path}/off_platform_cleaned.csv")
    return df

off_platform_df = load_off_platform_data()

# Header
st.markdown("# 🌐 Off-Platform Traffic Analytics")
st.markdown("### External Traffic Sources & Performance")
st.markdown("---")

# Calculate KPIs
total_visits = pd.to_numeric(off_platform_df['Visits'], errors='coerce').sum()
total_visitors = pd.to_numeric(off_platform_df['Visitors'], errors='coerce').sum()
total_sales = pd.to_numeric(off_platform_df['Sales_IDR'], errors='coerce').sum()
total_orders = pd.to_numeric(off_platform_df['Orders'], errors='coerce').sum()
total_cart_adds = pd.to_numeric(off_platform_df['Users_Added_To_Cart'], errors='coerce').sum()
avg_conversion = pd.to_numeric(off_platform_df['Conversion_Rate_Orders_Per_Visit'], errors='coerce').mean()

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="👥 Total Visitors",
        value=f"{int(total_visitors):,}",
        help="Unique visitors from external sources"
    )

with col2:
    st.metric(
        label="🔗 Total Visits",
        value=f"{int(total_visits):,}",
        help="Total visits from off-platform"
    )

with col3:
    st.metric(
        label="💰 Total Sales",
        value=f"IDR {total_sales/1e6:.1f}M",
        help="Revenue from external traffic"
    )

with col4:
    st.metric(
        label="🛒 Total Orders",
        value=f"{int(total_orders):,}",
        help="Orders from external sources"
    )

with col5:
    st.metric(
        label="📈 Conversion Rate",
        value=f"{avg_conversion:.2f}%",
        help="Visit to order conversion"
    )

st.markdown("---")

# Traffic by channel
st.markdown("## 📊 Traffic by Channel")

col1, col2 = st.columns(2)

with col1:
    # Sales by channel
    channel_sales = off_platform_df.groupby('Channel').agg({
        'Sales_IDR': lambda x: pd.to_numeric(x, errors='coerce').sum()
    }).reset_index()
    
    fig = px.pie(
        channel_sales,
        values='Sales_IDR',
        names='Channel',
        title='Sales Distribution by Channel',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Visitors by channel
    channel_visitors = off_platform_df.groupby('Channel').agg({
        'Visitors': lambda x: pd.to_numeric(x, errors='coerce').sum()
    }).reset_index()
    
    fig = px.bar(
        channel_visitors,
        x='Channel',
        y='Visitors',
        title='Visitors by Channel',
        color='Visitors',
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Platform performance
st.markdown("## 🖥️ Platform Performance")

platform_stats = off_platform_df.groupby('Platform').agg({
    'Visits': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Visitors': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Sales_IDR': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Orders': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Conversion_Rate_Orders_Per_Visit': lambda x: pd.to_numeric(x, errors='coerce').mean()
}).reset_index()

platform_stats.columns = ['Platform', 'Visits', 'Visitors', 'Sales (IDR)', 'Orders', 'Avg Conversion (%)']
platform_stats['Sales (IDR)'] = platform_stats['Sales (IDR)'].apply(lambda x: f"IDR {x/1e6:.2f}M")

st.dataframe(platform_stats, use_container_width=True, hide_index=True)

st.markdown("---")

# Conversion funnel
st.markdown("## 🎯 Off-Platform Conversion Funnel")

col1, col2 = st.columns([2, 1])

with col1:
    funnel_data = pd.DataFrame({
        'Stage': ['Visits', 'Added to Cart', 'Orders'],
        'Count': [total_visits, total_cart_adds, total_orders]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        marker=dict(color=['#667eea', '#764ba2', '#4facfe'])
    ))
    
    fig.update_layout(
        title='External Traffic Conversion',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Conversion Metrics")
    
    visit_to_cart = (total_cart_adds / total_visits * 100) if total_visits > 0 else 0
    cart_to_order = (total_orders / total_cart_adds * 100) if total_cart_adds > 0 else 0
    
    st.metric("Visit → Cart", f"{visit_to_cart:.1f}%")
    st.metric("Cart → Order", f"{cart_to_order:.1f}%")
    st.metric("Overall", f"{avg_conversion:.2f}%")
    
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    st.metric("Avg Order Value", f"IDR {avg_order_value/1000:.0f}K")

st.markdown("---")

# Channel insights
st.markdown("## 💡 Channel Insights")

col1, col2, col3 = st.columns(3)

with col1:
    best_channel = channel_sales.loc[channel_sales['Sales_IDR'].idxmax(), 'Channel'] if not channel_sales.empty else 'N/A'
    best_sales = channel_sales['Sales_IDR'].max() if not channel_sales.empty else 0
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; height: 200px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🏆</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Top Channel</div>
        <div style="font-size: 1.5rem; font-weight: 800;">{best_channel}</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">IDR {best_sales/1e6:.1f}M in sales</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_new_buyers = pd.to_numeric(off_platform_df['New_Buyers'], errors='coerce').sum()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; color: white; height: 200px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">👤</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">New Customers</div>
        <div style="font-size: 1.5rem; font-weight: 800;">{int(total_new_buyers):,}</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">Acquired from external sources</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    cart_value = pd.to_numeric(off_platform_df['Value_Products_Added_To_Cart_IDR'], errors='coerce').sum()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; color: white; height: 200px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🛒</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Cart Value</div>
        <div style="font-size: 1.5rem; font-weight: 800;">IDR {cart_value/1e6:.1f}M</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">Total cart value added</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Recommendations
st.markdown("## 🎯 Optimization Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe;">
        <h4 style="color: #0f172a; margin-top: 0;">🚀 Scale Top Channels</h4>
        <ul style="color: #64748b;">
            <li>Increase ad spend on best-performing channels</li>
            <li>Replicate successful campaigns</li>
            <li>A/B test different creatives</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10b981;">
        <h4 style="color: #0f172a; margin-top: 0;">📊 Improve Conversion</h4>
        <ul style="color: #64748b;">
            <li>Optimize landing pages for external traffic</li>
            <li>Add retargeting pixels</li>
            <li>Create channel-specific promotions</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Export
st.markdown("---")
csv = off_platform_df.to_csv(index=False)
st.download_button(
    label="📥 Download Full Data (CSV)",
    data=csv,
    file_name="off_platform_traffic.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>🌐 Off-Platform Traffic Analytics | 📊 External Source Tracking</p>
</div>
""", unsafe_allow_html=True)
