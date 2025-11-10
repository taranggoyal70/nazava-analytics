"""
Mass Chat Broadcast Analytics
Analyze mass chat campaign performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Mass Chat Broadcasts", page_icon="📢", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_12masschatbroadcasts"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load data
@st.cache_data
def load_mass_chat_data():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    df = pd.read_csv(f"{data_path}/mass_chat_data_cleaned.csv")
    return df

mass_chat_df = load_mass_chat_data()

# Header
st.markdown("# 📢 Mass Chat Broadcast Analytics")
st.markdown("### Campaign Performance & Engagement Metrics")
from datetime import datetime
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Calculate KPIs
total_recipients = pd.to_numeric(mass_chat_df['Actual_Recipients'], errors='coerce').sum()
total_read = pd.to_numeric(mass_chat_df['Recipients_Read'], errors='coerce').sum()
total_clicked = pd.to_numeric(mass_chat_df['Recipients_Clicked'], errors='coerce').sum()
total_orders = pd.to_numeric(mass_chat_df['Orders'], errors='coerce').sum()
total_sales = pd.to_numeric(mass_chat_df['Sales_IDR'], errors='coerce').sum()

# Fix decimal percentage issue - multiply by 100 if values are < 1
avg_read_rate_raw = pd.to_numeric(mass_chat_df['Read_Rate'], errors='coerce').mean()
avg_read_rate = avg_read_rate_raw * 100 if avg_read_rate_raw < 1 else avg_read_rate_raw

avg_click_rate_raw = pd.to_numeric(mass_chat_df['Click_Rate'], errors='coerce').mean()
avg_click_rate = avg_click_rate_raw * 100 if avg_click_rate_raw < 1 else avg_click_rate_raw

avg_conversion_raw = pd.to_numeric(mass_chat_df['Conversion_Rate_Respond_To_Placed'], errors='coerce').mean()
avg_conversion = avg_conversion_raw * 100 if avg_conversion_raw < 1 else avg_conversion_raw

# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="📨 Total Recipients",
        value=f"{int(total_recipients):,}",
        help="Total message recipients"
    )

with col2:
    st.metric(
        label="👁️ Read Rate",
        value=f"{avg_read_rate:.1f}%",
        help="Average message read rate"
    )

with col3:
    st.metric(
        label="👆 Click Rate",
        value=f"{avg_click_rate:.1f}%",
        help="Average click-through rate"
    )

with col4:
    st.metric(
        label="🛒 Total Orders",
        value=f"{int(total_orders):,}",
        help="Orders from broadcasts"
    )

with col5:
    st.metric(
        label="💰 Total Sales",
        value=f"IDR {total_sales/1e6:.1f}M",
        help="Revenue from broadcasts"
    )

st.markdown("---")

# Engagement Funnel
st.markdown("## 📊 Broadcast Engagement Funnel")

col1, col2 = st.columns([2, 1])

with col1:
    funnel_data = pd.DataFrame({
        'Stage': ['Sent', 'Read', 'Clicked', 'Ordered'],
        'Count': [total_recipients, total_read, total_clicked, total_orders]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        marker=dict(color=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
    ))
    
    fig.update_layout(
        title='Message to Order Conversion',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📈 Conversion Metrics")
    
    read_rate = (total_read / total_recipients * 100) if total_recipients > 0 else 0
    click_rate = (total_clicked / total_read * 100) if total_read > 0 else 0
    order_rate = (total_orders / total_clicked * 100) if total_clicked > 0 else 0
    
    st.metric("Sent → Read", f"{read_rate:.1f}%")
    st.metric("Read → Click", f"{click_rate:.1f}%")
    st.metric("Click → Order", f"{order_rate:.1f}%")
    st.metric("Overall Conversion", f"{avg_conversion:.2f}%")

st.markdown("---")

# Performance over time
st.markdown("## 📈 Campaign Performance Trends")

col1, col2 = st.columns(2)

with col1:
    # Sales trend
    sales_trend = mass_chat_df[['Data_Period', 'Sales_IDR']].copy()
    sales_trend['Sales_IDR'] = pd.to_numeric(sales_trend['Sales_IDR'], errors='coerce')
    
    fig = px.line(
        sales_trend,
        x='Data_Period',
        y='Sales_IDR',
        title='Sales from Mass Chat Broadcasts',
        labels={'Sales_IDR': 'Sales (IDR)', 'Data_Period': 'Period'}
    )
    
    fig.update_traces(line_color='#4facfe')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Engagement rates
    engagement = mass_chat_df[['Data_Period', 'Read_Rate', 'Click_Rate']].copy()
    engagement['Read_Rate'] = pd.to_numeric(engagement['Read_Rate'], errors='coerce')
    engagement['Click_Rate'] = pd.to_numeric(engagement['Click_Rate'], errors='coerce')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=engagement['Data_Period'],
        y=engagement['Read_Rate'],
        name='Read Rate',
        line=dict(color='#667eea')
    ))
    fig.add_trace(go.Scatter(
        x=engagement['Data_Period'],
        y=engagement['Click_Rate'],
        name='Click Rate',
        line=dict(color='#f093fb')
    ))
    
    fig.update_layout(
        title='Engagement Rates Over Time',
        xaxis_title='Period',
        yaxis_title='Rate (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Campaign insights
st.markdown("## 💡 Campaign Insights")

col1, col2, col3 = st.columns(3)

with col1:
    if avg_read_rate >= 50:
        st.success(f"✅ **Strong Read Rate:** {avg_read_rate:.1f}%")
    else:
        st.warning(f"⚠️ **Read Rate:** {avg_read_rate:.1f}% - Improve message timing")

with col2:
    if avg_click_rate >= 10:
        st.success(f"✅ **Good Click Rate:** {avg_click_rate:.1f}%")
    else:
        st.info(f"📊 **Click Rate:** {avg_click_rate:.1f}% - Optimize CTAs")

with col3:
    roi = ((total_sales - 0) / 1) if total_sales > 0 else 0  # Assuming minimal cost
    st.info(f"💰 **Revenue Generated:** IDR {total_sales/1e6:.1f}M")

# Recommendations
st.markdown("## 🎯 Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe;">
        <h4 style="color: #0f172a; margin-top: 0;">📱 Optimize Send Times</h4>
        <ul style="color: #64748b;">
            <li>Send during peak engagement hours (evening)</li>
            <li>Avoid early morning or late night sends</li>
            <li>Test different days of the week</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10b981;">
        <h4 style="color: #0f172a; margin-top: 0;">✍️ Improve Message Content</h4>
        <ul style="color: #64748b;">
            <li>Personalize messages with customer names</li>
            <li>Include clear call-to-action buttons</li>
            <li>Add exclusive offers or discounts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Export option (keeping only the download button)
st.markdown("---")
csv = mass_chat_df.to_csv(index=False)
st.download_button(
    label="📥 Download Full Campaign Data (CSV)",
    data=csv,
    file_name="mass_chat_broadcasts.csv",
    mime="text/csv",
    use_container_width=True
)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>📢 Mass Chat Broadcast Analytics | 💬 Engagement Tracking</p>
</div>
""", unsafe_allow_html=True)
