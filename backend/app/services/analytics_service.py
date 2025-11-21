"""
Analytics Service - Business logic for analytics operations
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.analytics import KPIResponse, TrendResponse, FunnelResponse


class AnalyticsService:
    """Service for analytics operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.data_path = settings.DATA_PATH
        self._load_data()
    
    def _load_data(self):
        """Load cleaned CSV data"""
        self.chat_data = pd.read_csv(f"{self.data_path}/chat_data_cleaned.csv")
        self.traffic_data = pd.read_csv(f"{self.data_path}/traffic_overview_cleaned.csv")
        self.flash_sale_data = pd.read_csv(f"{self.data_path}/flash_sale_cleaned.csv")
        self.product_data = pd.read_csv(f"{self.data_path}/product_overview_cleaned.csv")
        self.off_platform_data = pd.read_csv(f"{self.data_path}/off_platform_cleaned.csv")
        
        # Convert date columns
        if 'Date' in self.traffic_data.columns:
            self.traffic_data['Date'] = pd.to_datetime(self.traffic_data['Date'])
        if 'Date' in self.product_data.columns:
            self.product_data['Date'] = pd.to_datetime(self.product_data['Date'])
        if 'Date' in self.off_platform_data.columns:
            self.off_platform_data['Date'] = pd.to_datetime(self.off_platform_data['Date'])
    
    async def get_kpis(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> KPIResponse:
        """Calculate key performance indicators"""
        
        # Calculate total sales from multiple sources
        total_sales = 0
        if 'Sales_IDR' in self.chat_data.columns:
            total_sales += self.chat_data['Sales_IDR'].sum()
        if 'Sales_Ready_To_Ship_IDR' in self.flash_sale_data.columns:
            total_sales += self.flash_sale_data['Sales_Ready_To_Ship_IDR'].sum()
        
        # Total orders
        total_orders = 0
        if 'Total_Orders' in self.chat_data.columns:
            total_orders += self.chat_data['Total_Orders'].sum()
        if 'Orders_Ready_To_Ship' in self.flash_sale_data.columns:
            total_orders += self.flash_sale_data['Orders_Ready_To_Ship'].sum()
        
        # Total visitors
        total_visitors = 0
        if 'Total_Visitors' in self.traffic_data.columns:
            total_visitors = self.traffic_data['Total_Visitors'].sum()
        
        # Conversion rate (orders / visitors)
        conversion_rate = (total_orders / total_visitors) if total_visitors > 0 else 0
        
        # Average order value
        avg_order_value = (total_sales / total_orders) if total_orders > 0 else 0
        
        # Customer satisfaction
        customer_satisfaction = 0
        if 'CSAT_Percent' in self.chat_data.columns:
            customer_satisfaction = self.chat_data['CSAT_Percent'].mean()
        
        return KPIResponse(
            total_sales=float(total_sales),
            total_orders=int(total_orders),
            total_visitors=int(total_visitors),
            conversion_rate=float(conversion_rate),
            average_order_value=float(avg_order_value),
            customer_satisfaction=float(customer_satisfaction),
            period="all_time"
        )
    
    async def get_trend(self, metric: str, category: Optional[str] = None, period: str = "daily"):
        """Get trend data for a metric"""
        
        if metric == "traffic" and 'Date' in self.traffic_data.columns:
            df = self.traffic_data.copy()
            df = df.sort_values('Date')
            
            trend_data = []
            for _, row in df.iterrows():
                trend_data.append({
                    "date": row['Date'].strftime('%Y-%m-%d'),
                    "value": float(row.get('Total_Visitors', 0))
                })
            
            # Calculate trend direction
            if len(trend_data) > 1:
                first_val = trend_data[0]['value']
                last_val = trend_data[-1]['value']
                change_pct = ((last_val - first_val) / first_val * 100) if first_val > 0 else 0
                
                if change_pct > 5:
                    direction = "up"
                elif change_pct < -5:
                    direction = "down"
                else:
                    direction = "stable"
            else:
                direction = "stable"
                change_pct = 0
            
            return {
                "metric": metric,
                "data": trend_data,
                "period": period,
                "trend_direction": direction,
                "change_percentage": float(change_pct)
            }
        
        return {
            "metric": metric,
            "data": [],
            "period": period,
            "trend_direction": "stable",
            "change_percentage": 0.0
        }
    
    async def get_funnel(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Get conversion funnel data"""
        
        # Calculate funnel stages from product data
        if not self.product_data.empty:
            total_visitors = self.product_data['Product_Visitors_Visits'].sum()
            added_to_cart = self.product_data['Product_Visitors_Adding_To_Cart'].sum()
            orders_created = self.product_data['Total_Buyers_Orders_Created'].sum()
            orders_shipped = self.product_data['Total_Buyers_Ready_To_Ship'].sum()
            
            stages = [
                {
                    "stage": "Visitors",
                    "count": int(total_visitors),
                    "percentage": 100.0,
                    "conversion_rate": None
                },
                {
                    "stage": "Added to Cart",
                    "count": int(added_to_cart),
                    "percentage": (added_to_cart / total_visitors * 100) if total_visitors > 0 else 0,
                    "conversion_rate": (added_to_cart / total_visitors) if total_visitors > 0 else 0
                },
                {
                    "stage": "Orders Created",
                    "count": int(orders_created),
                    "percentage": (orders_created / total_visitors * 100) if total_visitors > 0 else 0,
                    "conversion_rate": (orders_created / added_to_cart) if added_to_cart > 0 else 0
                },
                {
                    "stage": "Orders Shipped",
                    "count": int(orders_shipped),
                    "percentage": (orders_shipped / total_visitors * 100) if total_visitors > 0 else 0,
                    "conversion_rate": (orders_shipped / orders_created) if orders_created > 0 else 0
                }
            ]
            
            overall_conversion = (orders_shipped / total_visitors) if total_visitors > 0 else 0
            
            return {
                "stages": stages,
                "overall_conversion": float(overall_conversion)
            }
        
        return {"stages": [], "overall_conversion": 0.0}
    
    async def get_category_metrics(self):
        """Get metrics by category"""
        categories = []
        
        # Chat data metrics
        if not self.chat_data.empty:
            categories.append({
                "category": "Chat",
                "sales": float(self.chat_data['Sales_IDR'].sum()),
                "orders": int(self.chat_data['Total_Orders'].sum()),
                "conversion_rate": float(self.chat_data['Conversion_Rate_Chats_Replied'].mean()),
                "avg_order_value": float(self.chat_data['Sales_IDR'].sum() / self.chat_data['Total_Orders'].sum()) if self.chat_data['Total_Orders'].sum() > 0 else 0
            })
        
        # Flash sale metrics
        if not self.flash_sale_data.empty:
            total_sales = self.flash_sale_data['Sales_Ready_To_Ship_IDR'].sum()
            total_orders = self.flash_sale_data['Orders_Ready_To_Ship'].sum()
            
            categories.append({
                "category": "Flash Sale",
                "sales": float(total_sales),
                "orders": int(total_orders),
                "conversion_rate": float(self.flash_sale_data['Click_Rate'].mean()),
                "avg_order_value": float(total_sales / total_orders) if total_orders > 0 else 0
            })
        
        return categories
    
    async def get_traffic_sources(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Get traffic by source"""
        if 'Platform' in self.off_platform_data.columns:
            sources = self.off_platform_data.groupby('Platform').agg({
                'Visitors': 'sum',
                'Sales_IDR': 'sum',
                'Orders': 'sum'
            }).reset_index()
            
            return sources.to_dict('records')
        
        return []
    
    async def get_campaign_performance(self, campaign_type: Optional[str] = None):
        """Get campaign performance metrics"""
        campaigns = []
        
        # Flash sale performance
        if not self.flash_sale_data.empty:
            campaigns.append({
                "campaign_type": "Flash Sale",
                "total_sales": float(self.flash_sale_data['Sales_Ready_To_Ship_IDR'].sum()),
                "total_orders": int(self.flash_sale_data['Orders_Ready_To_Ship'].sum()),
                "click_rate": float(self.flash_sale_data['Click_Rate'].mean()),
                "avg_order_value": float(self.flash_sale_data['Sales_Per_Buyer_Ready_To_Ship_IDR'].mean())
            })
        
        return campaigns
    
    async def get_top_products(self, limit: int = 10, metric: str = "sales"):
        """Get top performing products"""
        # This would require product-level data
        # For now, return placeholder
        return {
            "metric": metric,
            "products": [],
            "message": "Product-level data not available in current dataset"
        }
    
    async def get_customer_service_metrics(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        """Get customer service metrics"""
        if not self.chat_data.empty:
            return {
                "total_chats": int(self.chat_data['Number_Of_Chats'].sum()),
                "chats_replied": int(self.chat_data['Chats_Replied'].sum()),
                "chats_not_replied": int(self.chat_data['Chats_Not_Replied'].sum()),
                "avg_response_time_minutes": float(self.chat_data['Average_Response_Time'].mean()),
                "avg_csat": float(self.chat_data['CSAT_Percent'].mean()),
                "conversion_rate": float(self.chat_data['Conversion_Rate_Chats_Replied'].mean())
            }
        
        return {}
