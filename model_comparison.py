#!/usr/bin/env python3
"""
Comprehensive Model Comparison for Sales Forecasting
Compares: Gradient Boosting, XGBoost, Random Forest, LightGBM, and Linear Models
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import time
warnings.filterwarnings('ignore')

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score

# Try importing advanced libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️  XGBoost not installed. Run: pip install xgboost")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    print("⚠️  LightGBM not installed. Run: pip install lightgbm")

print("="*70)
print("🔬 SALES FORECASTING MODEL COMPARISON")
print("="*70)

# Load and prepare data
print("\n📊 Loading data...")
weekly_sales = pd.read_csv('data/processed/weekly_sales_CLEAN.csv')
weekly_sales['Week'] = pd.to_datetime(weekly_sales['Week'])

# Enhanced Feature Engineering (same as improved model)
print("🔧 Engineering features...")
weekly_sales['week_of_year'] = weekly_sales['Week'].dt.isocalendar().week
weekly_sales['month'] = weekly_sales['Week'].dt.month
weekly_sales['quarter'] = weekly_sales['Week'].dt.quarter
weekly_sales['year'] = weekly_sales['Week'].dt.year
weekly_sales['is_month_start'] = (weekly_sales['Week'].dt.day <= 7).astype(int)
weekly_sales['is_month_end'] = (weekly_sales['Week'].dt.day >= 22).astype(int)

# Lag features
weekly_sales['sales_lag1'] = weekly_sales['Total_Sales'].shift(1)
weekly_sales['sales_lag2'] = weekly_sales['Total_Sales'].shift(2)
weekly_sales['sales_lag3'] = weekly_sales['Total_Sales'].shift(3)

# Rolling averages
weekly_sales['sales_ma3'] = weekly_sales['Total_Sales'].rolling(window=3, min_periods=1).mean()
weekly_sales['sales_ma4'] = weekly_sales['Total_Sales'].rolling(window=4, min_periods=1).mean()

# Volatility
weekly_sales['sales_std3'] = weekly_sales['Total_Sales'].rolling(window=3, min_periods=1).std()

# Interaction features
weekly_sales['product_buyer_ratio'] = weekly_sales['Products'] / (weekly_sales['Buyers'] + 1)
weekly_sales['sales_per_product'] = weekly_sales['Product_Sales'] / (weekly_sales['Products'] + 1)
weekly_sales['sales_per_buyer'] = weekly_sales['Product_Sales'] / (weekly_sales['Buyers'] + 1)

# Trend features
weekly_sales['sales_diff1'] = weekly_sales['Total_Sales'].diff(1)
weekly_sales['sales_diff2'] = weekly_sales['Total_Sales'].diff(2)

# Feature list
feature_cols = [
    'week_of_year', 'month', 'quarter', 'year', 
    'is_month_start', 'is_month_end',
    'Product_Sales', 'Buyers', 'Products',
    'sales_lag1', 'sales_lag2', 'sales_lag3',
    'sales_ma3', 'sales_ma4',
    'sales_std3',
    'product_buyer_ratio', 'sales_per_product', 'sales_per_buyer',
    'sales_diff1', 'sales_diff2'
]

# Train/Test split
train_size = int(len(weekly_sales) * 0.8)
train_data = weekly_sales[:train_size].copy()
test_data = weekly_sales[train_size:].copy()

X_train = train_data[feature_cols].fillna(train_data[feature_cols].mean())
y_train = train_data['Total_Sales']
X_test = test_data[feature_cols].fillna(train_data[feature_cols].mean())
y_test = test_data['Total_Sales']

print(f"✅ Features: {len(feature_cols)}")
print(f"✅ Train: {len(train_data)} weeks | Test: {len(test_data)} weeks")

# Define models to compare
models = {}

# 1. Gradient Boosting (Enhanced)
models['Gradient Boosting'] = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    min_samples_split=3,
    min_samples_leaf=1,
    subsample=0.85,
    max_features='sqrt',
    random_state=42
)

# 2. XGBoost
if XGBOOST_AVAILABLE:
    models['XGBoost'] = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42,
        verbosity=0
    )

# 3. LightGBM
if LIGHTGBM_AVAILABLE:
    models['LightGBM'] = lgb.LGBMRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42,
        verbosity=-1
    )

# 4. Random Forest
models['Random Forest'] = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=3,
    min_samples_leaf=1,
    max_features='sqrt',
    random_state=42,
    n_jobs=-1
)

# 5. Linear Models
models['Linear Regression'] = LinearRegression()
models['Ridge'] = Ridge(alpha=1.0, random_state=42)
models['Lasso'] = Lasso(alpha=1.0, random_state=42)
models['ElasticNet'] = ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42)

# Train and evaluate all models
print("\n" + "="*70)
print("🚀 TRAINING AND EVALUATING MODELS")
print("="*70)

results = []

for name, model in models.items():
    print(f"\n⏳ Training {name}...")
    start_time = time.time()
    
    # Train
    model.fit(X_train, y_train)
    train_time = time.time() - start_time
    
    # Predict
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    def calculate_mape(y_true, y_pred):
        mask = y_true > 0
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    
    mae_train = mean_absolute_error(y_train, y_pred_train)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    
    mape_test = calculate_mape(y_test.values, y_pred_test)
    accuracy = 100 - mape_test
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                                scoring='neg_mean_absolute_error', n_jobs=-1)
    cv_mae = -cv_scores.mean()
    
    # Store results
    results.append({
        'Model': name,
        'Train MAE (M)': mae_train/1e6,
        'Test MAE (M)': mae_test/1e6,
        'Test RMSE (M)': rmse_test/1e6,
        'Test R²': r2_test,
        'Test MAPE (%)': mape_test,
        'Accuracy (%)': accuracy,
        'CV MAE (M)': cv_mae/1e6,
        'Train Time (s)': train_time,
        'Predictions': y_pred_test
    })
    
    print(f"✅ {name}: Test MAE = IDR {mae_test/1e6:.2f}M | Accuracy = {accuracy:.2f}%")

# Create results DataFrame
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Test MAE (M)')

# Display results
print("\n" + "="*70)
print("📊 MODEL COMPARISON RESULTS (Sorted by Test MAE)")
print("="*70)
display_df = results_df.drop('Predictions', axis=1).copy()
print(display_df.to_string(index=False))

# Find best model
best_model = results_df.iloc[0]
print("\n" + "="*70)
print(f"🏆 BEST MODEL: {best_model['Model']}")
print("="*70)
print(f"  Test MAE: IDR {best_model['Test MAE (M)']:.2f}M")
print(f"  Test RMSE: IDR {best_model['Test RMSE (M)']:.2f}M")
print(f"  Test R²: {best_model['Test R²']:.4f}")
print(f"  Accuracy: {best_model['Accuracy (%)']:.2f}%")
print(f"  CV MAE: IDR {best_model['CV MAE (M)']:.2f}M")
print(f"  Training Time: {best_model['Train Time (s)']:.2f}s")

# Visualizations
print("\n📈 Creating visualizations...")

fig = plt.figure(figsize=(18, 12))

# 1. Test MAE Comparison
ax1 = plt.subplot(2, 3, 1)
sns.barplot(data=display_df, y='Model', x='Test MAE (M)', palette='viridis', ax=ax1)
ax1.set_title('Test MAE Comparison (Lower is Better)', fontweight='bold')
ax1.set_xlabel('MAE (Million IDR)')

# 2. Accuracy Comparison
ax2 = plt.subplot(2, 3, 2)
sns.barplot(data=display_df, y='Model', x='Accuracy (%)', palette='rocket', ax=ax2)
ax2.set_title('Accuracy Comparison (Higher is Better)', fontweight='bold')
ax2.set_xlabel('Accuracy (%)')

# 3. R² Comparison
ax3 = plt.subplot(2, 3, 3)
sns.barplot(data=display_df, y='Model', x='Test R²', palette='mako', ax=ax3)
ax3.set_title('R² Score Comparison (Higher is Better)', fontweight='bold')
ax3.set_xlabel('R² Score')

# 4. Training Time Comparison
ax4 = plt.subplot(2, 3, 4)
sns.barplot(data=display_df, y='Model', x='Train Time (s)', palette='flare', ax=ax4)
ax4.set_title('Training Time Comparison', fontweight='bold')
ax4.set_xlabel('Time (seconds)')

# 5. Predictions Comparison (Top 3 models)
ax5 = plt.subplot(2, 3, 5)
for idx in range(min(3, len(results_df))):
    model_result = results_df.iloc[idx]
    ax5.plot(test_data.index, model_result['Predictions']/1e6, 
             marker='o', label=model_result['Model'], alpha=0.7)
ax5.plot(test_data.index, y_test/1e6, 'k--', linewidth=2, label='Actual', alpha=0.8)
ax5.set_title('Top 3 Models: Predictions vs Actual', fontweight='bold')
ax5.set_xlabel('Test Sample Index')
ax5.set_ylabel('Sales (Million IDR)')
ax5.legend()
ax5.grid(True, alpha=0.3)

# 6. Error Distribution (Best Model)
ax6 = plt.subplot(2, 3, 6)
best_predictions = best_model['Predictions']
errors = y_test - best_predictions
ax6.hist(errors/1e6, bins=15, color='steelblue', alpha=0.7, edgecolor='black')
ax6.axvline(0, color='red', linestyle='--', linewidth=2)
ax6.set_title(f'Error Distribution: {best_model["Model"]}', fontweight='bold')
ax6.set_xlabel('Prediction Error (Million IDR)')
ax6.set_ylabel('Frequency')
ax6.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('model_comparison_results.png', dpi=300, bbox_inches='tight')
print("✅ Saved: model_comparison_results.png")
plt.show()

# Save results to CSV
display_df.to_csv('model_comparison_results.csv', index=False)
print("✅ Saved: model_comparison_results.csv")

print("\n" + "="*70)
print("✅ MODEL COMPARISON COMPLETE!")
print("="*70)
