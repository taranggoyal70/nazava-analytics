"""
Customer Segmentation Dashboard
ML-powered customer insights and recommendations
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml_models.customer_segmentation import CustomerSegmentation, run_segmentation

st.set_page_config(
    page_title="Customer Segments",
    page_icon="👥",
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
    if st.button("🚪 Logout", use_container_width=True, key="logout_segments"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Header
st.markdown("# 👥 Customer Segmentation")
st.markdown("### AI-Powered Customer Insights & Targeting")
st.markdown("---")

# Load data and run segmentation
@st.cache_data
def load_segmentation():
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    model, segments_df, labels = run_segmentation(data_path)
    return model, segments_df, labels

with st.spinner("🤖 Running AI segmentation model..."):
    model, segments_df, labels = load_segmentation()

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📊 Total Segments",
        value="4",
        help="Number of customer segments identified"
    )

with col2:
    st.metric(
        label="🎯 Segmentation Method",
        value="K-Means",
        help="Machine learning clustering algorithm"
    )

with col3:
    total_days = len(segments_df)
    st.metric(
        label="📅 Days Analyzed",
        value=f"{total_days}",
        help="Days of customer behavior data"
    )

with col4:
    st.metric(
        label="🔍 Features Used",
        value=f"{len(model.feature_names)}",
        help="Customer behavior features"
    )

st.markdown("---")

# Segment visualization
st.markdown("## 📊 Customer Segment Visualization")

col1, col2 = st.columns([2, 1])

with col1:
    # PCA visualization
    fig = model.visualize_clusters(segments_df.drop(columns=['month', 'Segment'], errors='ignore'), labels)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🎯 Segment Distribution")
    
    # Descriptive segment names
    segment_names = {
        0: "🎯 Standard Customers",
        1: "💎 Premium Customers",
        2: "📈 Growing Customers",
        3: "❤️ Loyal Customers"
    }
    
    # Count by segment
    segment_counts = pd.Series(labels).value_counts().sort_index()
    
    for i, count in segment_counts.items():
        percentage = (count / len(labels)) * 100
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #4facfe;">
            <div style="font-weight: 600; color: #0f172a;">{segment_names.get(i, f'Segment {i+1}')}</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #4facfe;">{percentage:.1f}%</div>
            <div style="font-size: 0.9rem; color: #64748b;">{count} days</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Segment profiles - Redesigned for better presentation
st.markdown("## 📋 Segment Profiles")

# Create 4 columns for segment cards
cols = st.columns(4)

segment_names = {
    0: "🎯 Standard",
    1: "💎 Premium", 
    2: "📈 Growing",
    3: "❤️ Loyal"
}

segment_colors = {
    0: "#667eea",
    1: "#764ba2",
    2: "#f093fb",
    3: "#4facfe"
}

for i, col in enumerate(cols):
    if i in model.cluster_profiles:
        profile = model.cluster_profiles[i]
        metrics = profile['mean_values']
        
        with col:
            # Segment card with custom styling
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {segment_colors[i]}15 0%, {segment_colors[i]}05 100%); 
                        padding: 1.5rem; border-radius: 12px; border: 2px solid {segment_colors[i]}40;
                        height: 280px;">
                <div style="font-size: 1.5rem; font-weight: 700; color: {segment_colors[i]}; margin-bottom: 0.5rem;">
                    {segment_names[i]}
                </div>
                <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 1rem;">
                    {profile['size']} days
                </div>
                <div style="background: white; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                    <div style="font-size: 0.8rem; color: #64748b;">Avg Sales</div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: #0f172a;">
                        IDR {metrics.get('total_sales', 0)/1e6:.1f}M
                    </div>
                </div>
                <div style="background: white; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                    <div style="font-size: 0.8rem; color: #64748b;">Avg Orders</div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: #0f172a;">
                        {metrics.get('total_orders', 0):.0f}
                    </div>
                </div>
                <div style="background: white; padding: 0.75rem; border-radius: 8px;">
                    <div style="font-size: 0.8rem; color: #64748b;">CSAT Score</div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: #0f172a;">
                        {metrics.get('csat_score', 0):.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# Detailed segment analysis
st.markdown("## 🔍 Detailed Segment Analysis")

# Use same descriptive names
segment_names = {
    0: "🎯 Standard",
    1: "💎 Premium",
    2: "📈 Growing",
    3: "❤️ Loyal"
}

tabs = st.tabs([segment_names[i] for i in range(4)])

for i, tab in enumerate(tabs):
    with tab:
        # Get recommendations
        rec = model.get_recommendations(i)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"### {rec['segment_name']}")
            
            # Segment characteristics
            if i in model.cluster_profiles:
                profile = model.cluster_profiles[i]
                st.markdown(f"**Size:** {profile['size']} days")
                st.markdown(f"**Characteristics:** {profile['characteristics']}")
                
                # Key metrics
                st.markdown("#### 📊 Average Metrics")
                metrics = profile['mean_values']
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Sales", f"IDR {metrics.get('total_sales', 0)/1e6:.1f}M")
                    st.metric("Total Orders", f"{metrics.get('total_orders', 0):.0f}")
                with col_b:
                    st.metric("Visitors", f"{metrics.get('total_visitors', 0):.0f}")
                    st.metric("CSAT Score", f"{metrics.get('csat_score', 0):.1f}%")
        
        with col2:
            st.markdown("### 💡 Marketing Recommendations")
            
            for action in rec['actions']:
                st.markdown(f"- {action}")
            
            st.markdown("---")
            
            st.markdown("### 🎯 Suggested Actions")
            st.info(f"""
            **Priority Level:** {'🔴 High' if i == 0 else '🟡 Medium' if i == 1 else '🟢 Low'}
            
            **Focus Areas:**
            - Customer retention strategies
            - Personalized marketing campaigns
            - Product recommendations
            - Engagement optimization
            """)

st.markdown("---")

# Time series by segment
st.markdown("## 📈 Segment Performance Over Time")

# Add segment labels to dataframe
segments_df['Segment_Name'] = segments_df['Segment'].apply(
    lambda x: model.get_recommendations(x)['segment_name']
)

# Plot sales over time by segment
import plotly.express as px

fig = px.line(
    segments_df,
    x='month',
    y='total_sales',
    color='Segment_Name',
    title='Sales Performance by Customer Segment',
    labels={'total_sales': 'Total Sales (IDR)', 'month': 'Month'},
    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe']
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Export options
st.markdown("## 📥 Export Segment Data")

col1, col2 = st.columns(2)

with col1:
    # Download segment assignments
    csv = segments_df.to_csv(index=False)
    st.download_button(
        label="📊 Download Segment Data (CSV)",
        data=csv,
        file_name="customer_segments.csv",
        mime="text/csv"
    )

with col2:
    # Download recommendations
    recommendations_text = ""
    for i in range(4):
        rec = model.get_recommendations(i)
        recommendations_text += f"\n{rec['segment_name']}\n"
        recommendations_text += "=" * 50 + "\n"
        for action in rec['actions']:
            recommendations_text += f"{action}\n"
        recommendations_text += "\n"
    
    st.download_button(
        label="💡 Download Recommendations (TXT)",
        data=recommendations_text,
        file_name="segment_recommendations.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>🤖 Powered by K-Means Clustering | 📊 Based on RFM Analysis</p>
    <p>💡 Segments updated based on customer behavior patterns</p>
</div>
""", unsafe_allow_html=True)
