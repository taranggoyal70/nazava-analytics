"""
Improved Sales Forecasting Model using Prophet
Uses multiple data sources and 730 days of historical data
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import pickle
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class ImprovedSalesForecaster:
    """Sales forecasting using Facebook Prophet with multiple data sources"""
    
    def __init__(self, data_path=None):
        self.model = None
        self.data_path = data_path or "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
        self.forecast_df = None
        self.metrics = {}
        
    def load_data(self):
        """Load and combine sales data from multiple sources"""
        print("📊 Loading sales data from multiple sources...")
        
        # Load traffic data (730 days)
        traffic_df = pd.read_csv(f"{self.data_path}/traffic_overview_cleaned.csv")
        traffic_df['Date'] = pd.to_datetime(traffic_df['Date'], errors='coerce')
        traffic_df = traffic_df.dropna(subset=['Date'])
        
        # Load product data (30 days, most recent)
        product_df = pd.read_csv(f"{self.data_path}/product_overview_cleaned.csv")
        product_df['Date'] = pd.to_datetime(product_df['Date'], errors='coerce')
        product_df = product_df.dropna(subset=['Date'])
        
        print(f"   Traffic data: {len(traffic_df)} days ({traffic_df['Date'].min().date()} to {traffic_df['Date'].max().date()})")
        print(f"   Product data: {len(product_df)} days ({product_df['Date'].min().date()} to {product_df['Date'].max().date()})")
        
        # For traffic data, we need to estimate sales based on visitors and conversion
        # Use product data to calculate average revenue per visitor
        if len(product_df) > 0:
            # Convert to numeric, handling any non-numeric values
            sales_sum = pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
            visitors_sum = pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').sum()
            
            if visitors_sum > 0:
                avg_revenue_per_visitor = sales_sum / visitors_sum
                print(f"   Avg revenue per visitor: IDR {avg_revenue_per_visitor:,.0f}")
            else:
                avg_revenue_per_visitor = 10000
        else:
            avg_revenue_per_visitor = 10000  # Default estimate
        
        # Create estimated sales for traffic data
        traffic_sales = pd.DataFrame({
            'ds': traffic_df['Date'],
            'y': pd.to_numeric(traffic_df['Total_Visitors'], errors='coerce') * avg_revenue_per_visitor * 0.027  # Using 2.7% conversion rate
        })
        
        # Use actual sales from product data
        product_sales = pd.DataFrame({
            'ds': product_df['Date'],
            'y': product_df['Total Sales (Orders Created) (IDR)']
        })
        
        # Combine: use product data where available, traffic estimates elsewhere
        # Remove traffic data that overlaps with product data
        traffic_sales = traffic_sales[traffic_sales['ds'] < product_sales['ds'].min()]
        
        # Combine both datasets
        sales_data = pd.concat([traffic_sales, product_sales], ignore_index=True)
        sales_data = sales_data.sort_values('ds').reset_index(drop=True)
        
        # Remove any NaN or zero values
        sales_data = sales_data[sales_data['y'] > 0].dropna()
        
        print(f"\n✅ Combined dataset: {len(sales_data)} data points")
        print(f"📅 Date range: {sales_data['ds'].min().date()} to {sales_data['ds'].max().date()}")
        print(f"💰 Total sales: IDR {sales_data['y'].sum()/1e6:.1f}M")
        print(f"📊 Avg daily sales: IDR {sales_data['y'].mean()/1e6:.2f}M")
        
        return sales_data
    
    def add_regressors(self, df):
        """Add external regressors for better predictions"""
        # Add day of week (weekends might have different sales)
        df['day_of_week'] = df['ds'].dt.dayofweek
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        # Add month indicators for seasonality
        df['month'] = df['ds'].dt.month
        
        return df
    
    def train_model(self, df, test_size=0.15):
        """Train Prophet model with train-test split"""
        print("\n🤖 Training forecasting model...")
        
        # Add regressors
        df = self.add_regressors(df)
        
        # Split data
        split_idx = int(len(df) * (1 - test_size))
        train_df = df[:split_idx].copy()
        test_df = df[split_idx:].copy()
        
        print(f"📊 Train set: {len(train_df)} days")
        print(f"📊 Test set: {len(test_df)} days")
        
        # Initialize Prophet with optimized parameters for daily sales data
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            seasonality_mode='multiplicative',
            changepoint_prior_scale=0.05,
            seasonality_prior_scale=10,
            interval_width=0.95
        )
        
        # Add weekend regressor
        self.model.add_regressor('is_weekend')
        
        # Fit model
        print("⏳ Training in progress...")
        self.model.fit(train_df[['ds', 'y', 'is_weekend']])
        print("✅ Model trained successfully!")
        
        # Evaluate on test set
        test_forecast = self.model.predict(test_df[['ds', 'is_weekend']])
        self._evaluate_model(test_df, test_forecast)
        
        return train_df, test_df
    
    def _evaluate_model(self, actual_df, forecast_df):
        """Calculate model accuracy metrics"""
        actual = actual_df['y'].values
        predicted = forecast_df['yhat'].values
        
        # Calculate metrics
        mae = np.mean(np.abs(actual - predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        
        # R-squared
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        self.metrics = {
            'MAE': mae,
            'MAPE': mape,
            'RMSE': rmse,
            'R2': r2,
            'Accuracy': max(0, 100 - mape)
        }
        
        print("\n📊 Model Performance Metrics:")
        print(f"   MAE:      IDR {mae/1e6:.2f}M")
        print(f"   MAPE:     {mape:.2f}%")
        print(f"   RMSE:     IDR {rmse/1e6:.2f}M")
        print(f"   R²:       {r2:.4f}")
        print(f"   Accuracy: {max(0, 100-mape):.2f}%")
        
        if max(0, 100 - mape) >= 85:
            print("   ✅ Model meets 85% accuracy target!")
        elif max(0, 100 - mape) >= 70:
            print("   ⚠️  Model has good accuracy (70-85%)")
        else:
            print("   ⚠️  Model below target accuracy")
    
    def forecast_future(self, periods=26*7):
        """Generate forecast for future periods (default: 26 weeks = 182 days)"""
        print(f"\n🔮 Generating {periods//7}-week ({periods}-day) forecast...")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods, freq='D')
        
        # Add regressors for future dates
        future['day_of_week'] = future['ds'].dt.dayofweek
        future['is_weekend'] = (future['day_of_week'] >= 5).astype(int)
        
        # Generate forecast
        self.forecast_df = self.model.predict(future[['ds', 'is_weekend']])
        
        # Get only future predictions
        future_forecast = self.forecast_df.tail(periods)
        
        # Aggregate to weekly
        future_forecast['week'] = future_forecast['ds'].dt.to_period('W')
        weekly_forecast = future_forecast.groupby('week').agg({
            'yhat': 'sum',
            'yhat_lower': 'sum',
            'yhat_upper': 'sum'
        }).reset_index()
        
        print(f"✅ Forecast generated for next {periods//7} weeks")
        print(f"📅 Forecast period: {future_forecast['ds'].min().date()} to {future_forecast['ds'].max().date()}")
        print(f"💰 Predicted total sales (6 months): IDR {future_forecast['yhat'].sum()/1e6:.1f}M")
        print(f"📈 Avg weekly sales: IDR {weekly_forecast['yhat'].mean()/1e6:.1f}M")
        print(f"📊 Avg daily sales: IDR {future_forecast['yhat'].mean()/1e6:.2f}M")
        
        return future_forecast, weekly_forecast
    
    def get_forecast_summary(self):
        """Get summary statistics of forecast"""
        if self.forecast_df is None:
            return None
        
        future = self.forecast_df.tail(182)  # Next 6 months (26 weeks)
        
        summary = {
            'total_predicted_sales': future['yhat'].sum(),
            'avg_daily_sales': future['yhat'].mean(),
            'min_daily_sales': future['yhat'].min(),
            'max_daily_sales': future['yhat'].max(),
            'confidence_lower': future['yhat_lower'].sum(),
            'confidence_upper': future['yhat_upper'].sum(),
            'forecast_dates': (future['ds'].min(), future['ds'].max()),
            'metrics': self.metrics
        }
        
        return summary
    
    def save_forecast_csv(self, filepath='forecasts/sales_forecast_6months.csv'):
        """Save forecast to CSV"""
        if self.forecast_df is None:
            print("❌ No forecast available")
            return
        
        future = self.forecast_df.tail(182)
        future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(filepath, index=False)
        print(f"💾 Forecast saved to {filepath}")


def main():
    """Main execution"""
    print("="*70)
    print("🔮 NAZAVA IMPROVED SALES FORECASTING MODEL")
    print("="*70)
    
    # Initialize forecaster
    forecaster = ImprovedSalesForecaster()
    
    # Load data
    sales_data = forecaster.load_data()
    
    # Train model with validation
    train_df, test_df = forecaster.train_model(sales_data, test_size=0.15)
    
    # Generate 6-month forecast (26 weeks = 182 days)
    daily_forecast, weekly_forecast = forecaster.forecast_future(periods=182)
    
    # Get summary
    summary = forecaster.get_forecast_summary()
    
    print("\n" + "="*70)
    print("📊 6-MONTH FORECAST SUMMARY")
    print("="*70)
    print(f"Total Predicted Sales:     IDR {summary['total_predicted_sales']/1e6:.1f}M")
    print(f"Average Daily Sales:       IDR {summary['avg_daily_sales']/1e6:.2f}M")
    print(f"Average Weekly Sales:      IDR {summary['avg_daily_sales']*7/1e6:.1f}M")
    print(f"\nConfidence Interval (95%):")
    print(f"  Lower Bound: IDR {summary['confidence_lower']/1e6:.1f}M")
    print(f"  Upper Bound: IDR {summary['confidence_upper']/1e6:.1f}M")
    print(f"\nForecast Period: {summary['forecast_dates'][0].date()} to {summary['forecast_dates'][1].date()}")
    
    print("\n" + "="*70)
    print("📈 MODEL RELIABILITY")
    print("="*70)
    print(f"Accuracy:  {summary['metrics']['Accuracy']:.2f}%")
    print(f"R² Score:  {summary['metrics']['R2']:.4f}")
    print(f"MAPE:      {summary['metrics']['MAPE']:.2f}%")
    
    if summary['metrics']['Accuracy'] >= 85:
        print("\n✅ Model is RELIABLE for business planning (≥85% accuracy)")
    elif summary['metrics']['Accuracy'] >= 70:
        print("\n⚠️  Model has GOOD accuracy (70-85%) - use with caution")
    else:
        print("\n⚠️  Model needs improvement - consider as rough estimate only")
    
    print("\n✅ Forecasting complete!")
    
    return forecaster, daily_forecast, weekly_forecast


if __name__ == "__main__":
    forecaster, daily_forecast, weekly_forecast = main()
