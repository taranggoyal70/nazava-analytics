"""
Traffic Analysis Page
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_loader import load_traffic_data, load_off_platform_data

st.set_page_config(page_title="Traffic Analysis", page_icon="🚦", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_2traffic"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Load cleaned data
traffic_df = load_traffic_data()
off_platform_df = load_off_platform_data()

# Header
st.markdown("# 🚦 Traffic Analysis")
st.markdown("### Visitor Trends & Traffic Sources")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)

total_visitors = traffic_df['Total_Visitors'].sum()
new_visitors = traffic_df['New_Visitors'].sum()
returning_visitors = traffic_df['Returning_Visitors'].sum()
new_followers = traffic_df['New_Followers'].sum()

with col1:
    st.metric(
        label="👥 Total Visitors",
        value=f"{int(total_visitors/1000):.1f}K",
        help="Total unique visitors"
    )

with col2:
    st.metric(
        label="🆕 New Visitors",
        value=f"{int(new_visitors/1000):.1f}K",
        delta=f"{(new_visitors/total_visitors*100):.1f}%",
        help="First-time visitors"
    )

with col3:
    st.metric(
        label="🔄 Returning Visitors",
        value=f"{int(returning_visitors/1000):.1f}K",
        delta=f"{(returning_visitors/total_visitors*100):.1f}%",
        help="Repeat visitors"
    )

with col4:
    st.metric(
        label="⭐ New Followers",
        value=f"{int(new_followers):,}",
        help="New shop followers"
    )

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Daily Traffic Trend")
    
    # Daily traffic
    daily_traffic = traffic_df.groupby('Date')['Total_Visitors'].sum().reset_index()
    daily_traffic = daily_traffic.sort_values('Date')
    
    fig = px.line(
        daily_traffic,
        x='Date',
        y='Total_Visitors',
        title='Daily Visitors Over Time'
    )
    fig.update_traces(line_color='#667eea', line_width=2)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 👥 New vs Returning Visitors")
    
    # Stacked area chart
    visitor_types = traffic_df.groupby('Date')[['New_Visitors', 'Returning_Visitors']].sum().reset_index()
    visitor_types = visitor_types.sort_values('Date')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=visitor_types['Date'],
        y=visitor_types['New_Visitors'],
        name='New Visitors',
        fill='tozeroy',
        line=dict(color='#667eea')
    ))
    fig.add_trace(go.Scatter(
        x=visitor_types['Date'],
        y=visitor_types['Returning_Visitors'],
        name='Returning Visitors',
        fill='tonexty',
        line=dict(color='#764ba2')
    ))
    fig.update_layout(
        title='Visitor Type Distribution',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Products Viewed")
    
    products_viewed = traffic_df.groupby('Date')['Products_Viewed'].sum().reset_index()
    products_viewed = products_viewed.sort_values('Date')
    
    fig = px.bar(
        products_viewed,
        x='Date',
        y='Products_Viewed',
        title='Daily Products Viewed'
    )
    fig.update_traces(marker_color='#667eea')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### ⏱️ Average Time Spent")
    
    time_spent = traffic_df.groupby('Date')['Average_Time_Spent'].mean().reset_index()
    time_spent = time_spent.sort_values('Date')
    
    fig = px.line(
        time_spent,
        x='Date',
        y='Average_Time_Spent',
        title='Average Session Duration (minutes)'
    )
    fig.update_traces(line_color='#764ba2', line_width=2)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Traffic Sources
if not off_platform_df.empty and 'Platform' in off_platform_df.columns:
    st.markdown("### 🌐 Traffic Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Traffic by platform
        platform_traffic = off_platform_df.groupby('Platform')['Visitors'].sum().reset_index()
        platform_traffic = platform_traffic.sort_values('Visitors', ascending=False)
        
        fig = px.bar(
            platform_traffic,
            x='Platform',
            y='Visitors',
            title='Visitors by Platform',
            color='Visitors',
            color_continuous_scale='Purples'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Traffic by channel
        if 'Channel' in off_platform_df.columns:
            channel_traffic = off_platform_df.groupby('Channel')['Visitors'].sum().reset_index()
            channel_traffic = channel_traffic.sort_values('Visitors', ascending=False).head(10)
            
            fig = px.pie(
                channel_traffic,
                values='Visitors',
                names='Channel',
                title='Top 10 Traffic Channels'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Summary Stats
st.markdown("### 📊 Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Visitor Metrics")
    avg_daily_visitors = traffic_df['Total_Visitors'].mean()
    st.write(f"**Avg Daily Visitors:** {avg_daily_visitors:,.0f}")
    st.write(f"**Peak Day Visitors:** {traffic_df['Total_Visitors'].max():,.0f}")
    st.write(f"**Lowest Day Visitors:** {traffic_df['Total_Visitors'].min():,.0f}")

with col2:
    st.markdown("#### Engagement Metrics")
    avg_products_viewed = traffic_df['Products_Viewed'].mean()
    avg_time = traffic_df['Average_Time_Spent'].mean()
    st.write(f"**Avg Products Viewed:** {avg_products_viewed:,.0f}")
    st.write(f"**Avg Time Spent:** {avg_time:.1f} min")
    st.write(f"**Avg Views per Visitor:** {traffic_df['Average_Views'].mean():.1f}")

with col3:
    st.markdown("#### Growth Metrics")
    loyalty_rate = (returning_visitors / total_visitors * 100)
    st.write(f"**Visitor Loyalty Rate:** {loyalty_rate:.1f}%")
    st.write(f"**Total New Followers:** {int(new_followers):,}")
    st.write(f"**Follower Growth Rate:** {(new_followers/total_visitors*100):.2f}%")
