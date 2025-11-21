"""
Sales Forecast - 6 Month Prediction with XGBoost
89.18% Accuracy with Full Marketing Integration

Based on Jupyter Notebook: Nazava_FINAL_GradientBoosting.ipynb
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

st.set_page_config(
    page_title="Sales Forecast - Nazava Analytics",
    page_icon="🔮",
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
    if st.button("🚪 Logout", use_container_width=True, key="logout_forecast"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("app.py")

# Header
st.markdown("# 🔮 6-Month Sales Forecast")
st.markdown("### **AI-Powered Prediction using XGBoost (89.18% Accuracy)**")
st.markdown("*Includes seasonality, promotional periods, and advertising spend*")

# Data info
col1, col2 = st.columns([3, 1])
with col2:
    st.success("✅ **Model Status**: Active")

st.markdown("---")

# Load the XGBoost forecasting model
@st.cache_data
def load_forecast_data():
    """Load or generate forecast data using XGBoost"""
    try:
        from ml.forecasting.xgboost_forecaster import XGBoostSalesForecaster
        
        with st.spinner("🤖 Training XGBoost model..."):
            forecaster = XGBoostSalesForecaster()
            
            # Load data
            weekly_sales = forecaster.load_data()
            
            # Train model
            train_data, test_data, y_pred_test = forecaster.train_model(weekly_sales)
            
            # Generate forecast
            future_forecast = forecaster.forecast_future(weeks=26)
            
            # Get feature importance
            feature_importance = forecaster.get_feature_importance()
            
            return {
                'weekly_sales': weekly_sales,
                'future_forecast': future_forecast,
                'metrics': forecaster.metrics,
                'feature_importance': feature_importance,
                'test_data': test_data,
                'y_pred_test': y_pred_test
            }
    except Exception as e:
        st.error(f"❌ Error loading forecast: {str(e)}")
        st.exception(e)
        return None

# Load data with spinner
with st.spinner("🤖 Training XGBoost model and generating forecast... This may take a moment."):
    forecast_data = load_forecast_data()

if forecast_data:
    weekly_sales = forecast_data['weekly_sales']
    future_forecast = forecast_data['future_forecast']
    metrics = forecast_data['metrics']
    feature_importance = forecast_data['feature_importance']
    test_data = forecast_data['test_data']
    y_pred_test = forecast_data['y_pred_test']
    
    # Key Metrics
    st.markdown("## 📊 Model Performance & Forecast Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_forecast = future_forecast['Predicted_Sales'].sum()
    avg_weekly = future_forecast['Predicted_Sales'].mean()
    
    with col1:
        st.metric(
            label="🎯 Model Accuracy",
            value=f"{metrics['Test_Accuracy']:.2f}%",
            delta="XGBoost",
            help="Tested on withheld data (80/20 split)"
        )
    
    with col2:
        st.metric(
            label="📊 Test MAPE",
            value=f"{metrics['Test_MAPE']:.2f}%",
            delta=f"R² {metrics['Test_R2']:.3f}",
            help="Mean Absolute Percentage Error on test set"
        )
    
    with col3:
        # Calculate growth vs last 6 months (26 weeks)
        last_26_weeks_sales = weekly_sales.tail(26)['Total_Sales'].sum()
        growth_pct = ((total_forecast / last_26_weeks_sales) - 1) * 100 if last_26_weeks_sales > 0 else 0
        
        st.metric(
            label="💰 Total 6-Month Forecast",
            value=f"IDR {total_forecast/1e9:.2f}B",
            delta=f"{growth_pct:+.1f}% vs last 6 months",
            help="Forecast for next 26 weeks"
        )
    
    with col4:
        st.metric(
            label="📅 Average Weekly Sales",
            value=f"IDR {avg_weekly/1e6:.1f}M",
            delta="Predicted"
        )
    
    with col5:
        st.metric(
            label="📈 Test MAE",
            value=f"IDR {metrics['Test_MAE']/1e6:.2f}M",
            delta=f"{metrics['Test_MAE']/weekly_sales['Total_Sales'].mean()*100:.1f}% of avg",
            help="Mean Absolute Error on test set"
        )
    
    # Model Info
    st.info(f"""
    **🤖 Model Details:**
    - **Algorithm**: XGBoost (Gradient Boosting)
    - **Features**: 25+ (time, sales, marketing)
    - **Training Data**: {len(weekly_sales)} weeks ({weekly_sales['Week'].min().date()} to {weekly_sales['Week'].max().date()})
    - **Validation**: 80/20 train/test split + 5-fold cross-validation
    - **Marketing Integration**: ✅ Flash sales, vouchers, live streams, games, ad spend
    """)
    
    st.markdown("---")
    
    # Main Forecast Chart
    st.markdown("## 📈 Weekly Sales Forecast (Next 6 Months)")
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=weekly_sales['Week'],
        y=weekly_sales['Total_Sales']/1e6,
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='#667eea', width=2),
        marker=dict(size=6),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Sales: IDR %{y:.2f}M<extra></extra>'
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=future_forecast['Week'],
        y=future_forecast['Predicted_Sales']/1e6,
        mode='lines+markers',
        name=f'Forecast (89.18% Acc)',
        line=dict(color='#f093fb', width=3, dash='dash'),
        marker=dict(size=8),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Forecast: IDR %{y:.2f}M<extra></extra>'
    ))
    
    fig.update_layout(
        title='6-Month Weekly Sales Forecast with XGBoost',
        xaxis_title='Week',
        yaxis_title='Sales (Million IDR)',
        height=600,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Two columns for additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Model Validation: Actual vs Predicted")
        
        # Create validation chart
        fig_val = go.Figure()
        
        fig_val.add_trace(go.Scatter(
            x=test_data['Week'],
            y=test_data['Total_Sales']/1e6,
            mode='lines+markers',
            name='Actual',
            line=dict(color='black', width=3),
            marker=dict(size=10)
        ))
        
        fig_val.add_trace(go.Scatter(
            x=test_data['Week'],
            y=y_pred_test/1e6,
            mode='lines+markers',
            name='Predicted',
            line=dict(color='#f093fb', width=3),
            marker=dict(size=8)
        ))
        
        fig_val.update_layout(
            title=f'Test Set Performance: {metrics["Test_Accuracy"]:.1f}% Accuracy',
            xaxis_title='Week',
            yaxis_title='Sales (Million IDR)',
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_val, use_container_width=True)
        
        st.success(f"""
        **✅ Model Validation Results:**
        - Test Accuracy: {metrics['Test_Accuracy']:.2f}%
        - MAPE: {metrics['Test_MAPE']:.2f}%
        - R²: {metrics['Test_R2']:.4f}
        - MAE: IDR {metrics['Test_MAE']/1e6:.2f}M
        """)
    
    with col2:
        st.markdown("### 🔍 Top 10 Feature Importance")
        
        # Feature importance chart
        top_features = feature_importance.head(10)
        
        fig_feat = px.bar(
            top_features,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Most Important Predictive Features',
            color='Importance',
            color_continuous_scale='Viridis'
        )
        
        fig_feat.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_feat, use_container_width=True)
        
        st.info(f"""
        **📊 Key Drivers:**
        1. {top_features.iloc[0]['Feature']}: {top_features.iloc[0]['Importance']:.1%}
        2. {top_features.iloc[1]['Feature']}: {top_features.iloc[1]['Importance']:.1%}
        3. {top_features.iloc[2]['Feature']}: {top_features.iloc[2]['Importance']:.1%}
        """)
    
    st.markdown("---")
    
    # Monthly Forecast Summary
    st.markdown("## 📅 Monthly Forecast Breakdown")
    
    # Aggregate to monthly
    future_forecast['Month'] = future_forecast['Week'].dt.to_period('M').astype(str)
    monthly_forecast = future_forecast.groupby('Month').agg({
        'Predicted_Sales': 'sum',
        'Week': 'count'
    }).reset_index()
    monthly_forecast.columns = ['Month', 'Total_Sales', 'Weeks']
    
    # Display monthly table
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_monthly = px.bar(
            monthly_forecast,
            x='Month',
            y='Total_Sales',
            title='Monthly Sales Forecast',
            labels={'Total_Sales': 'Sales (IDR)', 'Month': 'Month'},
            color='Total_Sales',
            color_continuous_scale='Blues'
        )
        
        fig_monthly.update_layout(
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig_monthly.update_traces(
            hovertemplate='<b>%{x}</b><br>Sales: IDR %{y:,.0f}<extra></extra>'
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Monthly Summary")
        
        for _, row in monthly_forecast.iterrows():
            st.metric(
                label=f"📅 {row['Month']}",
                value=f"IDR {row['Total_Sales']/1e6:.1f}M",
                delta=f"{row['Weeks']} weeks"
            )
    
    st.markdown("---")
    
    # Forecast Table
    st.markdown("## 📋 Detailed Weekly Forecast")
    
    # Prepare display dataframe
    display_df = future_forecast[['Week', 'Predicted_Sales']].copy()
    display_df['Week'] = display_df['Week'].dt.strftime('%Y-%m-%d')
    display_df['Predicted_Sales'] = display_df['Predicted_Sales'].apply(lambda x: f"IDR {x/1e6:.2f}M")
    display_df.columns = ['Week Starting', 'Predicted Sales']
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download button
    csv = future_forecast[['Week', 'Predicted_Sales']].to_csv(index=False)
    st.download_button(
        label="📥 Download Forecast CSV",
        data=csv,
        file_name="weekly_sales_forecast_6months_XGBoost.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Model Insights
    st.markdown("## 💡 Key Insights & Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 12px; color: white;">
            <h4 style="margin-top: 0;">🎯 Model Strengths</h4>
            <ul>
                <li>89.18% accuracy on test data</li>
                <li>Accounts for seasonality</li>
                <li>Includes promotional impact</li>
                <li>Tracks advertising ROI</li>
                <li>Validated with cross-validation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_forecast = future_forecast['Predicted_Sales'].mean()
        avg_historical = weekly_sales['Total_Sales'].mean()
        growth = ((avg_forecast / avg_historical) - 1) * 100
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; color: white;">
            <h4 style="margin-top: 0;">📈 Growth Projection</h4>
            <ul>
                <li>Avg weekly: IDR {avg_forecast/1e6:.1f}M</li>
                <li>Historical avg: IDR {avg_historical/1e6:.1f}M</li>
                <li>Growth: {growth:+.1f}%</li>
                <li>Total 6-month: IDR {total_forecast/1e9:.2f}B</li>
                <li>Confidence: High (89%)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; color: white;">
            <h4 style="margin-top: 0;">💡 Recommendations</h4>
            <ul>
                <li>Maintain promotional cadence</li>
                <li>Optimize ad spend for ROI</li>
                <li>Focus on top product categories</li>
                <li>Plan inventory based on forecast</li>
                <li>Monitor actual vs predicted weekly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical Details
    with st.expander("🔧 Technical Details & Methodology"):
        st.markdown("""
        ### Model Architecture: XGBoost Regressor
        
        **Hyperparameters:**
        - n_estimators: 200
        - max_depth: 6
        - learning_rate: 0.05
        - subsample: 0.85
        - colsample_bytree: 0.85
        - reg_lambda: 1 (L2 regularization)
        
        **Features (25+):**
        
        **Time Features (6):**
        - week_of_year, month, quarter, year
        - is_month_start, is_month_end
        
        **Sales Features (12):**
        - Lag features (1, 2, 3 weeks)
        - Rolling averages (3, 4 weeks)
        - Volatility (rolling std)
        - Interaction features (ratios)
        - Trend features (differences)
        
        **Marketing Features (8+):**
        - Total_Ad_Spend
        - Ad spend lags and moving averages
        - Sales per ad dollar (ROI)
        - Promotional indicators
        - Voucher ROI
        - Flash sales impact
        
        **Validation:**
        - 80/20 train/test split
        - 5-fold cross-validation
        - No overfitting detected
        - Tested on withheld data
        
        **Data Source:**
        - Weekly aggregated sales (58 weeks)
        - Period: Jan 2024 - Oct 2025
        - Includes promotional and ad spend data
        """)

else:
    st.error("❌ Could not load forecast data. Please check the data files and model configuration.")
    st.info("💡 Ensure the following files exist:")
    st.code("""
    - data/processed/weekly_sales_CLEAN.csv
    - analytical-showdown-pipeline/cleaned_data/flash_sale_cleaned.csv
    - analytical-showdown-pipeline/cleaned_data/voucher_cleaned.csv
    - analytical-showdown-pipeline/cleaned_data/live_cleaned.csv
    - analytical-showdown-pipeline/cleaned_data/game_cleaned.csv
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.9rem;">
    <p>🔮 Sales Forecast | 🤖 XGBoost ML Model | 📊 89.18% Accuracy</p>
    <p>Based on Jupyter Notebook: Nazava_FINAL_GradientBoosting.ipynb</p>
</div>
""", unsafe_allow_html=True)
