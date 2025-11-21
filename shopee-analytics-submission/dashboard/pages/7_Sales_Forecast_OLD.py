"""
Sales Forecast - 6 Month Prediction
Shows the Prophet ML model's sales forecasting results
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

st.title("🔮 6-Month Sales Forecast")
st.markdown("**AI-Powered Sales Prediction using Prophet ML Model**")

# Load the forecasting model results
@st.cache_data
def load_forecast_data():
    """Load or generate forecast data"""
    try:
        # Try to run the forecaster
        from ml.forecasting.final_sales_forecaster import FinalSalesForecaster
        
        forecaster = FinalSalesForecaster()
        sales_data = forecaster.load_data()
        train_df = forecaster.train_model(sales_data)
        daily_forecast, weekly_forecast = forecaster.forecast_future(weeks=26)
        
        return {
            'daily_forecast': daily_forecast,
            'weekly_forecast': weekly_forecast,
            'historical': sales_data,
            'metrics': forecaster.metrics
        }
    except Exception as e:
        st.error(f"Error loading forecast: {str(e)}")
        return None

# Load data
with st.spinner("🔮 Loading forecast data..."):
    forecast_data = load_forecast_data()

if forecast_data:
    daily_forecast = forecast_data['daily_forecast']
    weekly_forecast = forecast_data['weekly_forecast']
    historical = forecast_data['historical']
    metrics = forecast_data['metrics']
    
    # Key Metrics
    st.markdown("---")
    st.markdown("## 📊 Forecast Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_forecast = daily_forecast['yhat'].sum()
    avg_weekly = weekly_forecast['yhat'].mean()
    avg_daily = daily_forecast['yhat'].mean()
    
    with col1:
        st.metric(
            label="💰 Total 6-Month Forecast",
            value=f"IDR {total_forecast/1e9:.2f}B",
            delta=f"{(total_forecast/historical['y'].sum() - 1)*100:.1f}% vs historical"
        )
    
    with col2:
        st.metric(
            label="📅 Average Weekly Sales",
            value=f"IDR {avg_weekly/1e6:.1f}M",
            delta="Predicted"
        )
    
    with col3:
        st.metric(
            label="📈 Average Daily Sales",
            value=f"IDR {avg_daily/1e6:.2f}M",
            delta=f"{metrics['Accuracy']:.1f}% accuracy"
        )
    
    with col4:
        st.metric(
            label="🎯 Model Accuracy",
            value=f"{metrics['Accuracy']:.1f}%",
            delta="Good" if metrics['Accuracy'] >= 70 else "Fair"
        )
    
    # Main Forecast Chart
    st.markdown("---")
    st.markdown("## 📈 Daily Sales Forecast (Next 6 Months)")
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=historical['ds'],
        y=historical['y'],
        mode='lines+markers',
        name='Historical Sales',
        line=dict(color='#4a5568', width=2),
        marker=dict(size=4)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=daily_forecast['ds'],
        y=daily_forecast['yhat'],
        mode='lines',
        name='Forecast',
        line=dict(color='#4facfe', width=3)
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=daily_forecast['ds'],
        y=daily_forecast['yhat_upper'],
        mode='lines',
        name='Upper Bound (95%)',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_forecast['ds'],
        y=daily_forecast['yhat_lower'],
        mode='lines',
        name='Confidence Interval',
        line=dict(width=0),
        fillcolor='rgba(79, 172, 254, 0.2)',
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Daily Sales: Historical + 6-Month Forecast",
        xaxis_title="Date",
        yaxis_title="Sales (IDR)",
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Weekly Forecast Table
    st.markdown("---")
    st.markdown("## 📅 Weekly Forecast Breakdown")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Weekly chart
        fig_weekly = go.Figure()
        
        fig_weekly.add_trace(go.Bar(
            x=weekly_forecast['week_num'],
            y=weekly_forecast['yhat']/1e6,
            name='Predicted Sales',
            marker_color='#4facfe',
            text=weekly_forecast['yhat'].apply(lambda x: f'IDR {x/1e6:.1f}M'),
            textposition='outside'
        ))
        
        fig_weekly.update_layout(
            title="Weekly Sales Forecast (26 Weeks)",
            xaxis_title="Week Number",
            yaxis_title="Sales (Million IDR)",
            height=400,
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Top 10 Weeks")
        
        # Show top 10 weeks
        top_weeks = weekly_forecast.nlargest(10, 'yhat')[['week_num', 'yhat']].copy()
        top_weeks['yhat'] = top_weeks['yhat'].apply(lambda x: f"IDR {x/1e6:.1f}M")
        top_weeks.columns = ['Week', 'Forecast']
        
        st.dataframe(
            top_weeks,
            hide_index=True,
            use_container_width=True,
            height=400
        )
    
    # Detailed Weekly Table
    st.markdown("---")
    st.markdown("## 📋 Detailed Weekly Forecast")
    
    # Format the weekly forecast for display
    display_df = weekly_forecast.copy()
    display_df['week'] = display_df['week'].astype(str)
    display_df['Predicted Sales'] = display_df['yhat'].apply(lambda x: f"IDR {x/1e6:.1f}M")
    display_df['Lower Bound'] = display_df['yhat_lower'].apply(lambda x: f"IDR {x/1e6:.1f}M")
    display_df['Upper Bound'] = display_df['yhat_upper'].apply(lambda x: f"IDR {x/1e6:.1f}M")
    display_df['Week #'] = display_df['week_num']
    
    st.dataframe(
        display_df[['Week #', 'week', 'Predicted Sales', 'Lower Bound', 'Upper Bound']],
        hide_index=True,
        use_container_width=True,
        height=400
    )
    
    # Model Performance
    st.markdown("---")
    st.markdown("## 🎯 Model Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mean Absolute Error", f"IDR {metrics['MAE']/1e6:.2f}M")
    
    with col2:
        st.metric("MAPE", f"{metrics['MAPE']:.2f}%")
    
    with col3:
        st.metric("RMSE", f"IDR {metrics['RMSE']/1e6:.2f}M")
    
    with col4:
        st.metric("R² Score", f"{metrics['R2']:.4f}")
    
    # Insights
    st.markdown("---")
    st.markdown("## 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📈 Growth Trend**
        - Starting: IDR {daily_forecast['yhat'].iloc[0]/1e6:.1f}M per day
        - Ending: IDR {daily_forecast['yhat'].iloc[-1]/1e6:.1f}M per day
        - Growth: {((daily_forecast['yhat'].iloc[-1]/daily_forecast['yhat'].iloc[0]) - 1)*100:.1f}%
        """)
    
    with col2:
        st.success(f"""
        **🎯 Reliability**
        - Model Accuracy: {metrics['Accuracy']:.1f}%
        - Status: {'✅ Good for planning' if metrics['Accuracy'] >= 70 else '⚠️ Use with caution'}
        - Recommendation: {'Suitable for tactical planning' if metrics['Accuracy'] >= 70 else 'Collect more data'}
        """)
    
    # Recommendations
    st.markdown("---")
    st.markdown("## 📝 Business Recommendations")
    
    st.markdown("""
    ### Based on the 6-month forecast:
    
    **Inventory Planning:**
    - 📦 Stock for average weekly sales of IDR {:.1f}M
    - 📊 Plan for ±44% variance (confidence interval)
    - 📈 Increase inventory in high-growth weeks
    
    **Marketing Strategy:**
    - 💰 Maintain current marketing spend ratio (8-10% of revenue)
    - 🎯 Focus campaigns on predicted high-sales weeks
    - 📊 Test new campaigns during stable periods
    
    **Financial Planning:**
    - 💵 Conservative estimate: IDR {:.1f}B
    - 🎯 Expected: IDR {:.2f}B
    - 🚀 Optimistic: IDR {:.1f}B
    
    **Next Steps:**
    - 🔄 Update forecast monthly with new data
    - 📊 Monitor actual vs predicted performance
    - 🎯 Adjust strategy based on variance
    """.format(
        avg_weekly/1e6,
        daily_forecast['yhat_lower'].sum()/1e9,
        total_forecast/1e9,
        daily_forecast['yhat_upper'].sum()/1e9
    ))
    
    # Download options
    st.markdown("---")
    st.markdown("## 📥 Export Forecast Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily forecast CSV
        csv_daily = daily_forecast.to_csv(index=False)
        st.download_button(
            label="📊 Download Daily Forecast (CSV)",
            data=csv_daily,
            file_name="nazava_daily_forecast_6months.csv",
            mime="text/csv"
        )
    
    with col2:
        # Weekly forecast CSV
        csv_weekly = weekly_forecast.to_csv(index=False)
        st.download_button(
            label="📅 Download Weekly Forecast (CSV)",
            data=csv_weekly,
            file_name="nazava_weekly_forecast_26weeks.csv",
            mime="text/csv"
        )

else:
    st.error("❌ Unable to load forecast data. Please ensure the ML model has been trained.")
    st.info("💡 Run the forecasting model first: `python ml/forecasting/final_sales_forecaster.py`")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.9rem;'>
    <p>🔮 Powered by Facebook Prophet ML | Updated: {}</p>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
