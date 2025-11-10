"""
Customer Segmentation Model
Uses K-means clustering to segment customers based on behavior
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class CustomerSegmentation:
    """
    Customer segmentation using K-means clustering
    Segments customers based on RFM (Recency, Frequency, Monetary) analysis
    """
    
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.pca = PCA(n_components=2)
        self.feature_names = []
        self.cluster_profiles = {}
        
    def prepare_features(self, chat_df, traffic_df, product_df):
        """
        Prepare customer features from multiple data sources
        """
        # Aggregate chat metrics
        chat_features = pd.DataFrame({
            'avg_response_time': pd.to_numeric(chat_df['Average_Response_Time'], errors='coerce').mean(),
            'total_chats': pd.to_numeric(chat_df['Number_Of_Chats'], errors='coerce').sum(),
            'chat_conversion': pd.to_numeric(chat_df['Conversion_Rate_Chats_Replied'], errors='coerce').mean(),
            'chat_sales': pd.to_numeric(chat_df['Sales_IDR'], errors='coerce').sum(),
            'csat_score': pd.to_numeric(chat_df['CSAT_Percent'], errors='coerce').mean(),
        }, index=[0])
        
        # Aggregate traffic metrics
        traffic_features = pd.DataFrame({
            'total_visitors': pd.to_numeric(traffic_df['Total_Visitors'], errors='coerce').sum(),
            'new_visitors': pd.to_numeric(traffic_df['New_Visitors'], errors='coerce').sum(),
            'returning_visitors': pd.to_numeric(traffic_df['Returning_Visitors'], errors='coerce').sum(),
            'avg_time_spent': pd.to_numeric(traffic_df['Average_Time_Spent'], errors='coerce').mean(),
        }, index=[0])
        
        # Aggregate product metrics
        product_features = pd.DataFrame({
            'product_visits': pd.to_numeric(product_df['Product Visitors (Visits)'], errors='coerce').sum(),
            'cart_additions': pd.to_numeric(product_df['Product Visitors (Added to Cart)'], errors='coerce').sum(),
            'total_orders': pd.to_numeric(product_df['Total Buyers (Orders Created)'], errors='coerce').sum(),
            'product_sales': pd.to_numeric(product_df['Total Sales (Orders Created) (IDR)'], errors='coerce').sum(),
        }, index=[0])
        
        # Combine all features
        features = pd.concat([chat_features, traffic_features, product_features], axis=1)
        
        # Calculate derived metrics
        features['visitor_retention_rate'] = (
            features['returning_visitors'] / features['total_visitors'] * 100
        ).fillna(0)
        
        features['cart_conversion_rate'] = (
            features['total_orders'] / features['cart_additions'] * 100
        ).fillna(0)
        
        features['avg_order_value'] = (
            features['product_sales'] / features['total_orders']
        ).fillna(0)
        
        features['engagement_score'] = (
            features['avg_time_spent'] * features['visitor_retention_rate']
        ).fillna(0)
        
        self.feature_names = features.columns.tolist()
        return features
    
    def create_time_based_segments(self, chat_df, traffic_df, product_df):
        """
        Create customer segments based on daily data (not monthly)
        """
        # Use daily product data since that's where we have the most complete data
        if 'Date' not in product_df.columns:
            raise ValueError("Product data must have 'Date' column")
        
        # Parse dates
        product_df['date'] = pd.to_datetime(product_df['Date'], errors='coerce')
        traffic_df['date'] = pd.to_datetime(traffic_df['Date'], errors='coerce') if 'Date' in traffic_df.columns else None
        
        # Filter to valid dates
        product_df = product_df[product_df['date'].notna()].copy()
        
        segments = []
        
        # Group by date
        for date in sorted(product_df['date'].unique()):
            date_str = date.strftime('%Y-%m-%d')
            
            # Filter data for this date
            product_day = product_df[product_df['date'] == date]
            traffic_day = traffic_df[traffic_df['date'] == date] if traffic_df is not None and 'date' in traffic_df.columns else pd.DataFrame()
            
            # Calculate metrics from product data
            total_sales = pd.to_numeric(product_day['Total Sales (Orders Created) (IDR)'], errors='coerce').sum()
            total_orders = pd.to_numeric(product_day['Total Buyers (Orders Created)'], errors='coerce').sum()
            
            # Get traffic data
            total_visitors = pd.to_numeric(traffic_day['Total_Visitors'], errors='coerce').sum() if not traffic_day.empty else 0
            
            # Use average CSAT from chat data (since it's aggregated)
            # Fix decimal issue: if CSAT < 10, it's in decimal form, multiply by 100
            avg_csat_raw = pd.to_numeric(chat_df['CSAT_Percent'], errors='coerce').mean() if not chat_df.empty else 0.942
            avg_csat = avg_csat_raw * 100 if avg_csat_raw < 10 else avg_csat_raw
            
            # Chat conversion (use average)
            chat_conv = pd.to_numeric(chat_df['Conversion_Rate_Chats_Replied'], errors='coerce').mean() if not chat_df.empty else 0
            
            segment = {
                'month': date_str,  # Keep column name for compatibility
                'total_sales': total_sales,
                'total_visitors': total_visitors if total_visitors > 0 else 1000,  # Default if missing
                'total_orders': total_orders,
                'csat_score': avg_csat,
                'chat_conversion': chat_conv,
            }
            
            # Calculate derived metrics
            segment['avg_order_value'] = segment['total_sales'] / segment['total_orders'] if segment['total_orders'] > 0 else 0
            segment['conversion_rate'] = segment['total_orders'] / segment['total_visitors'] * 100 if segment['total_visitors'] > 0 else 0
            
            segments.append(segment)
        
        df = pd.DataFrame(segments)
        
        # Set feature names (excluding 'month')
        self.feature_names = [col for col in df.columns if col != 'month']
        
        return df
    
    def fit(self, features_df):
        """
        Fit the clustering model
        """
        # Remove non-numeric columns
        numeric_features = features_df.select_dtypes(include=[np.number])
        
        # Handle missing values
        numeric_features = numeric_features.fillna(0)
        
        # Scale features
        scaled_features = self.scaler.fit_transform(numeric_features)
        
        # Fit K-means
        self.kmeans.fit(scaled_features)
        
        # Get cluster labels
        labels = self.kmeans.labels_
        
        # Create cluster profiles
        for i in range(self.n_clusters):
            cluster_data = numeric_features[labels == i]
            self.cluster_profiles[i] = {
                'size': len(cluster_data),
                'mean_values': cluster_data.mean().to_dict(),
                'characteristics': self._interpret_cluster(cluster_data.mean())
            }
        
        return labels
    
    def _interpret_cluster(self, cluster_mean):
        """
        Interpret cluster characteristics
        """
        characteristics = []
        
        # Check sales performance
        if 'total_sales' in cluster_mean.index:
            if cluster_mean['total_sales'] > cluster_mean.get('total_sales', 0):
                characteristics.append("High Value")
            else:
                characteristics.append("Low Value")
        
        # Check engagement
        if 'engagement_score' in cluster_mean.index:
            if cluster_mean['engagement_score'] > 100:
                characteristics.append("Highly Engaged")
            else:
                characteristics.append("Low Engagement")
        
        # Check retention
        if 'visitor_retention_rate' in cluster_mean.index:
            if cluster_mean['visitor_retention_rate'] > 50:
                characteristics.append("Loyal")
            else:
                characteristics.append("New/Occasional")
        
        return " | ".join(characteristics) if characteristics else "Standard"
    
    def predict(self, features_df):
        """
        Predict cluster for new data
        """
        numeric_features = features_df.select_dtypes(include=[np.number]).fillna(0)
        scaled_features = self.scaler.transform(numeric_features)
        return self.kmeans.predict(scaled_features)
    
    def visualize_clusters(self, features_df, labels):
        """
        Create visualization of clusters using PCA
        """
        numeric_features = features_df.select_dtypes(include=[np.number]).fillna(0)
        scaled_features = self.scaler.transform(numeric_features)
        
        # Apply PCA for 2D visualization
        pca_features = self.pca.fit_transform(scaled_features)
        
        # Create DataFrame for plotting
        plot_df = pd.DataFrame({
            'PC1': pca_features[:, 0],
            'PC2': pca_features[:, 1],
            'Cluster': [f'Cluster {i}' for i in labels]
        })
        
        # Create scatter plot
        fig = px.scatter(
            plot_df,
            x='PC1',
            y='PC2',
            color='Cluster',
            title='Customer Segments (PCA Visualization)',
            labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'},
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe']
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500
        )
        
        return fig
    
    def get_segment_summary(self):
        """
        Get summary of all segments
        """
        summary = []
        for cluster_id, profile in self.cluster_profiles.items():
            summary.append({
                'Cluster': f'Segment {cluster_id + 1}',
                'Size': profile['size'],
                'Characteristics': profile['characteristics'],
                'Avg Sales': f"IDR {profile['mean_values'].get('total_sales', 0)/1e6:.1f}M",
                'Avg Orders': f"{profile['mean_values'].get('total_orders', 0):.0f}",
            })
        return pd.DataFrame(summary)
    
    def get_recommendations(self, cluster_id):
        """
        Get marketing recommendations for each segment
        """
        recommendations = {
            0: {
                'segment_name': 'High-Value Customers',
                'actions': [
                    '🎯 VIP loyalty program with exclusive benefits',
                    '💎 Premium product recommendations',
                    '🎁 Personalized offers and early access to sales',
                    '📧 Regular engagement through email/chat'
                ]
            },
            1: {
                'segment_name': 'Engaged Browsers',
                'actions': [
                    '🛒 Cart abandonment campaigns',
                    '💰 Limited-time discount offers',
                    '📱 Push notifications for viewed products',
                    '⭐ Social proof (reviews, ratings)'
                ]
            },
            2: {
                'segment_name': 'Occasional Buyers',
                'actions': [
                    '🔄 Re-engagement campaigns',
                    '🎯 Targeted promotions based on past purchases',
                    '📊 Product recommendations',
                    '💌 Win-back offers'
                ]
            },
            3: {
                'segment_name': 'New Visitors',
                'actions': [
                    '👋 Welcome campaigns',
                    '🎁 First-purchase discounts',
                    '📚 Educational content about products',
                    '💬 Proactive chat support'
                ]
            }
        }
        
        return recommendations.get(cluster_id, {'segment_name': 'Standard', 'actions': []})


def run_segmentation(data_path):
    """
    Run customer segmentation analysis
    """
    # Load data
    chat_df = pd.read_csv(f"{data_path}/chat_data_cleaned.csv")
    traffic_df = pd.read_csv(f"{data_path}/traffic_overview_cleaned.csv")
    product_df = pd.read_csv(f"{data_path}/product_overview_cleaned.csv")
    
    # Initialize model
    model = CustomerSegmentation(n_clusters=4)
    
    # Create time-based segments
    segments_df = model.create_time_based_segments(chat_df, traffic_df, product_df)
    
    # Fit model
    labels = model.fit(segments_df)
    
    # Add labels to segments
    segments_df['Segment'] = labels
    
    return model, segments_df, labels


if __name__ == "__main__":
    data_path = "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
    model, segments_df, labels = run_segmentation(data_path)
    
    print("✅ Customer Segmentation Complete!")
    print(f"\n📊 Segment Summary:")
    print(model.get_segment_summary())
    
    print(f"\n💡 Recommendations for each segment:")
    for i in range(4):
        rec = model.get_recommendations(i)
        print(f"\n{rec['segment_name']}:")
        for action in rec['actions']:
            print(f"  {action}")
