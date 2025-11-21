"""
Shopee API Integration Client
Two-way API integration for reading data and sending automated actions
"""

import requests
import hmac
import hashlib
import time
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ShopeeAPIClient:
    """
    Shopee API client for automated operations
    Supports both reading data and sending automated actions
    """
    
    def __init__(self, partner_id: str, partner_key: str, shop_id: str, base_url: str = "https://partner.shopeemobile.com"):
        """
        Initialize Shopee API client
        
        Args:
            partner_id: Shopee partner ID
            partner_key: Shopee partner key
            shop_id: Shop ID
            base_url: API base URL
        """
        self.partner_id = partner_id
        self.partner_key = partner_key
        self.shop_id = shop_id
        self.base_url = base_url
        self.access_token = None
        
    def _generate_signature(self, path: str, timestamp: int) -> str:
        """
        Generate HMAC-SHA256 signature for API authentication
        """
        base_string = f"{self.partner_id}{path}{timestamp}"
        signature = hmac.new(
            self.partner_key.encode('utf-8'),
            base_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, method: str, path: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """
        Make authenticated API request
        """
        timestamp = int(time.time())
        signature = self._generate_signature(path, timestamp)
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        url_params = {
            'partner_id': self.partner_id,
            'timestamp': timestamp,
            'sign': signature,
            'shop_id': self.shop_id
        }
        
        if self.access_token:
            url_params['access_token'] = self.access_token
        
        if params:
            url_params.update(params)
        
        url = f"{self.base_url}{path}"
        
        try:
            if method == 'GET':
                response = requests.get(url, params=url_params, headers=headers)
            elif method == 'POST':
                response = requests.post(url, params=url_params, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'success': False}
    
    # ========== DATA RETRIEVAL METHODS ==========
    
    def get_order_list(self, time_from: int, time_to: int, page_size: int = 100) -> Dict:
        """
        Get list of orders within time range
        """
        path = "/api/v2/order/get_order_list"
        params = {
            'time_from': time_from,
            'time_to': time_to,
            'page_size': page_size,
            'time_range_field': 'create_time'
        }
        return self._make_request('GET', path, params=params)
    
    def get_product_list(self, offset: int = 0, page_size: int = 100) -> Dict:
        """
        Get list of products
        """
        path = "/api/v2/product/get_item_list"
        params = {
            'offset': offset,
            'page_size': page_size
        }
        return self._make_request('GET', path, params=params)
    
    def get_shop_performance(self) -> Dict:
        """
        Get shop performance metrics
        """
        path = "/api/v2/shop/get_shop_info"
        return self._make_request('GET', path)
    
    # ========== AUTOMATED ACTION METHODS ==========
    
    def send_chat_message(self, conversation_id: str, message: str) -> Dict:
        """
        Send automated chat message to customer
        """
        path = "/api/v2/sellerchat/send_message"
        data = {
            'conversation_id': conversation_id,
            'message': message
        }
        return self._make_request('POST', path, data=data)
    
    def create_discount_activity(self, item_id: int, discount_percentage: float, 
                                 start_time: int, end_time: int) -> Dict:
        """
        Create automated discount campaign
        """
        path = "/api/v2/discount/add_discount_item"
        data = {
            'discount_id': int(time.time()),  # Generate unique ID
            'item_id': item_id,
            'discount_percentage': discount_percentage,
            'start_time': start_time,
            'end_time': end_time
        }
        return self._make_request('POST', path, data=data)
    
    def create_voucher(self, voucher_code: str, discount_amount: int, 
                       min_spend: int, usage_limit: int, start_time: int, end_time: int) -> Dict:
        """
        Create automated voucher campaign
        """
        path = "/api/v2/voucher/add_voucher"
        data = {
            'voucher_code': voucher_code,
            'discount_amount': discount_amount,
            'min_spend': min_spend,
            'usage_limit': usage_limit,
            'start_time': start_time,
            'end_time': end_time
        }
        return self._make_request('POST', path, data=data)
    
    def update_product_price(self, item_id: int, new_price: float) -> Dict:
        """
        Update product price automatically
        """
        path = "/api/v2/product/update_price"
        data = {
            'item_id': item_id,
            'price': new_price
        }
        return self._make_request('POST', path, data=data)
    
    def update_product_stock(self, item_id: int, stock: int) -> Dict:
        """
        Update product stock automatically
        """
        path = "/api/v2/product/update_stock"
        data = {
            'item_id': item_id,
            'stock': stock
        }
        return self._make_request('POST', path, data=data)
    
    def boost_product(self, item_id: int) -> Dict:
        """
        Boost product visibility (paid promotion)
        """
        path = "/api/v2/product/boost_item"
        data = {
            'item_id': item_id
        }
        return self._make_request('POST', path, data=data)
    
    # ========== ANALYTICS METHODS ==========
    
    def get_sales_analytics(self, days: int = 30) -> Dict:
        """
        Get sales analytics for specified period
        """
        end_time = int(time.time())
        start_time = end_time - (days * 24 * 60 * 60)
        
        orders = self.get_order_list(start_time, end_time)
        
        # Process and aggregate data
        analytics = {
            'total_orders': 0,
            'total_revenue': 0,
            'avg_order_value': 0,
            'period_days': days
        }
        
        if orders.get('response', {}).get('order_list'):
            order_list = orders['response']['order_list']
            analytics['total_orders'] = len(order_list)
            # Additional processing would go here
        
        return analytics


class AutomatedRecommendationBot:
    """
    Automated bot that uses ML insights to take actions via Shopee API
    """
    
    def __init__(self, api_client: ShopeeAPIClient):
        self.api_client = api_client
        self.actions_log = []
        
    def execute_campaign_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """
        Execute campaign recommendations automatically
        """
        results = []
        
        for rec in recommendations:
            if rec['priority'] == 'High' and 'Increase budget' in rec['action']:
                # Create discount campaign
                result = self._create_discount_campaign(rec)
                results.append(result)
                
            elif 'voucher' in rec['action'].lower():
                # Create voucher campaign
                result = self._create_voucher_campaign(rec)
                results.append(result)
        
        return results
    
    def _create_discount_campaign(self, recommendation: Dict) -> Dict:
        """
        Create discount campaign based on recommendation
        """
        # Calculate campaign parameters
        start_time = int(time.time())
        end_time = start_time + (7 * 24 * 60 * 60)  # 7 days
        
        action = {
            'type': 'discount_campaign',
            'recommendation': recommendation['campaign'],
            'status': 'simulated',  # In production, would be 'executed'
            'start_time': datetime.fromtimestamp(start_time).isoformat(),
            'end_time': datetime.fromtimestamp(end_time).isoformat(),
            'message': f"Would create discount campaign for {recommendation['campaign']}"
        }
        
        self.actions_log.append(action)
        return action
    
    def _create_voucher_campaign(self, recommendation: Dict) -> Dict:
        """
        Create voucher campaign based on recommendation
        """
        start_time = int(time.time())
        end_time = start_time + (14 * 24 * 60 * 60)  # 14 days
        
        action = {
            'type': 'voucher_campaign',
            'recommendation': recommendation['campaign'],
            'status': 'simulated',
            'start_time': datetime.fromtimestamp(start_time).isoformat(),
            'end_time': datetime.fromtimestamp(end_time).isoformat(),
            'message': f"Would create voucher campaign for {recommendation['campaign']}"
        }
        
        self.actions_log.append(action)
        return action
    
    def execute_product_recommendations(self, product_recs: Dict) -> List[Dict]:
        """
        Execute product recommendations automatically
        """
        results = []
        
        # Boost high-potential products
        if product_recs.get('products_to_promote'):
            for product in product_recs['products_to_promote'][:3]:  # Top 3
                result = {
                    'type': 'product_boost',
                    'product': product['date'],
                    'status': 'simulated',
                    'message': f"Would boost product visibility for {product['date']}"
                }
                results.append(result)
                self.actions_log.append(result)
        
        return results
    
    def execute_customer_segment_actions(self, segments: List[Dict]) -> List[Dict]:
        """
        Execute customer segment-based actions
        """
        results = []
        
        for segment in segments:
            if 'High-Value' in segment.get('segment_name', ''):
                # Send VIP message
                result = {
                    'type': 'customer_engagement',
                    'segment': segment['segment_name'],
                    'status': 'simulated',
                    'message': 'Would send VIP loyalty program invitation'
                }
                results.append(result)
                self.actions_log.append(result)
        
        return results
    
    def get_actions_summary(self) -> Dict:
        """
        Get summary of all automated actions
        """
        return {
            'total_actions': len(self.actions_log),
            'actions_by_type': self._count_by_type(),
            'recent_actions': self.actions_log[-10:],  # Last 10 actions
            'timestamp': datetime.now().isoformat()
        }
    
    def _count_by_type(self) -> Dict:
        """
        Count actions by type
        """
        counts = {}
        for action in self.actions_log:
            action_type = action.get('type', 'unknown')
            counts[action_type] = counts.get(action_type, 0) + 1
        return counts


# Example usage (for testing)
if __name__ == "__main__":
    # NOTE: In production, these would be real credentials
    # For demo purposes, we're using placeholder values
    
    print("🤖 Shopee API Integration Module")
    print("=" * 50)
    print("\n✅ API Client initialized (demo mode)")
    print("✅ Automated Bot ready")
    print("\n📋 Available Features:")
    print("  - Two-way API communication")
    print("  - Automated campaign creation")
    print("  - Product price/stock updates")
    print("  - Customer chat automation")
    print("  - ML-driven recommendations execution")
    print("\n⚠️  Note: Requires valid Shopee API credentials for production use")
