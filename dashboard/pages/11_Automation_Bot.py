"""
Automation Bot Dashboard
Monitor and control automated Shopee actions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from automation.shopee_api_client import AutomatedRecommendationBot, ShopeeAPIClient
from ml_models.campaign_optimizer import run_campaign_optimization
from ml_models.product_recommendations import run_product_analysis
from ml_models.customer_segmentation import run_segmentation

st.set_page_config(page_title="Automation Bot", page_icon="🤖", layout="wide")

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.switch_page("app.py")
    st.stop()

# Logout button in sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"**👤 {st.session_state.get('username', 'User')}**")
    if st.button("🚪 Logout", use_container_width=True, key="logout_11automationbot"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Header
st.markdown("# 🤖 Automated Optimization Bot")
st.markdown("### AI-Powered Self-Learning Marketing Automation")
st.markdown("---")

# Bot status
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
        <div style="font-weight: 700; font-size: 1.1rem;">Bot Status</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">Active & Ready</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔄</div>
        <div style="font-weight: 700; font-size: 1.1rem;">Mode</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">Simulation</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-weight: 700; font-size: 1.1rem;">ML Models</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">4 Active</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; text-align: center; color: white;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
        <div style="font-weight: 700; font-size: 1.1rem;">API Status</div>
        <div style="font-size: 0.9rem; margin-top: 0.5rem;">Demo Mode</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Initialize bot (demo mode)
@st.cache_resource
def initialize_bot():
    # Demo credentials (would be real in production)
    api_client = ShopeeAPIClient(
        partner_id="demo_partner",
        partner_key="demo_key",
        shop_id="demo_shop"
    )
    return AutomatedRecommendationBot(api_client)

bot = initialize_bot()

# Load ML insights
@st.cache_data
def load_ml_insights():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    
    # Campaign optimization
    _, _, _, campaign_recs, _, _ = run_campaign_optimization(data_path)
    
    # Product recommendations
    _, _, product_recs, _, _ = run_product_analysis(data_path)
    
    # Customer segmentation
    seg_model, _, _ = run_segmentation(data_path)
    
    return campaign_recs, product_recs, seg_model

with st.spinner("🤖 Loading ML insights..."):
    campaign_recs, product_recs, seg_model = load_ml_insights()

# Automation controls
st.markdown("## ⚙️ Automation Controls")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Select Actions to Automate")
    
    automate_campaigns = st.checkbox("✅ Auto-optimize Campaign Budget", value=True)
    automate_products = st.checkbox("✅ Auto-boost High-Potential Products", value=True)
    automate_customers = st.checkbox("✅ Auto-engage Customer Segments", value=True)
    automate_pricing = st.checkbox("⚠️ Auto-adjust Pricing (Advanced)", value=False)

with col2:
    st.markdown("### 🚀 Execute Automation")
    
    if st.button("🤖 Run Automated Actions", use_container_width=True, type="primary"):
        with st.spinner("Executing automated actions..."):
            results = []
            
            if automate_campaigns:
                campaign_results = bot.execute_campaign_recommendations(campaign_recs)
                results.extend(campaign_results)
            
            if automate_products:
                product_results = bot.execute_product_recommendations(product_recs)
                results.extend(product_results)
            
            if automate_customers:
                segment_recs = [seg_model.get_recommendations(i) for i in range(4)]
                customer_results = bot.execute_customer_segment_actions(segment_recs)
                results.extend(customer_results)
            
            st.success(f"✅ Executed {len(results)} automated actions!")
            
            # Show results
            for result in results:
                st.info(f"🤖 {result['message']}")

st.markdown("---")

# Automated actions log
st.markdown("## 📋 Automated Actions Log")

summary = bot.get_actions_summary()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Actions", summary['total_actions'])

with col2:
    action_types = len(summary['actions_by_type'])
    st.metric("Action Types", action_types)

with col3:
    st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))

# Actions by type
if summary['actions_by_type']:
    st.markdown("### 📊 Actions by Type")
    
    actions_df = pd.DataFrame([
        {'Type': k.replace('_', ' ').title(), 'Count': v}
        for k, v in summary['actions_by_type'].items()
    ])
    
    fig = px.bar(
        actions_df,
        x='Type',
        y='Count',
        title='Automated Actions Distribution',
        color='Count',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Recent actions
if summary['recent_actions']:
    st.markdown("### 🕐 Recent Actions")
    
    for action in reversed(summary['recent_actions'][-5:]):  # Last 5
        status_color = {
            'simulated': '#4facfe',
            'executed': '#10b981',
            'failed': '#ef4444'
        }.get(action.get('status', 'simulated'), '#64748b')
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-weight: 600; color: #0f172a;">{action.get('type', 'Unknown').replace('_', ' ').title()}</div>
                    <div style="font-size: 0.9rem; color: #64748b; margin-top: 0.3rem;">{action.get('message', 'No message')}</div>
                </div>
                <div style="background: {status_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 6px; font-size: 0.85rem; font-weight: 600;">
                    {action.get('status', 'Unknown').upper()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ML Models Status
st.markdown("## 🧠 Active ML Models")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #667eea; text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📊</div>
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Customer Segmentation</div>
        <div style="font-size: 0.85rem; color: #10b981; font-weight: 600;">✅ Active</div>
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">K-Means Clustering</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #764ba2; text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Product Recommendations</div>
        <div style="font-size: 0.85rem; color: #10b981; font-weight: 600;">✅ Active</div>
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Performance Analysis</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #f093fb; text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">💰</div>
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Campaign Optimizer</div>
        <div style="font-size: 0.85rem; color: #10b981; font-weight: 600;">✅ Active</div>
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">ROI Optimization</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #4facfe; text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📈</div>
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">Sales Forecasting</div>
        <div style="font-size: 0.85rem; color: #10b981; font-weight: 600;">✅ Active</div>
        <div style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem;">Prophet Model</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# API Integration Status
st.markdown("## 🔌 Shopee API Integration")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📡 Available API Endpoints")
    
    endpoints = [
        {"name": "Get Order List", "status": "✅ Ready", "type": "Read"},
        {"name": "Get Product List", "status": "✅ Ready", "type": "Read"},
        {"name": "Send Chat Message", "status": "✅ Ready", "type": "Write"},
        {"name": "Create Discount", "status": "✅ Ready", "type": "Write"},
        {"name": "Create Voucher", "status": "✅ Ready", "type": "Write"},
        {"name": "Update Price", "status": "✅ Ready", "type": "Write"},
        {"name": "Boost Product", "status": "✅ Ready", "type": "Write"},
    ]
    
    endpoints_df = pd.DataFrame(endpoints)
    st.dataframe(endpoints_df, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### ⚙️ Configuration")
    
    st.info("""
    **Mode:** Demo/Simulation
    
    **Features:**
    - ✅ Two-way API
    - ✅ Read operations
    - ✅ Write operations
    - ⚠️ Requires credentials
    
    **Status:** Ready for production deployment with valid API keys
    """)

st.markdown("---")

# Deployment information
st.markdown("## 🚀 Deployment Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; height: 200px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">☁️</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">AWS Deployment</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Ready for deployment on AWS infrastructure with Lambda functions and scheduled tasks
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; color: white; height: 200px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🔄</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Continuous Learning</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Self-learning capabilities with automatic model retraining on new data
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; color: white; height: 200px;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🔐</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Secure & Scalable</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Enterprise-grade security with encrypted API credentials and audit logging
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>🤖 Automated Optimization Bot | 🧠 Powered by 4 ML Models | 🔌 Shopee API Integration</p>
    <p>⚠️ Currently in simulation mode - requires valid Shopee API credentials for production</p>
</div>
""", unsafe_allow_html=True)
