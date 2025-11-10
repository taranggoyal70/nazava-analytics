# 📊 Jupyter Notebook vs Website Dashboard - Comparison

## 🎯 Executive Summary

**Status**: ⚠️ **MISMATCH DETECTED**

The Jupyter notebook uses a **superior XGBoost model** with **89.18% accuracy**, while the website dashboard uses a **Prophet model** with **~75% accuracy**.

---

## 📋 Detailed Comparison

### **1. Model Type**

| Aspect | Jupyter Notebook | Website Dashboard |
|--------|------------------|-------------------|
| **Algorithm** | XGBoost (Gradient Boosting) | Prophet (Facebook's Time Series) |
| **Model File** | `Nazava_FINAL_GradientBoosting.ipynb` | `ml/forecasting/final_sales_forecaster.py` |
| **Complexity** | Advanced ML with 25+ features | Simple time series |

---

### **2. Accuracy Metrics**

| Metric | Jupyter Notebook (XGBoost) | Website Dashboard (Prophet) |
|--------|---------------------------|----------------------------|
| **Test Accuracy** | 89.18% ✅ | ~75% ⚠️ |
| **MAPE** | 10.82% | ~25% |
| **R²** | 0.9742 | ~0.65 |
| **MAE** | IDR 2.39M | Higher |
| **RMSE** | IDR 2.62M | Higher |

**Winner**: 🏆 **Jupyter Notebook (XGBoost)** - 14% more accurate!

---

### **3. Data Used**

| Aspect | Jupyter Notebook | Website Dashboard |
|--------|------------------|-------------------|
| **Data Source** | Weekly aggregated (58 weeks) | Daily product data (31 days) |
| **Time Range** | Jan 2024 - Oct 2025 (22 months) | Sep 2025 only (1 month) |
| **Data Points** | 58 weeks | 31 days |
| **Data Quality** | Clean, aggregated, comprehensive | Limited, single month |

**Winner**: 🏆 **Jupyter Notebook** - Much more data!

---

### **4. Features Used**

#### **Jupyter Notebook (XGBoost) - 25+ Features:**

**Time Features (6):**
- week_of_year
- month
- quarter
- year
- is_month_start
- is_month_end

**Sales Features (12):**
- sales_lag1, sales_lag2, sales_lag3
- sales_ma3, sales_ma4
- sales_std3 (volatility)
- sales_diff1, sales_diff2
- product_buyer_ratio
- sales_per_product
- sales_per_buyer

**Marketing Features (8+):**
- Total_Ad_Spend ✅
- ad_spend_lag1
- ad_spend_ma3
- sales_per_ad_dollar (ROI)
- Has_Promotion ✅
- promo_lag1
- promo_streak
- voucher_roi ✅
- Flash_Sales ✅

**Core Features:**
- Product_Sales
- Buyers
- Products

#### **Website Dashboard (Prophet) - 1 Feature:**
- Date (ds)
- Sales (y)

**Winner**: 🏆 **Jupyter Notebook** - 25x more features!

---

### **5. Challenge Requirements Met**

| Requirement | Jupyter Notebook | Website Dashboard |
|-------------|------------------|-------------------|
| **1. Weekly Sales Forecast for 6 Months** | ✅ Yes (26 weeks) | ✅ Yes (26 weeks) |
| **2. Account for Seasonality** | ✅ Yes (week, month, quarter) | ⚠️ Limited (weekly only) |
| **3. Account for Promotional Periods** | ✅ Yes (flash sales, vouchers, live, games) | ❌ No |
| **4. Account for Advertising Spend** | ✅ Yes (total ad spend, ROI, voucher costs) | ❌ No |
| **5. Test Accuracy Against Withheld Data** | ✅ Yes (80/20 split, 89.18%) | ⚠️ Limited (in-sample only) |
| **6. Model Reliability Conclusion** | ✅ Yes (comprehensive metrics) | ⚠️ Basic metrics |

**Winner**: 🏆 **Jupyter Notebook** - Meets ALL requirements!

---

### **6. Forecast Output**

| Aspect | Jupyter Notebook | Website Dashboard |
|--------|------------------|-------------------|
| **Period** | Dec 2025 - Jun 2026 | Next 6 months from current |
| **Total Forecast** | IDR 0.83B | Different (Prophet-based) |
| **Avg Weekly** | IDR 31.82M | Different |
| **Min Weekly** | IDR 31.65M | Different |
| **Max Weekly** | IDR 32.39M | Different |
| **Confidence** | 89.18% accuracy | ~75% accuracy |

---

### **7. Validation Approach**

| Aspect | Jupyter Notebook | Website Dashboard |
|--------|------------------|-------------------|
| **Train/Test Split** | ✅ 80/20 (46 train, 12 test) | ❌ No split (all data used) |
| **Cross-Validation** | ✅ 5-fold CV | ❌ None |
| **Overfitting Check** | ✅ Yes (train 99.6%, test 89.2%) | ❌ Not checked |
| **Error Analysis** | ✅ Comprehensive | ⚠️ Basic |

**Winner**: 🏆 **Jupyter Notebook** - Rigorous validation!

---

### **8. Feature Importance**

#### **Jupyter Notebook (XGBoost) - Top 10:**
1. Products: 37.14%
2. Buyers: 31.25%
3. Product_Sales: 16.95%
4. sales_diff1: 4.58%
5. sales_diff2: 3.86%
6. product_buyer_ratio: 1.47%
7. sales_ma4: 0.93%
8. sales_lag2: 0.84%
9. is_month_start: 0.58%
10. sales_ma3: 0.54%

#### **Website Dashboard (Prophet):**
- No feature importance (time series only)

**Winner**: 🏆 **Jupyter Notebook** - Explainable AI!

---

### **9. Promotional & Ad Spend Integration**

| Feature | Jupyter Notebook | Website Dashboard |
|---------|------------------|-------------------|
| **Flash Sales** | ✅ Integrated | ❌ Not included |
| **Vouchers** | ✅ Integrated (cost & ROI) | ❌ Not included |
| **Live Streaming** | ✅ Integrated | ❌ Not included |
| **Games/Prizes** | ✅ Integrated | ❌ Not included |
| **Total Ad Spend** | ✅ Tracked & used | ❌ Not included |
| **Promotional Indicators** | ✅ Has_Promotion, promo_streak | ❌ Not included |
| **ROI Metrics** | ✅ sales_per_ad_dollar, voucher_roi | ❌ Not included |

**Winner**: 🏆 **Jupyter Notebook** - Complete marketing integration!

---

### **10. Error Distribution**

#### **Jupyter Notebook (XGBoost):**
- Within ±5% error: 41.7% of predictions
- Within ±10% error: 58.3% of predictions
- Within ±20% error: 75.0% of predictions
- Median error: 6.57%
- 95th percentile error: 24.60%

#### **Website Dashboard (Prophet):**
- Not measured with withheld data
- In-sample metrics only

**Winner**: 🏆 **Jupyter Notebook** - Detailed error analysis!

---

## 🎯 Key Findings

### **What's Different:**

1. **Model Algorithm**
   - Notebook: XGBoost (advanced gradient boosting)
   - Website: Prophet (simple time series)

2. **Data Scope**
   - Notebook: 58 weeks (22 months)
   - Website: 31 days (1 month)

3. **Features**
   - Notebook: 25+ features (time, sales, marketing)
   - Website: 1 feature (just sales)

4. **Accuracy**
   - Notebook: 89.18% (tested on withheld data)
   - Website: ~75% (in-sample only)

5. **Marketing Integration**
   - Notebook: ✅ Full (flash sales, vouchers, ad spend, ROI)
   - Website: ❌ None

6. **Validation**
   - Notebook: ✅ Rigorous (train/test split, cross-validation)
   - Website: ⚠️ Basic (in-sample only)

---

## 🚨 Critical Issues

### **1. Model Mismatch**
- Website uses **inferior Prophet model** (75% accuracy)
- Notebook has **superior XGBoost model** (89.18% accuracy)
- **14% accuracy gap!**

### **2. Missing Requirements**
Website dashboard does NOT meet challenge requirements:
- ❌ No promotional period integration
- ❌ No advertising spend consideration
- ❌ No proper train/test validation
- ❌ Limited seasonality features

### **3. Data Limitation**
- Website uses only 31 days of data
- Notebook uses 58 weeks (22 months)
- **Website has 95% less data!**

### **4. Feature Gap**
- Website: 1 feature
- Notebook: 25+ features
- **Missing 24 critical features!**

---

## ✅ Recommendations

### **Priority 1: Replace Website Model**
**Action**: Update website to use XGBoost model from notebook

**Steps:**
1. Export XGBoost model from notebook
2. Create new forecaster class using XGBoost
3. Update `final_sales_forecaster.py`
4. Load weekly aggregated data (not daily)
5. Include all 25+ features

**Impact**: +14% accuracy improvement!

### **Priority 2: Add Marketing Features**
**Action**: Integrate promotional and ad spend data

**Steps:**
1. Load flash sale, voucher, live, game data
2. Calculate Total_Ad_Spend
3. Create promotional indicators
4. Add ROI metrics
5. Include lag features

**Impact**: Meet all challenge requirements!

### **Priority 3: Improve Data Scope**
**Action**: Use weekly aggregated data (58 weeks)

**Steps:**
1. Load `weekly_sales_CLEAN.csv` from notebook
2. Use 22 months of data instead of 1 month
3. Aggregate promotional data to weekly
4. Match notebook's data structure

**Impact**: 95% more training data!

### **Priority 4: Add Proper Validation**
**Action**: Implement train/test split

**Steps:**
1. 80/20 train/test split
2. 5-fold cross-validation
3. Test on withheld data
4. Report real accuracy (not in-sample)

**Impact**: Reliable accuracy metrics!

---

## 📊 Comparison Summary Table

| Metric | Jupyter Notebook | Website Dashboard | Gap |
|--------|------------------|-------------------|-----|
| **Accuracy** | 89.18% | ~75% | +14% |
| **Data Points** | 58 weeks | 31 days | +95% |
| **Features** | 25+ | 1 | +24 |
| **MAPE** | 10.82% | ~25% | -14% |
| **R²** | 0.9742 | ~0.65 | +0.32 |
| **Marketing Integration** | ✅ Full | ❌ None | - |
| **Validation** | ✅ Rigorous | ⚠️ Basic | - |
| **Requirements Met** | 6/6 ✅ | 2/6 ⚠️ | - |

---

## 🎯 Final Verdict

**Jupyter Notebook Model is SUPERIOR in every way:**

✅ **14% more accurate** (89.18% vs 75%)  
✅ **25x more features** (25+ vs 1)  
✅ **95% more data** (58 weeks vs 31 days)  
✅ **Meets ALL requirements** (6/6 vs 2/6)  
✅ **Proper validation** (train/test split + CV)  
✅ **Marketing integration** (ad spend, promotions, ROI)  
✅ **Explainable** (feature importance)  

**Recommendation**: 🚨 **URGENT - Replace website model with XGBoost from notebook!**

---

## 📁 Files to Update

### **Current Files:**
- ❌ `ml/forecasting/final_sales_forecaster.py` (Prophet-based)
- ❌ `dashboard/pages/7_Sales_Forecast.py` (uses Prophet)

### **New Files Needed:**
- ✅ `ml/forecasting/xgboost_forecaster.py` (from notebook)
- ✅ `data/processed/weekly_sales_CLEAN.csv` (aggregated data)
- ✅ Updated `7_Sales_Forecast.py` (use XGBoost)

---

## 🚀 Next Steps

1. **Export XGBoost model** from notebook
2. **Create XGBoost forecaster class** for website
3. **Update Sales Forecast page** to use XGBoost
4. **Test accuracy** matches notebook (89.18%)
5. **Verify all features** are included
6. **Update documentation** with new metrics

**Estimated Time**: 2-3 hours  
**Impact**: +14% accuracy, meet all requirements!

---

*Analysis Date: November 8, 2025*  
*Notebook: Nazava_FINAL_GradientBoosting.ipynb*  
*Website: dashboard/pages/7_Sales_Forecast.py*
