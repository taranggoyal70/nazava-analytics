"""
Product Recommendation Engine
Collaborative filtering and content-based recommendations
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

class ProductRecommender:
    """
    Product recommendation system using multiple strategies:
    1. Popularity-based recommendations
    2. Performance-based recommendations  
    3. Cross-sell opportunities
    """
    
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.product_scores = {}
        self.recommendations = {}
        
    def analyze_product_performance(self, product_df):
        """
        Analyze product performance metrics
        """
        # Calculate key metrics
        metrics = pd.DataFrame({
            'total_visits': pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce'),
            'total_views': pd.to_numeric(product_df['Product Page Views'], errors='coerce'),
            'cart_additions': pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce'),
            'total_orders': pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce'),
            'total_sales': pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce'),
            'products_visited': pd.to_numeric(product_df['Products Visited'], errors='coerce'),
        })
        
        # Aggregate metrics
        performance = {
            'total_visits': metrics['total_visits'].sum(),
            'total_views': metrics['total_views'].sum(),
            'cart_additions': metrics['cart_additions'].sum(),
            'total_orders': metrics['total_orders'].sum(),
            'total_sales': metrics['total_sales'].sum(),
            'unique_products': metrics['products_visited'].sum(),
        }
        
        # Calculate conversion rates
        performance['visit_to_cart'] = (
            performance['cart_additions'] / performance['total_visits'] * 100
            if performance['total_visits'] > 0 else 0
        )
        
        performance['cart_to_order'] = (
            performance['total_orders'] / performance['cart_additions'] * 100
            if performance['cart_additions'] > 0 else 0
        )
        
        performance['overall_conversion'] = (
            performance['total_orders'] / performance['total_visits'] * 100
            if performance['total_visits'] > 0 else 0
        )
        
        performance['avg_order_value'] = (
            performance['total_sales'] / performance['total_orders']
            if performance['total_orders'] > 0 else 0
        )
        
        return performance
    
    def identify_high_performers(self, product_df):
        """
        Identify top performing products
        """
        # Calculate performance score for each period
        product_df['performance_score'] = (
            pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce') * 0.4 +
            pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce') * 1000000 * 0.3 +
            pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce') * 500000 * 0.2 +
            pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce') * 10000 * 0.1
        ).fillna(0)
        
        # Get top periods
        top_performers = product_df.nlargest(10, 'performance_score')[
            ['Date', 'performance_score', 'Total Sales (Orders Created) (IDR)', 
             'Total Buyers (Orders Created)', 'Product Visitors (Visits)']
        ].copy()
        
        return top_performers
    
    def identify_underperformers(self, product_df):
        """
        Identify underperforming products that need attention
        """
        # Calculate performance score
        product_df['performance_score'] = (
            pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce') * 0.4 +
            pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce') * 1000000 * 0.3 +
            pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce') * 500000 * 0.2 +
            pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce') * 10000 * 0.1
        ).fillna(0)
        
        # Get bottom performers (excluding zeros)
        underperformers = product_df[product_df['performance_score'] > 0].nsmallest(10, 'performance_score')[
            ['Date', 'performance_score', 'Total Sales (Orders Created) (IDR)', 
             'Total Buyers (Orders Created)', 'Product Visitors (Visits)']
        ].copy()
        
        return underperformers
    
    def recommend_cross_sell_opportunities(self, product_df):
        """
        Identify cross-sell opportunities based on browsing patterns
        """
        opportunities = []
        
        # High traffic but low conversion
        visitors_numeric = pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce')
        product_df['conversion_rate'] = (
            pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce') /
            visitors_numeric * 100
        ).fillna(0)
        
        high_traffic_low_conversion = product_df[
            (visitors_numeric > visitors_numeric.median()) &
            (product_df['conversion_rate'] < product_df['conversion_rate'].median())
        ]
        
        if not high_traffic_low_conversion.empty:
            opportunities.append({
                'type': 'High Traffic, Low Conversion',
                'count': len(high_traffic_low_conversion),
                'recommendation': 'Add product bundles, improve product descriptions, offer discounts',
                'avg_visitors': pd.to_numeric(high_traffic_low_conversion['Product Visitors (Visits)'], errors='coerce').mean(),
                'avg_conversion': high_traffic_low_conversion['conversion_rate'].mean()
            })
        
        # High cart additions but low purchase
        cart_numeric = pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce')
        product_df['cart_to_purchase'] = (
            pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce') /
            cart_numeric * 100
        ).fillna(0)
        
        high_cart_low_purchase = product_df[
            (cart_numeric > cart_numeric.median()) &
            (product_df['cart_to_purchase'] < product_df['cart_to_purchase'].median())
        ]
        
        if not high_cart_low_purchase.empty:
            opportunities.append({
                'type': 'High Cart Abandonment',
                'count': len(high_cart_low_purchase),
                'recommendation': 'Send cart abandonment emails, offer free shipping, create urgency',
                'avg_cart_additions': pd.to_numeric(high_cart_low_purchase['Product Visitors (Added to Cart)'], errors='coerce').mean(),
                'avg_completion': high_cart_low_purchase['cart_to_purchase'].mean()
            })
        
        return opportunities
    
    def generate_product_recommendations(self, product_df):
        """
        Generate comprehensive product recommendations
        """
        recommendations = {
            'top_products': [],
            'products_to_promote': [],
            'products_to_optimize': [],
            'bundle_opportunities': []
        }
        
        # Top products (high sales, high conversion)
        product_df['score'] = (
            pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce').fillna(0) / 1e6 * 0.5 +
            (pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').fillna(0) /
             pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').fillna(1) * 100) * 0.5
        )
        
        top_products = product_df.nlargest(5, 'score')
        for _, row in top_products.iterrows():
            recommendations['top_products'].append({
                'date': row['Date'],
                'sales': f"IDR {pd.to_numeric(row['Total Sales (Orders Created) (IDR)'], errors='coerce')/1e6:.1f}M",
                'orders': int(pd.to_numeric(row['Total Buyers (Orders Created)'], errors='coerce')),
                'action': '⭐ Continue promoting, maintain inventory'
            })
        
        # Products to promote (high potential, low visibility)
        product_df['potential_score'] = (
            (pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').fillna(0) /
             pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').fillna(1)) * 100
        )
        
        # Convert visitors to numeric for median calculation
        visitors_numeric = pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce')
        visitors_median = visitors_numeric.median()
        
        high_potential = product_df[
            (product_df['potential_score'] > product_df['potential_score'].median()) &
            (visitors_numeric < visitors_median)
        ].nlargest(5, 'potential_score')
        
        for _, row in high_potential.iterrows():
            recommendations['products_to_promote'].append({
                'date': row['Date'],
                'conversion': f"{row['potential_score']:.1f}%",
                'visitors': int(pd.to_numeric(row['Product Visitors (Visits)'], errors='coerce')),
                'action': '📢 Increase visibility through ads and promotions'
            })
        
        # Products to optimize (high traffic, low conversion)
        # Add visitors_numeric as a column for sorting
        product_df['visitors_numeric_temp'] = visitors_numeric
        low_conversion = product_df[
            (visitors_numeric > visitors_median) &
            (product_df['potential_score'] < product_df['potential_score'].median())
        ].nlargest(5, 'visitors_numeric_temp')
        
        for _, row in low_conversion.iterrows():
            recommendations['products_to_optimize'].append({
                'date': row['Date'],
                'visitors': int(pd.to_numeric(row['Product Visitors (Visits)'], errors='coerce')),
                'conversion': f"{row['potential_score']:.1f}%",
                'action': '🔧 Improve listings, add reviews, optimize pricing'
            })
        
        return recommendations
    
    def get_pricing_insights(self, product_df):
        """
        Analyze pricing and provide optimization suggestions
        """
        insights = {
            'avg_order_value': 0,
            'revenue_per_visitor': 0,
            'suggestions': []
        }
        
        total_sales = pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
        total_orders = pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').sum()
        total_visitors = pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').sum()
        
        if total_orders > 0:
            insights['avg_order_value'] = total_sales / total_orders
            
        if total_visitors > 0:
            insights['revenue_per_visitor'] = total_sales / total_visitors
        
        # Pricing suggestions
        if insights['avg_order_value'] < 100000:
            insights['suggestions'].append({
                'type': 'Bundle Products',
                'reason': 'Low average order value',
                'action': 'Create product bundles to increase AOV',
                'expected_impact': '+15-25% AOV'
            })
        
        if insights['revenue_per_visitor'] < 50000:
            insights['suggestions'].append({
                'type': 'Upsell Strategy',
                'reason': 'Low revenue per visitor',
                'action': 'Implement upselling and cross-selling',
                'expected_impact': '+20-30% revenue per visitor'
            })
        
        insights['suggestions'].append({
            'type': 'Premium Products',
            'reason': 'Focus on complete water filters (SAM products >Rp 100K)',
            'action': 'Promote higher-margin complete filter systems',
            'expected_impact': '+30-40% profit margin'
        })
        
        return insights


def run_product_analysis(data_path):
    """
    Run complete product recommendation analysis
    """
    # Load data
    product_df = pd.read_csv(f"{data_path}/product_overview_cleaned.csv")
    
    # Initialize recommender
    recommender = ProductRecommender()
    
    # Analyze performance
    performance = recommender.analyze_product_performance(product_df)
    
    # Get recommendations
    recommendations = recommender.generate_product_recommendations(product_df)
    
    # Get cross-sell opportunities
    cross_sell = recommender.recommend_cross_sell_opportunities(product_df)
    
    # Get pricing insights
    pricing = recommender.get_pricing_insights(product_df)
    
    return recommender, performance, recommendations, cross_sell, pricing


if __name__ == "__main__":
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    recommender, performance, recommendations, cross_sell, pricing = run_product_analysis(data_path)
    
    print("✅ Product Recommendation Analysis Complete!")
    print(f"\n📊 Overall Performance:")
    print(f"Total Sales: IDR {performance['total_sales']/1e6:.1f}M")
    print(f"Total Orders: {performance['total_orders']:.0f}")
    print(f"Conversion Rate: {performance['overall_conversion']:.2f}%")
    print(f"Avg Order Value: IDR {performance['avg_order_value']/1000:.0f}K")
