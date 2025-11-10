# 🎯 Nazava Data Showdown Challenge Brief

## 📋 Challenge Overview

**Challenge**: Optimizing Multi-Channel Sales for Nazava

**Company**: Nazava - A social enterprise providing affordable water filters in Indonesia

**Platform**: Shopee (Southeast Asia's largest e-commerce platform)

---

## 🎯 Business Goals

### Primary Objectives:
1. **Increase total revenue** while maintaining marketing costs (ads and promotions) as a constant percentage of revenue
2. **Increase the share of complete water filter sales**:
   - SKUs containing "SAM" 
   - Products priced above Rp 100,000
   - Over smaller accessories

---

## 📊 Project Objectives

### **Objective #1: Identify Key Drivers of Shopee Sales**

Use Shopee data and Nazava's internal MySQL database to identify primary factors correlating with high-performing sales periods.

**Key Questions to Explore**:
- ✅ What is the effectiveness of Shopee promotion features?
- ✅ Which ad campaigns or ad types have the highest ROI? How can this be optimized?
- ✅ How do chat, customer reviews, ratings, and questions influence sales?
- ✅ What else can we learn from the data?

**Status**: ✅ **COMPLETED** - We built the analytics dashboard showing:
- Chat performance and conversion rates
- Campaign effectiveness (Flash Sales, Vouchers, Games, Live)
- Traffic analysis and visitor behavior
- Sales trends and patterns
- Customer service metrics

---

### **Objective #2: Create a Predictive Model for Sales Forecasting**

Build a predictive model to forecast **weekly sales for the next 6 months**.

**Requirements**:
- Account for seasonality
- Account for promotional periods
- Account for advertising spend
- Test accuracy against withheld historical data
- Provide conclusion on model reliability

**Status**: 🔄 **IN PROGRESS** - Next steps:
- [ ] Implement Prophet/ARIMA forecasting model
- [ ] Train on historical data (Jan 2024 - Oct 2025)
- [ ] Test on validation set
- [ ] Evaluate accuracy metrics
- [ ] Build forecasting dashboard page

---

### **Objective #3: Data-Driven Strategy & Automation**

Synthesize findings to create actionable recommendations and ideally build a **(semi) automated, self-learning bot**.

**Deliverables**:
- Specific, actionable recommendations for:
  - Optimizing ad spending
  - Timing promotional campaigns
  - Improving product listings on Shopee
- **Bot Requirements**:
  - Runs on Nazava's AWS infrastructure
  - Continuously ingests Nazava MySQL + Shopee API data
  - Optimizes Shopee promotions
  - Recommends ad/promo actions
  - Uses Shopee's two-way API (read data + send messages/campaigns/ads)

**Status**: 🔄 **PLANNED** - Next steps:
- [ ] Customer segmentation (identify high-value customers)
- [ ] Product recommendations
- [ ] Price optimization
- [ ] Marketing mix optimization
- [ ] Automated campaign recommendations

---

## 📁 Available Data

### **Shopee Data Exports** (Jan 2024 - Oct 2025)
✅ Already cleaned and integrated:
- Chat data (22 months)
- Traffic overview (730 days)
- Flash sale metrics (22 months)
- Product overview (31 days)
- Voucher data
- Game/Prize campaigns
- Live streaming data
- Off-platform traffic
- Mass chat broadcasts

### **Nazava MySQL Database**
- All sales data (duplicate of Shopee order data)
- Customer information
- Order history
- Invoice data
- Payment records

### **Shopee API Access**
- Two-way API (read + write)
- Can retrieve sales data
- Can send chat messages
- Can manage campaigns
- Can create advertisements

---

## ✅ What We've Built So Far

### **1. Data Cleaning Pipeline** ✅
- Translated Indonesian data to English
- Cleaned 1,601 rows across 11 categories
- Standardized formats (currency, percentages, dates)

### **2. Analytics Dashboard** ✅
- **Overview**: KPIs, trends, funnel
- **Traffic**: Visitor analysis, sources, engagement
- **Sales**: Revenue metrics, channel performance
- **Campaigns**: Flash sales, vouchers, games, live streaming
- **Customer Service**: Chat metrics, CSAT, response times
- **Products**: Product funnel, cart behavior, conversion

### **3. Backend API** ✅
- 31 REST API endpoints
- FastAPI with SQLAlchemy
- Analytics, Predictions, Insights, Reports services
- PostgreSQL + Redis ready

---

## 🎯 What's Next (To Complete Challenge)

### **Immediate Priorities**:

1. **Build Predictive Models** (Objective #2)
   - Sales forecasting (Prophet/ARIMA)
   - Traffic prediction
   - Demand forecasting
   - Seasonality analysis

2. **ML Insights Engine** (Objective #3)
   - Customer segmentation (K-means, DBSCAN)
   - Product recommendations
   - Price optimization
   - Campaign ROI optimization

3. **Automated Bot** (Objective #3)
   - Integrate Shopee API (two-way)
   - AWS deployment
   - Continuous data ingestion
   - Automated recommendations
   - Self-learning capabilities

---

## 📊 Key Metrics to Track

### **Revenue Metrics**:
- Total sales: IDR 649.3M (current)
- Average order value
- Revenue per visitor
- Marketing cost as % of revenue

### **Product Mix**:
- % of complete filter sales (SAM products, >Rp 100K)
- % of accessory sales
- Product conversion rates

### **Marketing Efficiency**:
- ROI by campaign type
- Cost per acquisition
- Customer lifetime value
- Ad spend efficiency

### **Engagement Metrics**:
- Chat conversion rate: Currently 2.01%
- CSAT score: Currently 94.2%
- Response time: Average varies
- Review impact on sales

---

## 🎯 Success Criteria

1. ✅ **Identify key sales drivers** - Dashboard shows correlations
2. 🔄 **Build accurate forecasting model** - Target: 85%+ accuracy
3. 🔄 **Create actionable recommendations** - Data-driven strategy
4. 🔄 **Deploy automated optimization bot** - AWS-hosted, API-integrated

---

## 🔗 Resources

- **Shopee API Guide**: [Developer Guide](https://open.shopee.com/developer-guide/4)
- **Data Location**: `/Users/tarang/Downloads/Analytical Showdown/`
- **Cleaned Data**: `analytical-showdown-pipeline/cleaned_data/`
- **Platform**: `shopee-analytics-platform/`

---

## 📝 Challenge Alignment

### What We've Accomplished:
✅ **Objective #1**: Identified key drivers through comprehensive analytics
- Chat effectiveness: 94.2% CSAT, drives IDR 441M in sales
- Flash sales: IDR 208M revenue, high click rates
- Traffic patterns: 125K visitors, conversion insights
- Campaign ROI: Vouchers, games, live streaming analysis

### What's Remaining:
🔄 **Objective #2**: Build predictive forecasting model
🔄 **Objective #3**: Create automated optimization bot

---

## 🚀 Next Steps

1. **Train ML Models**:
   - Sales forecasting (6-month prediction)
   - Demand prediction by product
   - Seasonality detection

2. **Build Optimization Engine**:
   - Customer segmentation
   - Campaign recommendations
   - Price optimization
   - Ad spend allocation

3. **Deploy Automation**:
   - Integrate Shopee API
   - AWS deployment
   - Continuous learning
   - Automated actions

---

**Current Status**: 50% Complete - Analytics ✅ | Predictions 🔄 | Automation 🔄

**Platform**: Nazava Analytics Platform - Ready for ML integration!
