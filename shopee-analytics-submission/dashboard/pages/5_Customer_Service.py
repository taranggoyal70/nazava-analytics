"""
Customer Service Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Customer Service", page_icon="💬", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_5customerservice"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load data
@st.cache_data
def load_cs_data():
    """Load customer service data"""
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    
    chat_df = pd.read_csv(f"{data_path}/chat_data_cleaned.csv")
    mass_chat_df = pd.read_csv(f"{data_path}/mass_chat_data_cleaned.csv")
    
    return chat_df, mass_chat_df

chat_df, mass_chat_df = load_cs_data()

# Header
st.markdown("# 💬 Customer Service Analytics")
st.markdown("### Chat Performance & Customer Satisfaction")
st.markdown("---")

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)

total_chats = chat_df['Number_Of_Chats'].sum()
chats_replied = chat_df['Chats_Replied'].sum()
avg_response_time = chat_df['Average_Response_Time'].mean()
avg_csat = chat_df['CSAT_Percent'].mean() * 100
conversion_rate = chat_df['Conversion_Rate_Chats_Replied'].mean() * 100

with col1:
    st.metric(
        label="💬 Total Chats",
        value=f"{int(total_chats):,}",
        help="Total chat conversations"
    )

with col2:
    reply_rate = (chats_replied / total_chats * 100) if total_chats > 0 else 0
    st.metric(
        label="✅ Reply Rate",
        value=f"{reply_rate:.1f}%",
        help="Percentage of chats replied"
    )

with col3:
    st.metric(
        label="⏱️ Avg Response Time",
        value=f"{avg_response_time:.1f} min",
        help="Average time to respond"
    )

with col4:
    st.metric(
        label="😊 CSAT Score",
        value=f"{avg_csat:.1f}%",
        help="Customer satisfaction score"
    )

with col5:
    st.metric(
        label="💰 Chat Conversion",
        value=f"{conversion_rate:.2f}%",
        help="Chat to sale conversion rate"
    )

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Chat Volume Trend")
    
    chat_trend = chat_df.copy()
    chat_trend['Period'] = range(1, len(chat_trend) + 1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chat_trend['Period'],
        y=chat_trend['Number_Of_Chats'],
        name='Total Chats',
        line=dict(color='#667eea', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=chat_trend['Period'],
        y=chat_trend['Chats_Replied'],
        name='Chats Replied',
        line=dict(color='#764ba2', width=3)
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ⏱️ Response Time Trend")
    
    response_trend = chat_df.copy()
    response_trend['Period'] = range(1, len(response_trend) + 1)
    
    fig = px.line(
        response_trend,
        x='Period',
        y='Average_Response_Time',
        title='Average Response Time Over Time'
    )
    fig.update_traces(line_color='#764ba2', line_width=3)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        yaxis_title='Response Time (minutes)'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 😊 CSAT Score Trend")
    
    csat_trend = chat_df.copy()
    csat_trend['Period'] = range(1, len(csat_trend) + 1)
    csat_trend['CSAT_Percent'] = csat_trend['CSAT_Percent'] * 100
    
    fig = px.bar(
        csat_trend,
        x='Period',
        y='CSAT_Percent',
        title='Customer Satisfaction Score'
    )
    fig.update_traces(marker_color='#667eea')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        yaxis_title='CSAT %'
    )
    # Add target line
    fig.add_hline(y=90, line_dash="dash", line_color="green", annotation_text="Target: 90%")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 💰 Chat to Sale Conversion")
    
    conversion_trend = chat_df.copy()
    conversion_trend['Period'] = range(1, len(conversion_trend) + 1)
    conversion_trend['Conversion_Rate_Chats_Replied'] = conversion_trend['Conversion_Rate_Chats_Replied'] * 100
    
    fig = px.area(
        conversion_trend,
        x='Period',
        y='Conversion_Rate_Chats_Replied',
        title='Chat Conversion Rate'
    )
    fig.update_traces(line_color='#764ba2', fillcolor='rgba(118, 75, 162, 0.3)')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        yaxis_title='Conversion Rate %'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Chat Performance Metrics
st.markdown("### 📊 Detailed Chat Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Response Metrics")
    st.write(f"**Total Chats:** {int(total_chats):,}")
    st.write(f"**Chats Replied:** {int(chats_replied):,}")
    st.write(f"**Chats Not Replied:** {int(chat_df['Chats_Not_Replied'].sum()):,}")
    st.write(f"**Reply Rate:** {reply_rate:.1f}%")

with col2:
    st.markdown("#### Time Metrics")
    st.write(f"**Avg Response Time:** {avg_response_time:.1f} min")
    st.write(f"**First Response Time:** {chat_df['First_Chat_Response_Time'].mean():.1f} min")
    st.write(f"**Fastest Response:** {chat_df['Average_Response_Time'].min():.1f} min")
    st.write(f"**Slowest Response:** {chat_df['Average_Response_Time'].max():.1f} min")

with col3:
    st.markdown("#### Business Impact")
    total_sales_from_chat = chat_df['Sales_IDR'].sum()
    total_orders_from_chat = chat_df['Total_Orders'].sum()
    st.write(f"**Sales from Chat:** IDR {total_sales_from_chat/1e6:.1f}M")
    st.write(f"**Orders from Chat:** {int(total_orders_from_chat):,}")
    st.write(f"**Avg CSAT:** {avg_csat:.1f}%")
    st.write(f"**Conversion Rate:** {conversion_rate:.2f}%")

st.markdown("---")

# Mass Chat Performance
if not mass_chat_df.empty:
    st.markdown("### 📢 Broadcast Chat Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_recipients = mass_chat_df['Actual_Recipients'].sum()
        st.metric(
            label="Total Recipients",
            value=f"{int(total_recipients):,}"
        )
    
    with col2:
        read_rate = mass_chat_df['Read_Rate'].mean() * 100
        st.metric(
            label="Avg Read Rate",
            value=f"{read_rate:.1f}%"
        )
    
    with col3:
        click_rate = mass_chat_df['Click_Rate'].mean() * 100
        st.metric(
            label="Avg Click Rate",
            value=f"{click_rate:.1f}%"
        )
    
    with col4:
        broadcast_orders = mass_chat_df['Orders'].sum()
        st.metric(
            label="Orders from Broadcast",
            value=f"{int(broadcast_orders):,}"
        )

st.markdown("---")

# Performance Summary
st.markdown("### 💡 Performance Insights")

col1, col2 = st.columns(2)

with col1:
    if avg_csat >= 90:
        st.success(f"✅ **Excellent CSAT Score:** {avg_csat:.1f}% (Target: 90%)")
    else:
        st.warning(f"⚠️ **CSAT Below Target:** {avg_csat:.1f}% (Target: 90%)")
    
    if avg_response_time <= 5:
        st.success(f"✅ **Fast Response Time:** {avg_response_time:.1f} min")
    else:
        st.info(f"📊 **Response Time:** {avg_response_time:.1f} min")

with col2:
    if reply_rate >= 95:
        st.success(f"✅ **High Reply Rate:** {reply_rate:.1f}%")
    else:
        st.warning(f"⚠️ **Reply Rate:** {reply_rate:.1f}% - Room for improvement")
    
    st.info(f"💰 **Revenue from Chat:** IDR {total_sales_from_chat/1e6:.1f}M")
