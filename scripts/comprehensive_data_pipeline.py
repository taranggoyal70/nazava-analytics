"""
Comprehensive Data Cleaning & Translation Pipeline
Works with original raw Indonesian Excel files
Cleans, translates, and prepares data for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Indonesian to English translations
TRANSLATIONS = {
    # Date/Time
    'Tanggal': 'Date',
    'Periode Data': 'Data_Period',
    'Waktu Periode': 'Time_Period',
    
    # Traffic
    'Pengunjung Produk (Kunjungan)': 'Product Visitors (Visits)',
    'Halaman Produk Dilihat': 'Product Page Views',
    'Produk Dikunjungi': 'Products Visited',
    'Pengunjung Melihat Tanpa Membeli': 'Visitors Viewed Without Purchase',
    'Klik Pencarian': 'Search Clicks',
    'Suka': 'Likes',
    'Pengunjung Produk (Menambahkan Produk ke Keranjang)': 'Product Visitors (Added to Cart)',
    'Dimasukkan ke Keranjang (Produk)': 'Added to Cart (Products)',
    'Total Pembeli (Pesanan Dibuat)': 'Total Buyers (Orders Created)',
    'Produk (Pesanan Dibuat)': 'Products (Orders Created)',
    'Produk Dipesan': 'Products Ordered',
    'Total Pembeli (Pesanan Siap Dikirim)': 'Total Buyers (Orders Ready to Ship)',
    'Produk (Pesanan Siap Dikirim)': 'Products (Orders Ready to Ship)',
    'Produk Siap Dikirim': 'Products Ready to Ship',
    
    # Sales
    'Penjualan (Pesanan Dibuat) (IDR)': 'Total Sales (Orders Created) (IDR)',
    'Penjualan (Pesanan Siap Dikirim) (IDR)': 'Sales (Orders Ready to Ship) (IDR)',
    'Pesanan (Pesanan Dibuat)': 'Orders (Orders Created)',
    'Pesanan (Pesanan Siap Dikirim)': 'Orders (Orders Ready to Ship)',
    
    # Conversion Rates
    'Tingkat Konversi Pesanan (Pesanan Dibuat)': 'Order Conversion Rate (Orders Created)',
    'Tingkat Konversi Pesanan (Pesanan Siap Dikirim)': 'Order Conversion Rate (Orders Ready to Ship)',
    'Tingkat Konversi Pesanan (Pesanan Siap Dikirim ÷ Pesanan Dibuat)': 'Order Conversion Rate (Orders Ready to Ship ÷ Orders Created)',
    
    # PayLater
    'Tenor': 'Tenor',
    'Biaya Layanan yang Dikenakan (Pesanan Dibuat)': 'Service_Fee_Orders_Created',
    'Biaya Layanan yang Dikenakan (Pesanan Siap Dikirim)': 'Service_Fee_Ready_To_Ship',
    'ROI (Pesanan Dibuat)': 'ROI_Orders_Created',
    'ROI (Pesanan Siap Dikirim)': 'ROI_Ready_To_Ship',
    
    # Chat
    'Pengunjung': 'Visitors',
    'Jumlah Chat': 'Number_Of_Chats',
    'Pengunjung Bertanya': 'Visitors_Asking',
    'Pertanyaan Diajukan': 'Questions_Asked',
    'Chat Dibalas': 'Chats_Replied',
    'Chat Tidak Dibalas': 'Chats_Not_Replied',
    'Waktu Respons Rata-rata': 'Average_Response_Time',
    'Persentase CSAT': 'CSAT_Percent',
    'Waktu Respons Chat Pertama': 'First_Chat_Response_Time',
    'Tingkat Konversi (Chat Direspons)': 'Conversion_Rate_Chats_Responded',
    'Total Pembeli': 'Total_Buyers',
    'Total Pesanan': 'Total_Orders',
    'Produk': 'Products',
    'Penjualan (IDR)': 'Sales_IDR',
    'Tingkat Konversi (Chat Dibalas)': 'Conversion_Rate_Chats_Replied',
    
    # Off-Platform
    'Platform': 'Platform',
    'Saluran': 'Channel',
    'Kunjungan': 'Visits',
    'Pembeli Baru': 'New_Buyers',
    'Tingkat Konversi (Pesanan per Kunjungan)': 'Conversion_Rate_Orders_Per_Visit',
    'Pengguna Menambahkan ke Keranjang': 'Users_Added_To_Cart',
    'Nilai Produk Ditambahkan ke Keranjang (IDR)': 'Value_Products_Added_To_Cart_IDR',
    'Produk Ditambahkan ke Keranjang': 'Products_Added_To_Cart',
    'Tingkat Konversi (Kunjungan ke Keranjang)': 'Conversion_Rate_Visit_To_Cart',
    'Tingkat Konversi (Keranjang ke Pesanan)': 'Conversion_Rate_Cart_To_Order',
    
    # Mass Chat
    'Penerima Sebenarnya': 'Actual_Recipients',
    'Penerima Membaca': 'Recipients_Read',
    'Penerima Mengklik': 'Recipients_Clicked',
    'Penerima Memblokir': 'Recipients_Blocked',
    'Pesanan': 'Orders',
    'Pembeli': 'Buyers',
    'Tingkat Baca': 'Read_Rate',
    'Tingkat Klik': 'Click_Rate',
    'Tingkat Konversi (Merespons ke Ditempatkan)': 'Conversion_Rate_Respond_To_Placed',
    
    # Campaigns
    'Tingkat Klik': 'Click_Rate',
    'Jumlah Produk Dilihat': 'Number_Of_Products_Viewed',
    'Produk Diklik': 'Products_Clicked',
    'Penjualan per Pembeli (Pesanan Dibuat) (IDR)': 'Sales_Per_Buyer_Orders_Created_IDR',
    'Penjualan per Pembeli (Pesanan Siap Dikirim) (IDR)': 'Sales_Per_Buyer_Ready_To_Ship_IDR',
}

def clean_column_name(col):
    """Clean and translate column names"""
    # Remove extra spaces
    col = ' '.join(col.split())
    
    # Try direct translation first
    if col in TRANSLATIONS:
        return TRANSLATIONS[col]
    
    # Additional common translations
    common_translations = {
        # Traffic
        'Produk Dilihat': 'Products_Viewed',
        'Produk_Dilihat': 'Products_Viewed',
        'Rata-rata Dilihat': 'Average_Views',
        'Rata_rata_Dilihat': 'Average_Views',
        'Rata-rata Waktu Dihabiskan': 'Average_Time_Spent',
        'Rata_rata_Waktu_Dihabiskan': 'Average_Time_Spent',
        'Tingkat Pengunjung Melihat Tanpa Membeli': 'Rate_Visitors_Viewing_Without_Buying',
        'Tingkat_Pengunjung_Melihat_Tanpa_Membeli': 'Rate_Visitors_Viewing_Without_Buying',
        'Total Pengunjung': 'Total_Visitors',
        'Total_Pengunjung': 'Total_Visitors',
        'Pengunjung Baru': 'New_Visitors',
        'Pengunjung_Baru': 'New_Visitors',
        'Pengunjung Lama': 'Returning_Visitors',
        'Pengunjung_Lama': 'Returning_Visitors',
        'Jumlah Pengikut Baru': 'New_Followers',
        'Jumlah_Pengikut_Baru': 'New_Followers',
        
        # Chat
        'Periode Waktu': 'Time_Period',
        'Periode_Waktu': 'Time_Period',
        'Chat Belum Dibalas': 'Chats_Not_Replied',
        'Chat_Belum_Dibalas': 'Chats_Not_Replied',
        'Waktu Respon Rata-rata': 'Average_Response_Time',
        'Waktu_Respon_Rata_rata': 'Average_Response_Time',
        'CSAT %': 'CSAT_Percent',
        'Waktu Respon Chat Pertama Kali': 'First_Chat_Response_Time',
        'Waktu_Respon_Chat_Pertama_Kali': 'First_Chat_Response_Time',
        'Tingkat Konversi (Jumlah Chat yang Direspon)': 'Conversion_Rate_Chats_Responded',
        'Tingkat_Konversi_Jumlah_Chat_yang_Direspon': 'Conversion_Rate_Chats_Responded',
        
        # Product
        'Tingkat Konversi (Produk Dimasukkan ke Keranjang)': 'Product_Add_to_Cart_Conversion_Rate',
        'Tingkat_Konversi_Produk_Dimasukkan_ke_Keranjang': 'Product_Add_to_Cart_Conversion_Rate',
        'Total Penjualan (Pesanan Dibuat) (IDR)': 'Total_Sales_Orders_Created_IDR',
        'Total_Penjualan_Pesanan_Dibuat_IDR': 'Total_Sales_Orders_Created_IDR',
        'Tingkat Konversi (Pesanan yang Dibuat)': 'Order_Conversion_Rate_Orders_Created',
        'Tingkat_Konversi_Pesanan_yang_Dibuat': 'Order_Conversion_Rate_Orders_Created',
        'Tingkat Konversi (Pesanan Siap Dikirim)': 'Order_Conversion_Rate_Orders_Ready_to_Ship',
        'Tingkat_Konversi_Pesanan_Siap_Dikirim': 'Order_Conversion_Rate_Orders_Ready_to_Ship',
        'Tingkat Konversi (Pesanan Siap Dikirim ÷ Pesanan Dibuat)': 'Order_Conversion_Rate_Orders_Ready_to_Ship_÷_Orders_Created',
        'Tingkat_Konversi_Pesanan_Siap_Dikirim_dibagi_Pesanan_Dibuat': 'Order_Conversion_Rate_Orders_Ready_to_Ship_÷_Orders_Created',
    }
    
    if col in common_translations:
        return common_translations[col]
    
    # Clean up common patterns
    col = col.replace('(', '').replace(')', '').replace('/', '_')
    col = col.replace(' ', '_')
    col = col.replace('-', '_')
    col = col.replace('__', '_')
    
    return col

def clean_numeric_value(value):
    """Clean numeric values - handle European format"""
    if pd.isna(value):
        return np.nan
    
    if isinstance(value, (int, float)):
        return float(value)
    
    value_str = str(value).strip()
    
    # Remove spaces
    value_str = value_str.replace(' ', '')
    
    # Handle European format (1.234,56)
    if '.' in value_str and ',' in value_str:
        value_str = value_str.replace('.', '').replace(',', '.')
    # Handle thousands separator (1.234)
    elif '.' in value_str and re.match(r'^\d{1,3}(\.\d{3})+$', value_str):
        value_str = value_str.replace('.', '')
    # Handle decimal comma (1,5)
    elif ',' in value_str:
        value_str = value_str.replace(',', '.')
    
    try:
        return float(value_str)
    except:
        return np.nan

def process_excel_file(file_path, category):
    """Process a single Excel file"""
    try:
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Skip if empty
        if df.empty:
            return None
        
        # Clean column names
        df.columns = [clean_column_name(col) for col in df.columns]
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Remove header rows that repeat column names
        for col in df.columns:
            if col in df.columns:
                df = df[df[col] != col]
        
        # Convert numeric columns
        for col in df.columns:
            if col not in ['Date', 'Data_Period', 'Time_Period', 'Platform', 'Channel', 'Tenor']:
                df[col] = df[col].apply(clean_numeric_value)
        
        # Add metadata
        df['Source_File'] = Path(file_path).name
        df['Category'] = category
        df['Processed_Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return df
        
    except Exception as e:
        print(f"  ❌ Error processing {Path(file_path).name}: {str(e)}")
        return None

def process_category(raw_path, category_folder, output_name):
    """Process all files in a category"""
    print(f"\n{'='*60}")
    print(f"Processing: {category_folder}")
    print(f"{'='*60}")
    
    category_path = raw_path / category_folder
    
    if not category_path.exists():
        print(f"  ⚠️  Folder not found: {category_folder}")
        return None
    
    # Get all Excel files
    excel_files = list(category_path.glob('*.xlsx')) + list(category_path.glob('*.xls'))
    
    if not excel_files:
        print(f"  ⚠️  No Excel files found")
        return None
    
    print(f"  Found {len(excel_files)} files")
    
    # Process each file
    dfs = []
    for file_path in excel_files:
        print(f"  Processing: {file_path.name}")
        df = process_excel_file(file_path, category_folder)
        if df is not None:
            dfs.append(df)
            print(f"    ✅ {len(df)} rows extracted")
    
    if not dfs:
        print(f"  ❌ No data extracted")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by date if available
    if 'Date' in combined_df.columns:
        combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
        combined_df = combined_df.sort_values('Date')
    elif 'Data_Period' in combined_df.columns:
        combined_df = combined_df.sort_values('Data_Period')
    
    print(f"\n  ✅ Combined: {len(combined_df)} total rows")
    print(f"  Columns: {len(combined_df.columns)}")
    
    return combined_df

def main():
    """Main processing pipeline"""
    print("="*60)
    print("COMPREHENSIVE DATA CLEANING & TRANSLATION PIPELINE")
    print("="*60)
    print("\nProcessing original raw Indonesian data...")
    print("Cleaning, translating, and preparing for analysis")
    print("="*60)
    
    # Paths
    raw_path = Path("/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/data/raw")
    output_path = Path("/Users/tarang/CascadeProjects/windsurf-project/shopee-analytics-platform/data/processed")
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Categories to process
    categories = [
        ('chat data', 'chat_data_processed.csv'),
        ('traffic overview', 'traffic_overview_processed.csv'),
        ('product overview', 'product_overview_processed.csv'),
        ('flash sale', 'flash_sale_processed.csv'),
        ('voucher', 'voucher_processed.csv'),
        ('game', 'game_processed.csv'),
        ('live', 'live_processed.csv'),
        ('mass chat data', 'mass_chat_data_processed.csv'),
        ('off platform', 'off_platform_processed.csv'),
        ('shopee paylater', 'shopee_paylater_processed.csv'),
    ]
    
    # Process each category
    results = {}
    for category_folder, output_name in categories:
        df = process_category(raw_path, category_folder, output_name)
        if df is not None:
            # Save to CSV
            output_file = output_path / output_name
            df.to_csv(output_file, index=False)
            print(f"  💾 Saved to: {output_name}")
            results[category_folder] = len(df)
    
    # Summary
    print("\n" + "="*60)
    print("PROCESSING COMPLETE")
    print("="*60)
    print(f"\nTotal categories processed: {len(results)}")
    print(f"\nRows per category:")
    for category, rows in results.items():
        print(f"  • {category}: {rows:,} rows")
    print(f"\nTotal rows: {sum(results.values()):,}")
    print(f"\nOutput location: {output_path}")
    print("="*60)

if __name__ == "__main__":
    main()
