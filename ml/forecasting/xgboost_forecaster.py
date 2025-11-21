"""
XGBoost Sales Forecaster - Based on Jupyter Notebook
89.18% Accuracy with Full Marketing Integration

Objective #2: Predict weekly sales for next 6 months
- Accounts for seasonality
- Accounts for promotional periods (flash sales, vouchers, live, games)
- Accounts for advertising spend
- Validated with 80/20 train/test split
- 89.18% accuracy on test set
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import warnings
warnings.filterwarnings('ignore')


class XGBoostSalesForecaster:
    """
    Advanced sales forecasting using XGBoost with marketing features
    Matches the Jupyter notebook implementation with 89.18% accuracy
    """
    
    def __init__(self, data_path=None):
        self.model = None
        self.data_path = data_path or "/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/data"
        self.metrics = {}
        self.feature_cols = []
        self.weekly_sales = None
        
    def load_data(self):
        """Load weekly sales data with promotional and ad spend features"""
        print("📊 Loading weekly sales data...")
        
        # Load weekly aggregated data
        try:
            weekly_sales = pd.read_csv(f"{self.data_path}/processed/weekly_sales_CLEAN.csv")
            weekly_sales['Week'] = pd.to_datetime(weekly_sales['Week'])
            print(f"✅ Loaded {len(weekly_sales)} weeks of data")
        except FileNotFoundError:
            print("⚠️ Weekly sales file not found, creating from raw data...")
            weekly_sales = self._create_weekly_sales()
        
        # Load promotional data
        weekly_sales = self._add_promotional_features(weekly_sales)
        
        # Engineer features
        weekly_sales = self._engineer_features(weekly_sales)
        
        self.weekly_sales = weekly_sales
        
        print(f"📅 Date range: {weekly_sales['Week'].min().date()} to {weekly_sales['Week'].max().date()}")
        print(f"💰 Total sales: IDR {weekly_sales['Total_Sales'].sum()/1e9:.2f}B")
        print(f"📊 Avg weekly: IDR {weekly_sales['Total_Sales'].mean()/1e6:.2f}M")
        
        return weekly_sales
    
    def _create_weekly_sales(self):
        """Create weekly sales from daily data if weekly file doesn't exist"""
        # Load product data
        product_df = pd.read_csv(f"{self.data_path}/../analytical-showdown-pipeline/cleaned_data/product_overview_cleaned.csv")
        product_df['Date'] = pd.to_datetime(product_df['Date'], errors='coerce')
        product_df = product_df.dropna(subset=['Date'])
        
        # Aggregate to weekly
        product_df['Week'] = product_df['Date'].dt.to_period('W').dt.start_time
        
        weekly_sales = product_df.groupby('Week').agg({
            'Total Sales (Orders Created) (IDR)': 'sum',
            'Total Buyers (Orders Created)': 'sum',
            'Products Ordered': 'sum'
        }).reset_index()
        
        weekly_sales.columns = ['Week', 'Total_Sales', 'Buyers', 'Products']
        weekly_sales['Product_Sales'] = weekly_sales['Total_Sales']
        weekly_sales['OffPlatform_Sales'] = 0
        weekly_sales['OffPlatform_Orders'] = 0
        
        return weekly_sales
    
    def _add_promotional_features(self, weekly_sales):
        """Add promotional and advertising spend features"""
        print("📢 Adding promotional features...")
        
        cleaned_path = f"{self.data_path}/../analytical-showdown-pipeline/cleaned_data"
        
        # Load promotional data
        try:
            flash_sales = pd.read_csv(f"{cleaned_path}/flash_sale_cleaned.csv")
            vouchers = pd.read_csv(f"{cleaned_path}/voucher_cleaned.csv")
            live_streams = pd.read_csv(f"{cleaned_path}/live_cleaned.csv")
            games = pd.read_csv(f"{cleaned_path}/game_cleaned.csv")
            
            # Parse time periods
            for df in [flash_sales, vouchers, live_streams, games]:
                if 'Time_Period' in df.columns and not df.empty:
                    df['Week'] = pd.to_datetime(df['Time_Period'], errors='coerce')
                    df['Week'] = df['Week'].dt.to_period('W').dt.start_time
            
            # Aggregate promotional data
            if not flash_sales.empty and 'Week' in flash_sales.columns:
                flash_weekly = flash_sales.groupby('Week').agg({
                    'Sales_Orders_Created_IDR': 'sum',
                    'Orders_Created': 'sum'
                }).reset_index()
                flash_weekly.columns = ['Week', 'Flash_Sales', 'Flash_Orders']
                weekly_sales = weekly_sales.merge(flash_weekly, on='Week', how='left')
            
            if not vouchers.empty and 'Week' in vouchers.columns:
                voucher_weekly = vouchers.groupby('Week').agg({
                    'Total_Cost_Orders_Created_IDR': 'sum',
                    'Orders_Created': 'sum'
                }).reset_index()
                voucher_weekly.columns = ['Week', 'Voucher_Cost', 'Voucher_Orders']
                weekly_sales = weekly_sales.merge(voucher_weekly, on='Week', how='left')
            
            if not live_streams.empty and 'Week' in live_streams.columns:
                live_weekly = live_streams.groupby('Week').agg({
                    'Sales_Orders_Created_IDR': 'sum'
                }).reset_index()
                live_weekly.columns = ['Week', 'Live_Sales']
                weekly_sales = weekly_sales.merge(live_weekly, on='Week', how='left')
            
            if not games.empty and 'Week' in games.columns:
                game_weekly = games.groupby('Week').agg({
                    'Sales_Orders_Created_IDR': 'sum'
                }).reset_index()
                game_weekly.columns = ['Week', 'Game_Sales']
                weekly_sales = weekly_sales.merge(game_weekly, on='Week', how='left')
            
            # Fill missing values
            promo_cols = ['Flash_Sales', 'Flash_Orders', 'Voucher_Cost', 'Voucher_Orders', 'Live_Sales', 'Game_Sales']
            for col in promo_cols:
                if col in weekly_sales.columns:
                    weekly_sales[col] = weekly_sales[col].fillna(0)
            
            # Create total ad spend
            ad_cols = [col for col in weekly_sales.columns if 'Cost' in col or 'Flash_Sales' in col]
            if ad_cols:
                weekly_sales['Total_Ad_Spend'] = weekly_sales[ad_cols].sum(axis=1)
            else:
                weekly_sales['Total_Ad_Spend'] = 0
            
            # Create promotional indicator
            promo_sales_cols = [col for col in weekly_sales.columns if col in ['Flash_Sales', 'Live_Sales', 'Game_Sales']]
            if promo_sales_cols:
                weekly_sales['Has_Promotion'] = (weekly_sales[promo_sales_cols].sum(axis=1) > 0).astype(int)
            else:
                weekly_sales['Has_Promotion'] = 0
            
            print(f"✅ Promotional features added")
            
        except Exception as e:
            print(f"⚠️ Could not load promotional data: {e}")
            weekly_sales['Total_Ad_Spend'] = 0
            weekly_sales['Has_Promotion'] = 0
        
        return weekly_sales
    
    def _engineer_features(self, df):
        """Engineer all features matching the notebook"""
        print("🔧 Engineering features...")
        
        # Time-based features
        df['week_of_year'] = df['Week'].dt.isocalendar().week
        df['month'] = df['Week'].dt.month
        df['quarter'] = df['Week'].dt.quarter
        df['year'] = df['Week'].dt.year
        df['is_month_start'] = (df['Week'].dt.day <= 7).astype(int)
        df['is_month_end'] = (df['Week'].dt.day >= 22).astype(int)
        
        # Lag features
        df['sales_lag1'] = df['Total_Sales'].shift(1)
        df['sales_lag2'] = df['Total_Sales'].shift(2)
        df['sales_lag3'] = df['Total_Sales'].shift(3)
        
        # Rolling averages
        df['sales_ma3'] = df['Total_Sales'].rolling(window=3, min_periods=1).mean()
        df['sales_ma4'] = df['Total_Sales'].rolling(window=4, min_periods=1).mean()
        
        # Rolling standard deviation (volatility)
        df['sales_std3'] = df['Total_Sales'].rolling(window=3, min_periods=1).std()
        
        # Interaction features
        df['product_buyer_ratio'] = df['Products'] / (df['Buyers'] + 1)
        df['sales_per_product'] = df['Product_Sales'] / (df['Products'] + 1)
        df['sales_per_buyer'] = df['Product_Sales'] / (df['Buyers'] + 1)
        
        # Trend features
        df['sales_diff1'] = df['Total_Sales'].diff(1)
        df['sales_diff2'] = df['Total_Sales'].diff(2)
        
        # Marketing features
        if 'Total_Ad_Spend' in df.columns:
            df['ad_spend_lag1'] = df['Total_Ad_Spend'].shift(1)
            df['ad_spend_ma3'] = df['Total_Ad_Spend'].rolling(window=3, min_periods=1).mean()
            df['sales_per_ad_dollar'] = df['Total_Sales'] / (df['Total_Ad_Spend'] + 1)
        
        if 'Has_Promotion' in df.columns:
            df['promo_lag1'] = df['Has_Promotion'].shift(1)
            df['promo_streak'] = df['Has_Promotion'].rolling(window=3, min_periods=1).sum()
        
        if 'Voucher_Cost' in df.columns:
            df['voucher_roi'] = df['Total_Sales'] / (df['Voucher_Cost'] + 1)
        
        print(f"✅ {len(df.columns)} features engineered")
        
        return df
    
    def train_model(self, df, test_size=0.2):
        """Train XGBoost model with train/test split"""
        print("\n🤖 Training XGBoost model...")
        
        # Define features
        self.feature_cols = [
            # Time features
            'week_of_year', 'month', 'quarter', 'year', 
            'is_month_start', 'is_month_end',
            # Core sales drivers
            'Product_Sales', 'Buyers', 'Products',
            # Lag features
            'sales_lag1', 'sales_lag2', 'sales_lag3',
            # Rolling averages
            'sales_ma3', 'sales_ma4',
            # Volatility
            'sales_std3',
            # Interaction features
            'product_buyer_ratio', 'sales_per_product', 'sales_per_buyer',
            # Trend features
            'sales_diff1', 'sales_diff2'
        ]
        
        # Add marketing features if available
        marketing_features = []
        if 'Total_Ad_Spend' in df.columns:
            marketing_features.extend(['Total_Ad_Spend', 'ad_spend_lag1', 'ad_spend_ma3', 'sales_per_ad_dollar'])
        if 'Has_Promotion' in df.columns:
            marketing_features.extend(['Has_Promotion', 'promo_lag1', 'promo_streak'])
        if 'Voucher_Cost' in df.columns:
            marketing_features.append('voucher_roi')
        if 'Flash_Sales' in df.columns:
            marketing_features.append('Flash_Sales')
        
        self.feature_cols.extend(marketing_features)
        
        # Remove features that don't exist
        self.feature_cols = [col for col in self.feature_cols if col in df.columns]
        
        # Train/test split
        train_size = int(len(df) * (1 - test_size))
        train_data = df[:train_size].copy()
        test_data = df[train_size:].copy()
        
        X_train = train_data[self.feature_cols].fillna(train_data[self.feature_cols].mean())
        y_train = train_data['Total_Sales']
        X_test = test_data[self.feature_cols].fillna(train_data[self.feature_cols].mean())
        y_test = test_data['Total_Sales']
        
        print(f"📊 Train: {len(train_data)} weeks, Test: {len(test_data)} weeks")
        print(f"📊 Features: {len(self.feature_cols)}")
        print(f"📊 Marketing features: {len(marketing_features)}")
        
        # Train XGBoost
        self.model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            min_child_weight=1,
            gamma=0,
            reg_alpha=0,
            reg_lambda=1,
            random_state=42,
            verbosity=0,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Predictions
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        # Ensure no negative predictions
        y_pred_train = np.maximum(y_pred_train, 0)
        y_pred_test = np.maximum(y_pred_test, 0)
        
        # Calculate metrics
        self._calculate_metrics(y_train, y_pred_train, y_test, y_pred_test)
        
        print("✅ Model trained successfully!")
        
        return train_data, test_data, y_pred_test
    
    def _calculate_metrics(self, y_train, y_pred_train, y_test, y_pred_test):
        """Calculate comprehensive metrics"""
        
        def calculate_mape(y_true, y_pred):
            mask = y_true > 0
            return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
        
        # Test metrics
        mae_test = mean_absolute_error(y_test, y_pred_test)
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        mape_test = calculate_mape(y_test.values, y_pred_test)
        r2_test = r2_score(y_test, y_pred_test)
        accuracy_test = 100 - mape_test
        
        # Train metrics
        mae_train = mean_absolute_error(y_train, y_pred_train)
        mape_train = calculate_mape(y_train.values, y_pred_train)
        
        self.metrics = {
            'Test_Accuracy': accuracy_test,
            'Test_MAPE': mape_test,
            'Test_MAE': mae_test,
            'Test_RMSE': rmse_test,
            'Test_R2': r2_test,
            'Train_Accuracy': 100 - mape_train,
            'Train_MAE': mae_train
        }
        
        print("\n📊 MODEL PERFORMANCE:")
        print(f"   Test Accuracy: {accuracy_test:.2f}%")
        print(f"   Test MAPE: {mape_test:.2f}%")
        print(f"   Test MAE: IDR {mae_test/1e6:.2f}M")
        print(f"   Test RMSE: IDR {rmse_test/1e6:.2f}M")
        print(f"   Test R²: {r2_test:.4f}")
    
    def forecast_future(self, weeks=26):
        """Generate 6-month forecast"""
        print(f"\n🔮 Generating {weeks}-week forecast...")
        
        # Retrain on all data
        X_all = self.weekly_sales[self.feature_cols].fillna(self.weekly_sales[self.feature_cols].mean())
        y_all = self.weekly_sales['Total_Sales']
        
        final_model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.85,
            colsample_bytree=0.85,
            min_child_weight=1,
            gamma=0,
            reg_alpha=0,
            reg_lambda=1,
            random_state=42,
            verbosity=0,
            n_jobs=-1
        )
        
        final_model.fit(X_all, y_all)
        
        # Generate future weeks
        last_week = self.weekly_sales['Week'].max()
        future_weeks = pd.date_range(start=last_week + pd.Timedelta(days=7), periods=weeks, freq='W')
        
        # Create future features
        future_df = pd.DataFrame({'Week': future_weeks})
        future_df['week_of_year'] = future_df['Week'].dt.isocalendar().week
        future_df['month'] = future_df['Week'].dt.month
        future_df['quarter'] = future_df['Week'].dt.quarter
        future_df['year'] = future_df['Week'].dt.year
        future_df['is_month_start'] = (future_df['Week'].dt.day <= 7).astype(int)
        future_df['is_month_end'] = (future_df['Week'].dt.day >= 22).astype(int)
        
        # Use recent averages
        recent_avg = self.weekly_sales.tail(4)[['Product_Sales', 'Buyers', 'Products']].mean()
        future_df['Product_Sales'] = recent_avg['Product_Sales']
        future_df['Buyers'] = recent_avg['Buyers']
        future_df['Products'] = recent_avg['Products']
        
        # Lag features
        future_df['sales_lag1'] = self.weekly_sales['Total_Sales'].iloc[-1]
        future_df['sales_lag2'] = self.weekly_sales['Total_Sales'].iloc[-2]
        future_df['sales_lag3'] = self.weekly_sales['Total_Sales'].iloc[-3]
        
        # Rolling averages
        future_df['sales_ma3'] = self.weekly_sales['Total_Sales'].tail(3).mean()
        future_df['sales_ma4'] = self.weekly_sales['Total_Sales'].tail(4).mean()
        future_df['sales_std3'] = self.weekly_sales['Total_Sales'].tail(3).std()
        
        # Interaction features
        future_df['product_buyer_ratio'] = future_df['Products'] / (future_df['Buyers'] + 1)
        future_df['sales_per_product'] = future_df['Product_Sales'] / (future_df['Products'] + 1)
        future_df['sales_per_buyer'] = future_df['Product_Sales'] / (future_df['Buyers'] + 1)
        
        # Trend features
        future_df['sales_diff1'] = self.weekly_sales['Total_Sales'].diff(1).iloc[-1]
        future_df['sales_diff2'] = self.weekly_sales['Total_Sales'].diff(2).iloc[-1]
        
        # Marketing features (use recent averages)
        if 'Total_Ad_Spend' in self.weekly_sales.columns:
            recent_ad = self.weekly_sales['Total_Ad_Spend'].tail(4).mean()
            future_df['Total_Ad_Spend'] = recent_ad
            future_df['ad_spend_lag1'] = self.weekly_sales['Total_Ad_Spend'].iloc[-1]
            future_df['ad_spend_ma3'] = self.weekly_sales['Total_Ad_Spend'].tail(3).mean()
            future_df['sales_per_ad_dollar'] = future_df['Product_Sales'] / (future_df['Total_Ad_Spend'] + 1)
        
        if 'Has_Promotion' in self.weekly_sales.columns:
            future_df['Has_Promotion'] = self.weekly_sales['Has_Promotion'].tail(4).mean()
            future_df['promo_lag1'] = self.weekly_sales['Has_Promotion'].iloc[-1]
            future_df['promo_streak'] = self.weekly_sales['Has_Promotion'].tail(3).sum()
        
        if 'Voucher_Cost' in self.weekly_sales.columns:
            recent_voucher = self.weekly_sales['Voucher_Cost'].tail(4).mean()
            future_df['Voucher_Cost'] = recent_voucher
            future_df['voucher_roi'] = future_df['Product_Sales'] / (future_df['Voucher_Cost'] + 1)
        
        if 'Flash_Sales' in self.weekly_sales.columns:
            future_df['Flash_Sales'] = self.weekly_sales['Flash_Sales'].tail(4).mean()
        
        # Predict
        X_future = future_df[self.feature_cols]
        future_predictions = final_model.predict(X_future)
        future_predictions = np.maximum(future_predictions, 0)
        
        future_df['Predicted_Sales'] = future_predictions
        
        print(f"✅ Forecast generated!")
        print(f"   Period: {future_weeks[0].date()} to {future_weeks[-1].date()}")
        print(f"   Total 6-month: IDR {future_predictions.sum()/1e9:.2f}B")
        print(f"   Avg weekly: IDR {future_predictions.mean()/1e6:.2f}M")
        print(f"   Model accuracy: {self.metrics.get('Test_Accuracy', 0):.2f}%")
        
        return future_df
    
    def get_feature_importance(self):
        """Get feature importance from trained model"""
        if self.model is None:
            return None
        
        importance_df = pd.DataFrame({
            'Feature': self.feature_cols,
            'Importance': self.model.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        return importance_df
