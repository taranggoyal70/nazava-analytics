"""
Campaign Optimizer Dashboard
AI-powered campaign ROI optimization and budget allocation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_models.campaign_optimizer import CampaignOptimizer, run_campaign_optimization

st.set_page_config(
    page_title="Campaign Optimizer",
    page_icon="💡",
    layout="wide"
)

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_optimizer"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Header
st.markdown("# 🎯 Campaign ROI Optimizer")
st.markdown("### AI-Powered Marketing Budget Allocation")
st.markdown("---")

# Budget input
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    total_budget = st.number_input(
        "💰 Total Marketing Budget (IDR)",
        min_value=1000000,
        max_value=1000000000,
        value=50000000,
        step=1000000,
        help="Enter your total marketing budget for optimization"
    )

with col2:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    optimize_button = st.button("🚀 Optimize Budget", use_container_width=True)

with col3:
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    st.markdown(f"**Budget:** IDR {total_budget/1e6:.1f}M")

# Load optimization
@st.cache_data
def load_optimization(budget):
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    return run_campaign_optimization(data_path, budget)

with st.spinner("🤖 Optimizing campaign allocation..."):
    optimizer, campaigns, allocation, recommendations, timing, efficiency = load_optimization(total_budget)

st.markdown("---")

# Overall efficiency metrics
st.markdown("## 📊 Marketing Efficiency Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"IDR {efficiency['total_revenue']/1e6:.1f}M",
        help="Total revenue from all campaigns"
    )

with col2:
    st.metric(
        label="💸 Total Cost",
        value=f"IDR {efficiency['total_cost']/1e6:.1f}M",
        help="Total marketing spend"
    )

with col3:
    st.metric(
        label="📈 Overall ROI",
        value=f"{efficiency['overall_roi']:.0f}%",
        delta=f"{efficiency['overall_roi']-100:.0f}%",
        help="Return on investment"
    )

with col4:
    st.metric(
        label="💵 Cost Ratio",
        value=f"{efficiency['cost_as_percentage_of_revenue']:.1f}%",
        help="Marketing cost as % of revenue"
    )

with col5:
    st.metric(
        label="🛒 Avg Cost/Order",
        value=f"IDR {efficiency['avg_cost_per_order']/1000:.0f}K",
        help="Average cost per order"
    )

st.markdown("---")

# Campaign performance comparison
st.markdown("## 📊 Campaign Performance Comparison")

col1, col2 = st.columns(2)

with col1:
    # ROI comparison
    campaign_data = pd.DataFrame([
        {'Campaign': name, 'ROI': metrics['roi']}
        for name, metrics in campaigns.items()
    ])
    
    fig = px.bar(
        campaign_data,
        x='Campaign',
        y='ROI',
        title='ROI by Campaign Type (%)',
        color='ROI',
        color_continuous_scale=['#f5576c', '#f093fb', '#4facfe', '#10b981'],
        text='ROI'
    )
    
    fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Revenue comparison
    revenue_data = pd.DataFrame([
        {'Campaign': name, 'Revenue': metrics['revenue']/1e6}
        for name, metrics in campaigns.items()
    ])
    
    fig = px.pie(
        revenue_data,
        values='Revenue',
        names='Campaign',
        title='Revenue Distribution (IDR Millions)',
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe']
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Optimal budget allocation
st.markdown("## 💡 AI-Optimized Budget Allocation")

st.info(f"📊 Based on historical ROI data, here's the optimal allocation for IDR {total_budget/1e6:.1f}M budget")

allocation_data = pd.DataFrame([
    {
        'Campaign': name,
        'Recommended Budget': f"IDR {alloc['budget']/1e6:.1f}M",
        'Percentage': f"{alloc['percentage']:.1f}%",
        'Expected Revenue': f"IDR {alloc['expected_revenue']/1e6:.1f}M",
        'Expected Orders': f"{alloc['expected_orders']:.0f}"
    }
    for name, alloc in allocation.items()
])

st.dataframe(allocation_data, use_container_width=True, hide_index=True)

# Visualization of allocation
col1, col2 = st.columns(2)

with col1:
    alloc_viz = pd.DataFrame([
        {'Campaign': name, 'Budget': alloc['budget']/1e6}
        for name, alloc in allocation.items()
    ])
    
    fig = px.pie(
        alloc_viz,
        values='Budget',
        names='Campaign',
        title='Recommended Budget Distribution',
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe']
    )
    
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    expected_revenue = pd.DataFrame([
        {'Campaign': name, 'Expected Revenue': alloc['expected_revenue']/1e6}
        for name, alloc in allocation.items()
    ])
    
    fig = px.bar(
        expected_revenue,
        x='Campaign',
        y='Expected Revenue',
        title='Expected Revenue by Campaign (IDR M)',
        color='Expected Revenue',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Campaign recommendations
st.markdown("## 💡 AI-Generated Recommendations")

for rec in recommendations:
    priority_color = {
        'High': '#10b981',
        'Medium': '#f59e0b',
        'Low': '#ef4444'
    }.get(rec['priority'], '#64748b')
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid {priority_color};">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div style="font-weight: 700; font-size: 1.2rem; color: #0f172a; margin-bottom: 0.5rem;">
                    {rec['campaign']}
                </div>
                <div style="color: #64748b; margin-bottom: 0.5rem;">
                    {rec['status']}
                </div>
                <div style="background: #f8fafc; padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem;">
                    <div style="font-weight: 600; color: #0f172a; margin-bottom: 0.3rem;">Recommended Action:</div>
                    <div style="color: #64748b;">{rec['action']}</div>
                </div>
                <div style="margin-top: 0.5rem; color: {priority_color}; font-weight: 600;">
                    {rec['expected_impact']}
                </div>
            </div>
            <div style="background: {priority_color}; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; margin-left: 1rem;">
                {rec['priority']} Priority
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Campaign timing suggestions
st.markdown("## 🗓️ Optimal Campaign Timing")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📅 Best Days & Months")
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe;">
        <div style="font-weight: 600; color: #0f172a; margin-bottom: 1rem;">Peak Traffic Periods</div>
        <div style="margin-bottom: 0.5rem;">
            <span style="font-weight: 600;">Best Day:</span> {timing['best_day_of_week']}
        </div>
        <div>
            <span style="font-weight: 600;">Best Month:</span> {timing['best_month']}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 💡 Timing Recommendations")
    for suggestion in timing['recommendations']:
        st.markdown(f"- {suggestion}")

st.markdown("---")

# Strategic insights
st.markdown("## 🎯 Strategic Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; height: 250px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Focus on High ROI</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Prioritize campaigns with ROI >500% for maximum returns. Vouchers and Flash Sales show strongest performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; color: white; height: 250px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">💰</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Optimize Spend</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Keep marketing costs at {efficiency['cost_as_percentage_of_revenue']:.1f}% of revenue. Current efficiency is strong - maintain this ratio.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; color: white; height: 250px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">📈</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Scale Winners</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Increase budget for top-performing campaigns. Expected overall ROI: {efficiency['overall_roi']:.0f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>🤖 Powered by AI ROI Optimization | 📊 Based on Historical Campaign Performance</p>
    <p>💡 Recommendations updated in real-time based on your budget input</p>
</div>
""", unsafe_allow_html=True)
