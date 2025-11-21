"""
Product Recommendations Dashboard
AI-powered product insights and optimization strategies
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_models.product_recommendations import ProductRecommender, run_product_analysis

st.set_page_config(
    page_title="Product Recommendations",
    page_icon="🎯",
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
    if st.button("🚪 Logout", use_container_width=True, key="logout_products"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Header
st.markdown("# 🎯 Product Recommendations")
st.markdown("### AI-Powered Product Optimization & Strategy")
st.markdown("---")

# Load analysis
@st.cache_data
def load_analysis():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    return run_product_analysis(data_path)

with st.spinner("🤖 Analyzing product performance..."):
    recommender, performance, recommendations, cross_sell, pricing = load_analysis()

# Key metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"IDR {performance['total_sales']/1e6:.1f}M",
        help="Total product sales"
    )

with col2:
    st.metric(
        label="🛒 Total Orders",
        value=f"{performance['total_orders']:.0f}",
        help="Total orders placed"
    )

with col3:
    st.metric(
        label="📈 Conversion Rate",
        value=f"{performance['overall_conversion']:.2f}%",
        help="Visitor to purchase conversion"
    )

with col4:
    st.metric(
        label="💵 Avg Order Value",
        value=f"IDR {performance['avg_order_value']/1000:.0f}K",
        help="Average order value"
    )

with col5:
    st.metric(
        label="📦 Products Tracked",
        value=f"{performance['unique_products']:.0f}",
        help="Unique products visited"
    )

st.markdown("---")

# Conversion funnel
st.markdown("## 🎯 Product Conversion Funnel")

col1, col2 = st.columns([2, 1])

with col1:
    funnel_data = pd.DataFrame({
        'Stage': ['Visits', 'Page Views', 'Added to Cart', 'Orders'],
        'Count': [
            performance['total_visits'],
            performance['total_views'],
            performance['cart_additions'],
            performance['total_orders']
        ]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial",
        marker=dict(color=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
    ))
    
    fig.update_layout(
        title='Product Purchase Funnel',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Conversion Metrics")
    
    st.metric(
        "Visit → Cart",
        f"{performance['visit_to_cart']:.1f}%",
        help="Percentage of visitors who add to cart"
    )
    
    st.metric(
        "Cart → Order",
        f"{performance['cart_to_order']:.1f}%",
        help="Percentage of cart additions that convert to orders"
    )
    
    st.metric(
        "Overall Conversion",
        f"{performance['overall_conversion']:.2f}%",
        help="Visit to purchase conversion rate"
    )

st.markdown("---")

# Product recommendations
st.markdown("## 💡 AI-Generated Recommendations")

tab1, tab2, tab3 = st.tabs(["⭐ Top Products", "📢 Products to Promote", "🔧 Products to Optimize"])

with tab1:
    st.markdown("### ⭐ Top Performing Products")
    st.markdown("*These products are driving the most value - continue promoting them*")
    
    if recommendations['top_products']:
        for i, product in enumerate(recommendations['top_products'], 1):
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #4facfe;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a;">#{i} - {product['date']}</div>
                        <div style="color: #64748b; margin-top: 0.5rem;">
                            💰 Sales: {product['sales']} | 🛒 Orders: {product['orders']}
                        </div>
                    </div>
                    <div style="background: #e6f3ff; padding: 0.5rem 1rem; border-radius: 8px; color: #4facfe; font-weight: 600;">
                        {product['action']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No data available")

with tab2:
    st.markdown("### 📢 High-Potential Products Needing Visibility")
    st.markdown("*These products have good conversion but low traffic - boost their visibility*")
    
    if recommendations['products_to_promote']:
        for i, product in enumerate(recommendations['products_to_promote'], 1):
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #f093fb;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a;">#{i} - {product['date']}</div>
                        <div style="color: #64748b; margin-top: 0.5rem;">
                            📈 Conversion: {product['conversion']} | 👥 Visitors: {product['visitors']}
                        </div>
                    </div>
                    <div style="background: #fef3f2; padding: 0.5rem 1rem; border-radius: 8px; color: #f093fb; font-weight: 600; font-size: 0.9rem;">
                        {product['action']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No data available")

with tab3:
    st.markdown("### 🔧 Products Needing Optimization")
    st.markdown("*These products have high traffic but low conversion - optimize their listings*")
    
    if recommendations['products_to_optimize']:
        for i, product in enumerate(recommendations['products_to_optimize'], 1):
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid #764ba2;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 700; font-size: 1.1rem; color: #0f172a;">#{i} - {product['date']}</div>
                        <div style="color: #64748b; margin-top: 0.5rem;">
                            👥 Visitors: {product['visitors']} | 📉 Conversion: {product['conversion']}
                        </div>
                    </div>
                    <div style="background: #f5f3ff; padding: 0.5rem 1rem; border-radius: 8px; color: #764ba2; font-weight: 600; font-size: 0.9rem;">
                        {product['action']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No data available")

st.markdown("---")

# Cross-sell opportunities
st.markdown("## 🎁 Cross-Sell & Bundle Opportunities")

if cross_sell:
    for opp in cross_sell:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### {opp['type']}")
            st.markdown(f"**Recommendation:** {opp['recommendation']}")
            
        with col2:
            st.metric("Opportunities", f"{opp['count']}")
else:
    st.info("No cross-sell opportunities identified at this time")

st.markdown("---")

# Pricing insights
st.markdown("## 💵 Pricing Optimization Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Current Metrics")
    st.metric("Average Order Value", f"IDR {pricing['avg_order_value']/1000:.0f}K")
    st.metric("Revenue per Visitor", f"IDR {pricing['revenue_per_visitor']/1000:.1f}K")

with col2:
    st.markdown("### 💡 Optimization Strategies")
    
    for suggestion in pricing['suggestions']:
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #10b981;">
            <div style="font-weight: 600; color: #0f172a;">{suggestion['type']}</div>
            <div style="font-size: 0.9rem; color: #64748b; margin-top: 0.3rem;">{suggestion['action']}</div>
            <div style="font-size: 0.85rem; color: #10b981; margin-top: 0.3rem; font-weight: 600;">
                Expected Impact: {suggestion['expected_impact']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Strategic recommendations
st.markdown("## 🎯 Strategic Recommendations")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">🎯</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Focus on SAM Products</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Prioritize complete water filter systems (SAM products >Rp 100K) for higher margins and customer value
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; color: white;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">📦</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Create Product Bundles</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Bundle filters with accessories to increase average order value by 15-25%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; color: white;">
        <div style="font-size: 2rem; margin-bottom: 1rem;">⭐</div>
        <div style="font-weight: 700; font-size: 1.2rem; margin-bottom: 1rem;">Optimize Listings</div>
        <div style="font-size: 0.9rem; line-height: 1.6;">
            Improve product photos, descriptions, and reviews to boost conversion rates
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>🤖 Powered by AI Product Analysis | 📊 Based on Sales & Conversion Data</p>
    <p>💡 Recommendations updated based on real-time performance metrics</p>
</div>
""", unsafe_allow_html=True)
