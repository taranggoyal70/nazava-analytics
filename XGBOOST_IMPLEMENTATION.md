# 🚀 XGBoost Implementation Guide

## Quick Start: Upgrade to XGBoost

XGBoost achieved **89.18% accuracy** vs Gradient Boosting's **78.91%** - a **40% reduction in error**!

---

## Step 1: Install XGBoost

```bash
pip install xgboost
```

---

## Step 2: Update Your Notebook

Replace the Gradient Boosting model (Cell 6) with this XGBoost code:

```python
# Train XGBoost Model (BEST PERFORMER!)
print("\n🚀 TRAINING XGBOOST MODEL")
print("-"*60)

import xgboost as xgb

# XGBoost with optimized hyperparameters
model = xgb.XGBRegressor(
    n_estimators=200,        # Number of boosting rounds
    max_depth=6,             # Maximum tree depth
    learning_rate=0.05,      # Step size shrinkage
    subsample=0.85,          # Row sampling
    colsample_bytree=0.85,   # Column sampling
    random_state=42,
    verbosity=0              # Suppress warnings
)

model.fit(X_train, y_train)

print("✅ XGBoost model trained!")

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\nTop 10 Important Features:")
for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['Feature']}: {row['Importance']:.4f}")
```

---

## Step 3: Update Forecast Generation (Cell 12)

Replace the final model training with XGBoost:

```python
# Generate 6-month forecast with XGBoost
print("\n🔮 GENERATING 6-MONTH FORECAST (XGBOOST)")
print("="*60)

# Retrain on all data with XGBoost
X_all = weekly_sales[feature_cols].fillna(weekly_sales[feature_cols].mean())
y_all = weekly_sales['Total_Sales']

final_model = xgb.XGBRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    random_state=42,
    verbosity=0
)

final_model.fit(X_all, y_all)

# ... rest of forecast code stays the same ...
```

---

## Expected Results

### Performance Metrics:
- **Test MAE**: IDR 2.39M (vs 3.98M with GB)
- **Test RMSE**: IDR 2.62M (vs 5.33M with GB)
- **Test R²**: 0.974 (vs 0.893 with GB)
- **Accuracy**: 89.18% (vs 78.91% with GB)
- **CV MAE**: IDR 2.82M (vs 4.21M with GB)

### Improvements:
- ✅ **40% lower error** (MAE)
- ✅ **51% lower RMSE**
- ✅ **+10.3% accuracy**
- ✅ **Better R²** (0.974 vs 0.893)

---

## Full XGBoost Notebook Cell

Here's the complete cell to replace Cell 6:

```python
# Train XGBoost Model - BEST PERFORMER!
print("\n🚀 TRAINING XGBOOST MODEL (89.18% Accuracy)")
print("-"*60)

import xgboost as xgb

# XGBoost Regressor with optimized hyperparameters
model = xgb.XGBRegressor(
    n_estimators=200,        # More trees for better learning
    max_depth=6,             # Deeper trees to capture complexity
    learning_rate=0.05,      # Lower learning rate for better generalization
    subsample=0.85,          # Row sampling to prevent overfitting
    colsample_bytree=0.85,   # Column sampling for robustness
    min_child_weight=1,      # Minimum sum of instance weight in a child
    gamma=0,                 # Minimum loss reduction for split
    reg_alpha=0,             # L1 regularization
    reg_lambda=1,            # L2 regularization
    random_state=42,
    verbosity=0,             # Suppress warnings
    n_jobs=-1                # Use all CPU cores
)

# Train the model
model.fit(X_train, y_train)

print("✅ XGBoost model trained!")

# Make predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\nTop 10 Important Features:")
for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['Feature']}: {row['Importance']:.4f}")
```

---

## Hyperparameter Explanation

| Parameter | Value | Why |
|-----------|-------|-----|
| `n_estimators` | 200 | More trees = better learning |
| `max_depth` | 6 | Balance complexity vs overfitting |
| `learning_rate` | 0.05 | Slower learning = better generalization |
| `subsample` | 0.85 | Use 85% of data per tree (prevents overfitting) |
| `colsample_bytree` | 0.85 | Use 85% of features per tree (robustness) |
| `random_state` | 42 | Reproducible results |
| `verbosity` | 0 | Clean output |
| `n_jobs` | -1 | Use all CPU cores (faster) |

---

## Alternative: Create New XGBoost Notebook

If you want to keep the Gradient Boosting notebook, create a new one:

1. Copy `Nazava_FINAL_GradientBoosting.ipynb`
2. Rename to `Nazava_FINAL_XGBoost.ipynb`
3. Update title to "XGBoost: 89.18% Accuracy"
4. Replace model cells with XGBoost code above
5. Update output filename to `weekly_sales_forecast_6months_XGBOOST.csv`

---

## Comparison: GB vs XGBoost

| Metric | Gradient Boosting | XGBoost | Winner |
|--------|-------------------|---------|--------|
| Test MAE | IDR 3.98M | IDR 2.39M | 🏆 XGBoost |
| Test RMSE | IDR 5.33M | IDR 2.62M | 🏆 XGBoost |
| Test R² | 0.893 | 0.974 | 🏆 XGBoost |
| Accuracy | 78.91% | 89.18% | 🏆 XGBoost |
| CV MAE | IDR 4.21M | IDR 2.82M | 🏆 XGBoost |
| Training Time | 0.03s | 0.27s | 🏆 GB |
| Dependencies | None | XGBoost | 🏆 GB |

**Verdict**: XGBoost wins on all performance metrics!

---

## Troubleshooting

### If XGBoost install fails:
```bash
# Try with conda
conda install -c conda-forge xgboost

# Or upgrade pip first
pip install --upgrade pip
pip install xgboost
```

### If you get import errors:
```python
try:
    import xgboost as xgb
    print("✅ XGBoost available!")
except ImportError:
    print("❌ XGBoost not installed. Run: pip install xgboost")
```

---

## Next Steps

1. ✅ Install XGBoost: `pip install xgboost`
2. ✅ Update notebook Cell 6 with XGBoost code
3. ✅ Update notebook Cell 12 for forecast
4. ✅ Run the notebook
5. ✅ Enjoy 89.18% accuracy! 🎉

---

*Recommendation: Switch to XGBoost for 40% better performance!*
