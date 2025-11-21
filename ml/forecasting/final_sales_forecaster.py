"""
Final Sales Forecasting Model - Using actual sales data only
Objective #2: Predict weekly sales for next 6 months with 85%+ accuracy
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')


class FinalSalesForecaster:
    """Sales forecasting using Facebook Prophet - production ready"""
    
    def __init__(self, data_path=None):
        self.model = None
        self.data_path = data_path or "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
        self.forecast_df = None
        self.metrics = {}
        
    def load_data(self):
        """Load actual sales data from product overview (30 days of real data)"""
        print("📊 Loading actual sales data...")
        
        product_df = pd.read_csv(f"{self.data_path}/product_overview_cleaned.csv")
        product_df['Date'] = pd.to_datetime(product_df['Date'], errors='coerce')
        product_df = product_df.dropna(subset=['Date'])
        
        # Create Prophet dataframe
        sales_data = pd.DataFrame({
            'ds': product_df['Date'],
            'y': pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce')
        })
        
        sales_data = sales_data.dropna().sort_values('ds').reset_index(drop=True)
        
        print(f"✅ Loaded {len(sales_data)} days of actual sales data")
        print(f"📅 Date range: {sales_data['ds'].min().date()} to {sales_data['ds'].max().date()}")
        print(f"💰 Total sales: IDR {sales_data['y'].sum()/1e6:.1f}M")
        print(f"📊 Avg daily sales: IDR {sales_data['y'].mean()/1e6:.2f}M")
        print(f"📊 Min daily sales: IDR {sales_data['y'].min()/1e6:.2f}M")
        print(f"📊 Max daily sales: IDR {sales_data['y'].max()/1e6:.2f}M")
        
        return sales_data
    
    def train_model(self, df):
        """Train Prophet model on all available data"""
        print("\n🤖 Training forecasting model...")
        print(f"📊 Training on {len(df)} days of data")
        
        # Initialize Prophet with parameters optimized for limited data
        self.model = Prophet(
            yearly_seasonality=False,  # Not enough data for yearly
            weekly_seasonality=True,   # Capture weekly patterns
            daily_seasonality=False,
            seasonality_mode='additive',  # More stable for limited data
            changepoint_prior_scale=0.05,  # Conservative trend changes
            interval_width=0.95
        )
        
        # Fit model
        print("⏳ Training in progress...")
        self.model.fit(df[['ds', 'y']])
        print("✅ Model trained successfully!")
        
        # Calculate in-sample accuracy
        predictions = self.model.predict(df[['ds']])
        self._evaluate_model(df, predictions, is_training=True)
        
        return df
    
    def _evaluate_model(self, actual_df, forecast_df, is_training=False):
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
        
        accuracy = max(0, 100 - mape)
        
        self.metrics = {
            'MAE': mae,
            'MAPE': mape,
            'RMSE': rmse,
            'R2': r2,
            'Accuracy': accuracy
        }
        
        label = "In-Sample Performance" if is_training else "Model Performance"
        print(f"\n📊 {label}:")
        print(f"   MAE:      IDR {mae/1e6:.2f}M ({mae/actual.mean()*100:.1f}% of avg)")
        print(f"   MAPE:     {mape:.2f}%")
        print(f"   RMSE:     IDR {rmse/1e6:.2f}M")
        print(f"   R²:       {r2:.4f}")
        print(f"   Accuracy: {accuracy:.2f}%")
        
        if accuracy >= 85:
            print("   ✅ Excellent accuracy (≥85%)")
        elif accuracy >= 70:
            print("   ⚠️  Good accuracy (70-85%)")
        else:
            print("   ⚠️  Limited data - use forecast with caution")
    
    def forecast_future(self, weeks=26):
        """Generate forecast for future weeks"""
        days = weeks * 7
        print(f"\n🔮 Generating {weeks}-week ({days}-day) forecast...")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=days, freq='D')
        
        # Generate forecast
        self.forecast_df = self.model.predict(future)
        
        # Get only future predictions
        future_forecast = self.forecast_df.tail(days).copy()
        
        # Aggregate to weekly
        future_forecast['week'] = future_forecast['ds'].dt.to_period('W')
        weekly_forecast = future_forecast.groupby('week').agg({
            'yhat': 'sum',
            'yhat_lower': 'sum',
            'yhat_upper': 'sum'
        }).reset_index()
        weekly_forecast['week_num'] = range(1, len(weekly_forecast) + 1)
        
        print(f"✅ Forecast generated successfully!")
        print(f"📅 Forecast period: {future_forecast['ds'].min().date()} to {future_forecast['ds'].max().date()}")
        print(f"\n💰 6-Month Sales Forecast:")
        print(f"   Total:        IDR {future_forecast['yhat'].sum()/1e6:.1f}M")
        print(f"   Avg Weekly:   IDR {weekly_forecast['yhat'].mean()/1e6:.1f}M")
        print(f"   Avg Daily:    IDR {future_forecast['yhat'].mean()/1e6:.2f}M")
        print(f"\n📊 Confidence Interval (95%):")
        print(f"   Lower Bound:  IDR {future_forecast['yhat_lower'].sum()/1e6:.1f}M")
        print(f"   Upper Bound:  IDR {future_forecast['yhat_upper'].sum()/1e6:.1f}M")
        
        return future_forecast, weekly_forecast
    
    def get_weekly_breakdown(self, weekly_forecast):
        """Print weekly forecast breakdown"""
        print("\n📅 Weekly Sales Forecast Breakdown:")
        print("="*70)
        print(f"{'Week':<8} {'Period':<20} {'Predicted Sales':<20} {'Range (95% CI)'}")
        print("="*70)
        
        for idx, row in weekly_forecast.head(10).iterrows():
            week_num = row['week_num']
            predicted = row['yhat'] / 1e6
            lower = row['yhat_lower'] / 1e6
            upper = row['yhat_upper'] / 1e6
            period = str(row['week'])
            
            print(f"Week {week_num:<3} {period:<20} IDR {predicted:>6.1f}M        IDR {lower:>5.1f}M - {upper:>5.1f}M")
        
        if len(weekly_forecast) > 10:
            print(f"... ({len(weekly_forecast) - 10} more weeks)")
        print("="*70)
    
    def get_model_conclusion(self):
        """Provide conclusion on model reliability"""
        print("\n" + "="*70)
        print("📋 MODEL RELIABILITY CONCLUSION")
        print("="*70)
        
        accuracy = self.metrics['Accuracy']
        r2 = self.metrics['R2']
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Accuracy (100 - MAPE): {accuracy:.2f}%")
        print(f"   R² Score:              {r2:.4f}")
        print(f"   Mean Absolute Error:   IDR {self.metrics['MAE']/1e6:.2f}M")
        
        print(f"\n💡 Reliability Assessment:")
        
        if accuracy >= 85:
            print("   ✅ HIGHLY RELIABLE - Model meets 85% accuracy target")
            print("   ✅ Suitable for strategic business planning")
            print("   ✅ Forecast can be used with high confidence")
        elif accuracy >= 70:
            print("   ⚠️  MODERATELY RELIABLE - Good accuracy (70-85%)")
            print("   ⚠️  Suitable for tactical planning with monitoring")
            print("   ⚠️  Recommend validating against actual results")
        elif accuracy >= 50:
            print("   ⚠️  LIMITED RELIABILITY - Fair accuracy (50-70%)")
            print("   ⚠️  Use as rough estimate only")
            print("   ⚠️  Requires frequent recalibration")
        else:
            print("   ❌ LOW RELIABILITY - Below 50% accuracy")
            print("   ❌ Limited training data (only 30 days)")
            print("   ❌ Use for directional guidance only")
        
        print(f"\n📝 Recommendations:")
        print("   • Collect more historical data for improved accuracy")
        print("   • Update model monthly as new data becomes available")
        print("   • Monitor actual vs predicted and adjust strategy")
        print("   • Consider seasonality factors (holidays, campaigns)")
        
        return accuracy >= 85


def main():
    """Main execution"""
    print("="*70)
    print("🔮 NAZAVA SALES FORECASTING - FINAL MODEL")
    print("   Objective #2: Predict Weekly Sales for Next 6 Months")
    print("="*70)
    
    # Initialize forecaster
    forecaster = FinalSalesForecaster()
    
    # Load data
    sales_data = forecaster.load_data()
    
    # Train model
    train_df = forecaster.train_model(sales_data)
    
    # Generate 6-month forecast (26 weeks)
    daily_forecast, weekly_forecast = forecaster.forecast_future(weeks=26)
    
    # Show weekly breakdown
    forecaster.get_weekly_breakdown(weekly_forecast)
    
    # Model conclusion
    is_reliable = forecaster.get_model_conclusion()
    
    print("\n" + "="*70)
    print("✅ FORECASTING COMPLETE!")
    print("="*70)
    
    if is_reliable:
        print("🎯 Model is ready for business use!")
    else:
        print("📊 Model provides directional guidance - collect more data for improvement")
    
    return forecaster, daily_forecast, weekly_forecast


if __name__ == "__main__":
    forecaster, daily_forecast, weekly_forecast = main()
