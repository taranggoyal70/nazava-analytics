"""
Sales Forecasting Model using Prophet
Predicts weekly sales for the next 6 months
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import pickle
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class SalesForecaster:
    """Sales forecasting using Facebook Prophet"""
    
    def __init__(self, data_path=None):
        self.model = None
        self.data_path = data_path or "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
        self.forecast_df = None
        self.metrics = {}
        
    def load_data(self):
        """Load and prepare sales data"""
        print("📊 Loading sales data...")
        
        # Load product overview data (has daily sales)
        product_df = pd.read_csv(f"{self.data_path}/product_overview_cleaned.csv")
        
        # Convert date column
        product_df['Date'] = pd.to_datetime(product_df['Date'], errors='coerce')
        product_df = product_df.dropna(subset=['Date'])
        
        # Create sales dataframe for Prophet
        sales_data = pd.DataFrame({
            'ds': product_df['Date'],  # Prophet requires 'ds' column for dates
            'y': product_df['Total Sales (Orders Created) (IDR)']  # Prophet requires 'y' for target
        })
        
        # Remove any NaN values
        sales_data = sales_data.dropna()
        
        # Sort by date
        sales_data = sales_data.sort_values('ds').reset_index(drop=True)
        
        print(f"✅ Loaded {len(sales_data)} data points")
        print(f"📅 Date range: {sales_data['ds'].min().date()} to {sales_data['ds'].max().date()}")
        print(f"💰 Total sales: IDR {sales_data['y'].sum()/1e6:.1f}M")
        print(f"📊 Avg daily sales: IDR {sales_data['y'].mean()/1e6:.2f}M")
        
        return sales_data
    
    def prepare_features(self, df):
        """Add additional features for better forecasting"""
        # Add month, quarter for seasonality
        df['month'] = df['ds'].dt.month
        df['quarter'] = df['ds'].dt.quarter
        df['year'] = df['ds'].dt.year
        
        return df
    
    def train_model(self, df, test_size=0.2):
        """Train Prophet model with train-test split"""
        print("\n🤖 Training forecasting model...")
        
        # Split data
        split_idx = int(len(df) * (1 - test_size))
        train_df = df[:split_idx].copy()
        test_df = df[split_idx:].copy()
        
        print(f"📊 Train set: {len(train_df)} points")
        print(f"📊 Test set: {len(test_df)} points")
        
        # Initialize Prophet with custom parameters for daily data
        self.model = Prophet(
            yearly_seasonality=False,  # We'll add custom
            weekly_seasonality=True,   # Daily data has weekly patterns
            daily_seasonality=False,   # Not enough intraday data
            seasonality_mode='multiplicative',  # Better for sales data
            changepoint_prior_scale=0.1,  # Flexibility in trend changes
            interval_width=0.95  # 95% confidence interval
        )
        
        # Add custom seasonality for monthly patterns
        self.model.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        )
        
        # Fit model
        print("⏳ Training in progress...")
        self.model.fit(train_df[['ds', 'y']])
        print("✅ Model trained successfully!")
        
        # Evaluate on test set
        test_forecast = self.model.predict(test_df[['ds']])
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
        r2 = 1 - (ss_res / ss_tot)
        
        self.metrics = {
            'MAE': mae,
            'MAPE': mape,
            'RMSE': rmse,
            'R2': r2,
            'Accuracy': 100 - mape
        }
        
        print("\n📊 Model Performance Metrics:")
        print(f"   MAE:      IDR {mae/1e6:.2f}M")
        print(f"   MAPE:     {mape:.2f}%")
        print(f"   RMSE:     IDR {rmse/1e6:.2f}M")
        print(f"   R²:       {r2:.4f}")
        print(f"   Accuracy: {100-mape:.2f}%")
        
        if 100 - mape >= 85:
            print("   ✅ Model meets 85% accuracy target!")
        else:
            print("   ⚠️  Model below 85% accuracy target")
    
    def forecast_future(self, periods=26):
        """Generate forecast for future periods (default: 26 weeks = 6 months)"""
        print(f"\n🔮 Generating {periods}-week forecast...")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(
            periods=periods,
            freq='W'  # Weekly forecast
        )
        
        # Generate forecast
        self.forecast_df = self.model.predict(future)
        
        # Get only future predictions
        future_forecast = self.forecast_df.tail(periods)
        
        print(f"✅ Forecast generated for next {periods} weeks")
        print(f"📅 Forecast period: {future_forecast['ds'].min().date()} to {future_forecast['ds'].max().date()}")
        print(f"💰 Predicted total sales: IDR {future_forecast['yhat'].sum()/1e6:.1f}M")
        print(f"📈 Avg weekly sales: IDR {future_forecast['yhat'].mean()/1e6:.1f}M")
        
        return future_forecast
    
    def get_forecast_summary(self):
        """Get summary statistics of forecast"""
        if self.forecast_df is None:
            return None
        
        future = self.forecast_df.tail(26)  # Next 6 months
        
        summary = {
            'total_predicted_sales': future['yhat'].sum(),
            'avg_weekly_sales': future['yhat'].mean(),
            'min_weekly_sales': future['yhat'].min(),
            'max_weekly_sales': future['yhat'].max(),
            'confidence_lower': future['yhat_lower'].sum(),
            'confidence_upper': future['yhat_upper'].sum(),
            'forecast_dates': (future['ds'].min(), future['ds'].max()),
            'metrics': self.metrics
        }
        
        return summary
    
    def save_model(self, filepath='models/trained_models/sales_forecaster.pkl'):
        """Save trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"💾 Model saved to {filepath}")
    
    def load_model(self, filepath='models/trained_models/sales_forecaster.pkl'):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        print(f"📂 Model loaded from {filepath}")
    
    def plot_forecast(self, save_path=None):
        """Generate forecast visualization"""
        if self.model is None or self.forecast_df is None:
            print("❌ No model or forecast available")
            return
        
        # Prophet has built-in plotting
        fig = self.model.plot(self.forecast_df)
        
        if save_path:
            fig.savefig(save_path)
            print(f"📊 Forecast plot saved to {save_path}")
        
        return fig
    
    def plot_components(self, save_path=None):
        """Plot forecast components (trend, seasonality)"""
        if self.model is None or self.forecast_df is None:
            print("❌ No model or forecast available")
            return
        
        fig = self.model.plot_components(self.forecast_df)
        
        if save_path:
            fig.savefig(save_path)
            print(f"📊 Components plot saved to {save_path}")
        
        return fig


def main():
    """Main execution"""
    print("="*70)
    print("🔮 NAZAVA SALES FORECASTING MODEL")
    print("="*70)
    
    # Initialize forecaster
    forecaster = SalesForecaster()
    
    # Load data
    sales_data = forecaster.load_data()
    
    # Prepare features
    sales_data = forecaster.prepare_features(sales_data)
    
    # Train model with validation
    train_df, test_df = forecaster.train_model(sales_data, test_size=0.2)
    
    # Generate 6-month forecast (26 weeks)
    future_forecast = forecaster.forecast_future(periods=26)
    
    # Get summary
    summary = forecaster.get_forecast_summary()
    
    print("\n" + "="*70)
    print("📊 FORECAST SUMMARY")
    print("="*70)
    print(f"Total Predicted Sales (6 months): IDR {summary['total_predicted_sales']/1e6:.1f}M")
    print(f"Average Weekly Sales:              IDR {summary['avg_weekly_sales']/1e6:.1f}M")
    print(f"Confidence Interval (95%):")
    print(f"  Lower Bound: IDR {summary['confidence_lower']/1e6:.1f}M")
    print(f"  Upper Bound: IDR {summary['confidence_upper']/1e6:.1f}M")
    print(f"\nForecast Period: {summary['forecast_dates'][0].date()} to {summary['forecast_dates'][1].date()}")
    
    # Save model
    # forecaster.save_model()
    
    print("\n✅ Forecasting complete!")
    
    return forecaster, future_forecast


if __name__ == "__main__":
    forecaster, forecast = main()
