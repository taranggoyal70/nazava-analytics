"""
Shopee PayLater Analytics
Track PayLater payment performance and ROI
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Shopee PayLater", page_icon="💳", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_14shopeepaylater"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load data
@st.cache_data
def load_paylater_data():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    df = pd.read_csv(f"{data_path}/shopee_paylater_cleaned.csv")
    # Skip header rows
    df = df[df['Periode Data'].notna() & (df['Periode Data'] != 'Periode Data')]
    return df

paylater_df = load_paylater_data()

# Header
st.markdown("# 💳 Shopee PayLater Analytics")
st.markdown("### Buy Now, Pay Later Performance & ROI")
st.info("ℹ️ **Note**: PayLater data is limited. This feature is still being adopted by customers.")
st.markdown("---")

# Calculate KPIs
total_sales_created = pd.to_numeric(paylater_df['Sales_Orders_Created_IDR'], errors='coerce').sum()
total_sales_shipped = pd.to_numeric(paylater_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
total_orders_created = pd.to_numeric(paylater_df['Orders_Created'], errors='coerce').sum()
total_orders_shipped = pd.to_numeric(paylater_df['Orders_Ready_To_Ship'], errors='coerce').sum()
total_service_fee_created = pd.to_numeric(paylater_df['Biaya Layanan yang Dikenakan (Pesanan Dibuat)'], errors='coerce').sum()
total_service_fee_shipped = pd.to_numeric(paylater_df['Biaya Layanan yang Dikenakan (Pesanan Siap Dikirim)'], errors='coerce').sum()
avg_roi_created = pd.to_numeric(paylater_df['ROI (Pesanan Dibuat)'], errors='coerce').mean()
avg_roi_shipped = pd.to_numeric(paylater_df['ROI (Pesanan Siap Dikirim)'], errors='coerce').mean()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Sales (Created)",
        value=f"IDR {total_sales_created/1e6:.1f}M",
        help="Total sales from PayLater orders created"
    )

with col2:
    st.metric(
        label="📦 Sales (Shipped)",
        value=f"IDR {total_sales_shipped/1e6:.1f}M",
        help="Total sales from PayLater orders shipped"
    )

with col3:
    st.metric(
        label="🛒 Total Orders",
        value=f"{int(total_orders_created):,}",
        delta=f"{int(total_orders_shipped):,} shipped",
        help="Orders created vs shipped"
    )

with col4:
    # Handle NaN ROI
    roi_display = f"{avg_roi_created:.1f}%" if not pd.isna(avg_roi_created) else "N/A"
    st.metric(
        label="📈 Avg ROI",
        value=roi_display,
        help="Return on investment (limited data)"
    )

st.markdown("---")

# Sales Overview
st.markdown("## 📊 Sales Overview")

col1, col2 = st.columns(2)

with col1:
    # Sales comparison
    sales_data = pd.DataFrame({
        'Stage': ['Orders Created', 'Orders Shipped'],
        'Sales': [total_sales_created, total_sales_shipped]
    })
    
    fig = px.bar(
        sales_data,
        x='Stage',
        y='Sales',
        title='Sales: Created vs Shipped (IDR)',
        color='Sales',
        color_continuous_scale='Blues',
        text='Sales'
    )
    
    fig.update_traces(texttemplate='IDR %{text:.1f}M', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False
    )
    fig.update_yaxes(title='Sales (IDR)')
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Orders comparison
    orders_data = pd.DataFrame({
        'Stage': ['Orders Created', 'Orders Shipped'],
        'Orders': [total_orders_created, total_orders_shipped]
    })
    
    fig = px.bar(
        orders_data,
        x='Stage',
        y='Orders',
        title='Orders: Created vs Shipped',
        color='Orders',
        color_continuous_scale='Purples',
        text='Orders'
    )
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Performance by tenor
st.markdown("## 📅 Performance by Payment Tenor")

# Group by tenor
tenor_stats = paylater_df.groupby('Tenor').agg({
    'Sales_Orders_Created_IDR': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'Orders_Created': lambda x: pd.to_numeric(x, errors='coerce').sum(),
    'ROI (Pesanan Dibuat)': lambda x: pd.to_numeric(x, errors='coerce').mean()
}).reset_index()

tenor_stats.columns = ['Tenor', 'Total Sales (IDR)', 'Total Orders', 'Avg ROI (%)']

col1, col2 = st.columns([2, 1])

with col1:
    fig = px.bar(
        tenor_stats,
        x='Tenor',
        y='Total Sales (IDR)',
        title='Sales by Payment Tenor',
        color='Total Sales (IDR)',
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Tenor Statistics")
    st.dataframe(tenor_stats, use_container_width=True, hide_index=True)

st.markdown("---")

# Cost vs Revenue
st.markdown("## 💰 Cost vs Revenue Analysis")

col1, col2, col3 = st.columns(3)

with col1:
    net_revenue_created = total_sales_created - total_service_fee_created
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe; text-align: center;">
        <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">Revenue (Created)</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #0f172a;">IDR {total_sales_created/1e6:.1f}M</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">Gross Revenue</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #f093fb; text-align: center;">
        <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">Service Fees</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #0f172a;">IDR {total_service_fee_created/1e6:.1f}M</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">Total Cost</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10b981; text-align: center;">
        <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">Net Revenue</div>
        <div style="font-size: 1.8rem; font-weight: 800; color: #10b981;">IDR {net_revenue_created/1e6:.1f}M</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">After Fees</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Insights
st.markdown("## 💡 PayLater Insights")

col1, col2, col3 = st.columns(3)

with col1:
    if not pd.isna(avg_roi_created) and avg_roi_created > 100:
        st.success(f"✅ **Strong ROI:** {avg_roi_created:.1f}%")
        st.markdown("PayLater is highly profitable - continue promoting")
    else:
        st.info("📊 **ROI Data**: Limited - more transactions needed for analysis")

with col2:
    fulfillment_rate = (total_orders_shipped / total_orders_created * 100) if total_orders_created > 0 else 0
    if fulfillment_rate >= 80:
        st.success(f"✅ **Fulfillment:** {fulfillment_rate:.1f}%")
    else:
        st.warning(f"⚠️ **Fulfillment:** {fulfillment_rate:.1f}%")

with col3:
    avg_order_value = total_sales_created / total_orders_created if total_orders_created > 0 else 0
    st.info(f"💵 **Avg Order:** IDR {avg_order_value/1000:.0f}K")

# Recommendations
st.markdown("---")
st.markdown("## 🎯 Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe;">
        <h4 style="color: #0f172a; margin-top: 0;">📈 Promote PayLater</h4>
        <ul style="color: #64748b;">
            <li>Highlight PayLater option at checkout</li>
            <li>Offer exclusive deals for PayLater users</li>
            <li>Promote longer tenors for higher-value items</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10b981;">
        <h4 style="color: #0f172a; margin-top: 0;">💰 Optimize Costs</h4>
        <ul style="color: #64748b;">
            <li>Monitor service fee impact on margins</li>
            <li>Focus on high-ROI tenors</li>
            <li>Track fulfillment rates to reduce fees</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Summary stats instead of detailed table
st.markdown("---")
st.markdown("## 📋 PayLater Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; border: 2px solid #e2e8f0;">
        <div style="font-size: 0.9rem; color: #64748b;">Total Transactions</div>
        <div style="font-size: 2rem; font-weight: 800; color: #0f172a;">{int(total_orders_created)}</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">PayLater Orders</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; border: 2px solid #e2e8f0;">
        <div style="font-size: 0.9rem; color: #64748b;">Fulfillment Rate</div>
        <div style="font-size: 2rem; font-weight: 800; color: #4facfe;">{fulfillment_rate:.0f}%</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">Orders Shipped</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; border: 2px solid #e2e8f0;">
        <div style="font-size: 0.9rem; color: #64748b;">Avg Order Value</div>
        <div style="font-size: 2rem; font-weight: 800; color: #10b981;">IDR {avg_order_value/1000:.0f}K</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">Per Transaction</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    unique_tenors = paylater_df['Tenor'].nunique()
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; text-align: center; border: 2px solid #e2e8f0;">
        <div style="font-size: 0.9rem; color: #64748b;">Payment Options</div>
        <div style="font-size: 2rem; font-weight: 800; color: #f093fb;">{unique_tenors}</div>
        <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">Tenor Options</div>
    </div>
    """, unsafe_allow_html=True)

# Export
csv = paylater_df.to_csv(index=False)
st.download_button(
    label="📥 Download Full Data (CSV)",
    data=csv,
    file_name="shopee_paylater.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>💳 Shopee PayLater Analytics | 📊 BNPL Performance Tracking</p>
</div>
""", unsafe_allow_html=True)
