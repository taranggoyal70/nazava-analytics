# 📊 6-Month Comparison Guide

## Overview

The Nazava Analytics Platform now includes powerful period comparison features that allow you to compare performance across different time periods (6 months, 3 months, custom ranges, etc.).

---

## 🎯 How to Use Period Comparison

### Method 1: Dedicated Comparison Page

**Navigate to**: Period Comparison page (new page in navigation)

**Features:**
- Compare traffic metrics across periods
- Compare sales performance
- Compare product metrics
- Visual trend comparisons
- Export comparison data

**Steps:**
1. Go to the "Period Comparison" page
2. Select your desired time period (Last 6 Months, Last 3 Months, etc.)
3. View automatic comparison with the previous period
4. Analyze growth/decline percentages
5. Export comparison summary

---

### Method 2: Add Comparison to Any Page

You can add period comparison to any existing dashboard page using the reusable component.

**Example Integration:**

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.date_filter import (
    create_date_filter,
    display_comparison_metric,
    create_comparison_chart
)

# In your page code:
# 1. Add date filter
filtered_df, comparison_df, date_range = create_date_filter(your_df, 'Date')

# 2. Display comparison metrics
current_value = filtered_df['metric'].sum()
previous_value = comparison_df['metric'].sum()
display_comparison_metric("Metric Name", current_value, previous_value, 'number', '📊')

# 3. Create comparison chart
fig = create_comparison_chart(filtered_df, comparison_df, 'metric_column', 'Date', 'Chart Title')
st.plotly_chart(fig, use_container_width=True)
```

---

## 📅 Available Time Periods

### Preset Options:
1. **Last 6 Months** - Compares last 6 months with previous 6 months
2. **Last 3 Months** - Compares last 3 months with previous 3 months
3. **Last Month** - Compares last 30 days with previous 30 days
4. **Custom Range** - Select any start and end date
5. **All Time** - View all available data (no comparison)

### Comparison Logic:
- **Current Period**: Your selected date range
- **Previous Period**: Same length period immediately before current period
- **Metrics**: Automatic calculation of change value and percentage

---

## 📊 Comparison Metrics

### Available Metric Types:

1. **Number Format**
   - Total visitors
   - Total orders
   - Product visits
   - Display: `1,234 (▲ 15.2%)`

2. **Currency Format**
   - Total sales
   - Revenue
   - Average order value
   - Display: `IDR 42.5M (▲ 12.3%)`

3. **Percentage Format**
   - Conversion rates
   - Growth rates
   - Engagement rates
   - Display: `2.7% (▲ 0.3pp)`

### Trend Indicators:
- ▲ **Green** = Positive growth
- ▼ **Red** = Decline
- = **Gray** = No change

---

## 📈 Comparison Charts

### Features:
- **Dual-line charts** showing current vs previous period
- **Filled area** for current period (better visibility)
- **Dashed line** for previous period (clear distinction)
- **Unified hover** to compare exact dates
- **Color coding**: Blue (current), Gray (previous)

### Chart Types Available:
1. Traffic trends
2. Sales trends
3. Conversion trends
4. Engagement trends

---

## 💡 Use Cases

### 1. Month-over-Month Analysis
```
Period: Last Month
Comparison: Previous Month
Use: Track monthly performance
```

### 2. Seasonal Comparison
```
Period: Custom (e.g., Dec 2024)
Comparison: Previous year (Dec 2023)
Use: Identify seasonal patterns
```

### 3. Campaign Impact
```
Period: Campaign duration
Comparison: Same period before campaign
Use: Measure campaign effectiveness
```

### 4. Quarter-over-Quarter
```
Period: Last 3 Months
Comparison: Previous 3 Months
Use: Quarterly business reviews
```

### 5. Half-Year Review
```
Period: Last 6 Months
Comparison: Previous 6 Months
Use: Semi-annual performance review
```

---

## 🎯 Best Practices

### 1. Choose Appropriate Periods
- **Short-term trends**: Use 1-month comparison
- **Medium-term trends**: Use 3-month comparison
- **Long-term trends**: Use 6-month comparison
- **Seasonal analysis**: Use year-over-year comparison

### 2. Consider Seasonality
- Compare similar seasons (e.g., Q4 2024 vs Q4 2023)
- Account for holidays and special events
- Look for recurring patterns

### 3. Context Matters
- Consider external factors (market conditions, competition)
- Account for internal changes (new campaigns, price changes)
- Look at multiple metrics together

### 4. Export and Share
- Download comparison summaries for reports
- Share insights with stakeholders
- Track trends over time

---

## 📥 Exporting Comparison Data

### Available Export Formats:

**CSV Export** includes:
- Metric names
- Current period values
- Previous period values
- Change values
- Change percentages

**Example Export:**
```csv
Metric,Current Period,Previous Period,Change (%)
Total Visitors,45600,38200,+19.4%
Total Sales,649300000,582100000,+11.5%
Conversion Rate,2.7%,2.4%,+12.5%
```

---

## 🔧 Technical Details

### Component Location:
`dashboard/components/date_filter.py`

### Key Functions:

1. **create_date_filter(df, date_column)**
   - Creates date range selector
   - Returns filtered and comparison DataFrames
   - Handles date parsing and validation

2. **display_comparison_metric(label, current, previous, format, icon)**
   - Displays metric with comparison
   - Calculates change percentage
   - Shows trend indicator

3. **create_comparison_chart(current_df, comparison_df, metric, date, title)**
   - Creates dual-line comparison chart
   - Handles data aggregation
   - Returns Plotly figure

4. **calculate_comparison_metrics(current, previous)**
   - Calculates change value
   - Calculates change percentage
   - Determines trend direction

---

## 🚀 Quick Start Examples

### Example 1: Compare Last 6 Months Traffic
```python
# Load traffic data
traffic_df = pd.read_csv("traffic_overview_cleaned.csv")

# Apply date filter
filtered, comparison, _ = create_date_filter(traffic_df, 'Date')

# Calculate metrics
current_visitors = filtered['Total_Visitors'].sum()
previous_visitors = comparison['Total_Visitors'].sum()

# Display comparison
display_comparison_metric(
    "Total Visitors", 
    current_visitors, 
    previous_visitors, 
    'number', 
    '👥'
)
```

### Example 2: Compare Sales Performance
```python
# Load product data
product_df = pd.read_csv("product_overview_cleaned.csv")

# Apply filter
filtered, comparison, _ = create_date_filter(product_df, 'Date')

# Calculate sales
current_sales = pd.to_numeric(filtered['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
previous_sales = pd.to_numeric(comparison['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()

# Display
display_comparison_metric(
    "Total Sales",
    current_sales,
    previous_sales,
    'currency',
    '💰'
)
```

### Example 3: Create Comparison Chart
```python
# Create visual comparison
fig = create_comparison_chart(
    filtered_df,
    comparison_df,
    'Total_Visitors',
    'Date',
    'Visitor Trends: 6-Month Comparison'
)

st.plotly_chart(fig, use_container_width=True)
```

---

## 📊 Integration with Existing Pages

### Pages Ready for Comparison:
- ✅ Period Comparison (dedicated page)
- 🔄 Overview (can be added)
- 🔄 Traffic (can be added)
- 🔄 Sales (can be added)
- 🔄 Products (can be added)
- 🔄 Campaigns (can be added)

### To Add Comparison to Any Page:
1. Import the component functions
2. Add `create_date_filter()` at the top
3. Replace static metrics with `display_comparison_metric()`
4. Add comparison charts where needed
5. Test with different date ranges

---

## 💡 Tips & Tricks

### Tip 1: Multiple Comparisons
Compare multiple metrics side-by-side to identify correlations:
- Traffic ↑ + Sales ↑ = Good growth
- Traffic ↑ + Sales → = Conversion issue
- Traffic → + Sales ↑ = Better conversion

### Tip 2: Drill Down
Start with 6-month view, then drill down to specific periods that show interesting patterns.

### Tip 3: Export for Reports
Use the export feature to create executive summaries and board reports.

### Tip 4: Set Benchmarks
Use comparison data to set realistic growth targets based on historical performance.

---

## 🎯 Success Metrics

Track these key comparisons:

### Growth Metrics:
- [ ] Traffic growth (month-over-month)
- [ ] Sales growth (month-over-month)
- [ ] Customer acquisition (new vs returning)
- [ ] Conversion rate improvement

### Efficiency Metrics:
- [ ] Cost per acquisition trend
- [ ] Average order value trend
- [ ] Cart abandonment rate
- [ ] Customer satisfaction (CSAT)

### Campaign Metrics:
- [ ] Campaign ROI comparison
- [ ] Channel performance comparison
- [ ] Promotion effectiveness
- [ ] Seasonal performance

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Platform**: Nazava Analytics Platform
