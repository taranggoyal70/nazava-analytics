# Sample Data for Testing

This folder contains sample datasets for testing the Nazava Analytics Dashboard.

## Data Files Included

All files are located in `data/cleaned/` directory:

### Core Sales & Traffic Data
- `traffic_overview_cleaned.csv` - Daily traffic metrics (visitors, views, time spent)
- `product_overview_cleaned.csv` - Product performance data
- `revenue_2_cleaned.csv` - Revenue and sales data

### Campaign & Promotional Data
- `flash_sale_cleaned.csv` - Flash sale campaign performance
- `voucher_cleaned.csv` - Voucher campaign data
- `live_cleaned.csv` - Live streaming event data
- `game_cleaned.csv` - Gamification campaign data

### Customer Service Data
- `chat_data_cleaned.csv` - Customer service chat metrics
- `mass_chat_data_cleaned.csv` - Mass broadcast campaign data

### Additional Data
- `off_platform_cleaned.csv` - Off-platform traffic sources
- `shopee_paylater_cleaned.csv` - PayLater payment data

### Processed Data
- `weekly_sales_CLEAN.csv` - Aggregated weekly sales (used for forecasting)

## How to Use

1. **Extract the data** to the `data/cleaned/` folder
2. **Run the dashboard**:
   ```bash
   cd dashboard
   streamlit run app.py
   ```
3. **Login** with demo credentials:
   - Username: `admin`
   - Password: `admin123`

## Data Period

- **Date Range**: January 2024 - October 2025
- **Total Weeks**: 58 weeks
- **Records**: Varies by dataset (see individual files)

## Data Quality

All data has been:
- ✅ Cleaned and validated
- ✅ Formatted consistently
- ✅ Tested with the dashboard
- ✅ Ready for analysis

## Questions?

If you encounter any issues with the data, please check:
1. Files are in the correct `data/cleaned/` directory
2. File names match exactly (case-sensitive)
3. CSV files are not corrupted

For technical issues, refer to the main README.md or SETUP.md files.
