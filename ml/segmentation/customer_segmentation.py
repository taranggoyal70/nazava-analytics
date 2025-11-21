"""
Customer Segmentation Model using K-Means Clustering
Identifies high-value customer segments for targeted marketing
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import warnings
warnings.filterwarnings('ignore')


class CustomerSegmentation:
    """Customer segmentation using K-Means clustering"""
    
    def __init__(self, data_path=None, n_clusters=4):
        self.data_path = data_path or "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = StandardScaler()
        self.pca = None
        self.segments = None
        self.feature_names = []
        
    def load_and_prepare_data(self):
        """Load data and create customer features"""
        print("📊 Loading customer data...")
        
        # Load multiple data sources
        chat_df = pd.read_csv(f"{self.data_path}/chat_data_cleaned.csv")
        flash_df = pd.read_csv(f"{self.data_path}/flash_sale_cleaned.csv")
        product_df = pd.read_csv(f"{self.data_path}/product_overview_cleaned.csv")
        
        print(f"   Chat data: {len(chat_df)} records")
        print(f"   Flash sale data: {len(flash_df)} records")
        print(f"   Product data: {len(product_df)} records")
        
        # Create customer behavior features
        # Since we don't have individual customer IDs, we'll segment based on time periods
        # Each period represents a cohort of customers
        
        features_list = []
        
        # Process chat data (monthly cohorts)
        for idx, row in chat_df.iterrows():
            chats_replied = pd.to_numeric(row['Chats_Replied'], errors='coerce')
            total_chats = pd.to_numeric(row['Number_Of_Chats'], errors='coerce')
            reply_rate = (chats_replied / total_chats * 100) if total_chats > 0 else 0
            
            features = {
                'period': row['Time_Period'],
                'chat_volume': pd.to_numeric(row['Number_Of_Chats'], errors='coerce'),
                'reply_rate': reply_rate,
                'avg_response_time_min': pd.to_numeric(row['Average_Response_Time'], errors='coerce'),
                'csat_score': pd.to_numeric(row['CSAT_Percent'], errors='coerce'),
                'chat_conversion_rate': pd.to_numeric(row['Conversion_Rate_Chats_Replied'], errors='coerce'),
                'sales': pd.to_numeric(row['Sales_IDR'], errors='coerce'),
                'orders': pd.to_numeric(row['Total_Orders'], errors='coerce'),
            }
            features_list.append(features)
        
        # Add flash sale behavior
        for idx, row in flash_df.iterrows():
            period = row['Time_Period']
            # Find matching period in features
            matching = [f for f in features_list if f['period'] == period]
            if matching:
                f = matching[0]
                f['flash_click_rate'] = pd.to_numeric(row['Click_Rate'], errors='coerce')
                f['flash_sales'] = pd.to_numeric(row['Sales_Orders_Created_IDR'], errors='coerce')
                f['flash_orders'] = pd.to_numeric(row['Orders_Created'], errors='coerce')
        
        # Create DataFrame
        customer_df = pd.DataFrame(features_list)
        
        # Fill missing values with 0
        customer_df = customer_df.fillna(0)
        
        # Calculate derived features
        customer_df['avg_order_value'] = customer_df.apply(
            lambda x: x['sales'] / x['orders'] if x['orders'] > 0 else 0, axis=1
        )
        customer_df['engagement_score'] = (
            customer_df['chat_conversion_rate'] * 0.4 +
            customer_df['reply_rate'] * 0.3 +
            customer_df['csat_score'] / 100 * 0.3
        )
        customer_df['purchase_frequency'] = customer_df['orders']
        
        print(f"\n✅ Created customer feature dataset: {len(customer_df)} cohorts")
        print(f"📊 Features: {len(customer_df.columns) - 1} behavioral metrics")
        
        return customer_df
    
    def select_features(self, df):
        """Select features for clustering"""
        # Key features for segmentation
        feature_cols = [
            'sales',
            'orders',
            'avg_order_value',
            'chat_conversion_rate',
            'engagement_score',
            'csat_score',
            'reply_rate',
            'flash_sales',
            'purchase_frequency'
        ]
        
        # Filter to available features
        available_features = [col for col in feature_cols if col in df.columns]
        self.feature_names = available_features
        
        X = df[available_features].values
        
        print(f"\n🎯 Selected {len(available_features)} features for clustering:")
        for feat in available_features:
            print(f"   - {feat}")
        
        return X, df
    
    def train_model(self, X):
        """Train K-Means clustering model"""
        print(f"\n🤖 Training K-Means clustering model...")
        print(f"📊 Number of clusters: {self.n_clusters}")
        
        # Standardize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA for dimensionality reduction (optional, for visualization)
        self.pca = PCA(n_components=2)
        X_pca = self.pca.fit_transform(X_scaled)
        
        print(f"   PCA explained variance: {self.pca.explained_variance_ratio_.sum():.2%}")
        
        # Train K-Means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            init='k-means++',
            n_init=10,
            max_iter=300,
            random_state=42
        )
        
        print("⏳ Training in progress...")
        cluster_labels = self.model.fit_predict(X_scaled)
        
        # Calculate silhouette score
        from sklearn.metrics import silhouette_score
        silhouette_avg = silhouette_score(X_scaled, cluster_labels)
        
        print(f"✅ Model trained successfully!")
        print(f"📊 Silhouette Score: {silhouette_avg:.3f}")
        
        if silhouette_avg > 0.5:
            print("   ✅ Excellent cluster separation")
        elif silhouette_avg > 0.3:
            print("   ✅ Good cluster separation")
        else:
            print("   ⚠️  Moderate cluster separation")
        
        return cluster_labels, X_scaled, X_pca
    
    def analyze_segments(self, df, cluster_labels, X):
        """Analyze and profile each segment"""
        print("\n" + "="*70)
        print("📊 CUSTOMER SEGMENT ANALYSIS")
        print("="*70)
        
        df['segment'] = cluster_labels
        
        segment_profiles = []
        
        for segment_id in range(self.n_clusters):
            segment_data = df[df['segment'] == segment_id]
            
            profile = {
                'segment_id': segment_id,
                'size': len(segment_data),
                'size_pct': len(segment_data) / len(df) * 100,
                'avg_sales': segment_data['sales'].mean(),
                'total_sales': segment_data['sales'].sum(),
                'avg_orders': segment_data['orders'].mean(),
                'avg_order_value': segment_data['avg_order_value'].mean(),
                'avg_engagement': segment_data['engagement_score'].mean(),
                'avg_csat': segment_data['csat_score'].mean(),
                'avg_conversion': segment_data['chat_conversion_rate'].mean(),
            }
            
            segment_profiles.append(profile)
        
        # Sort by total sales (descending)
        segment_profiles = sorted(segment_profiles, key=lambda x: x['total_sales'], reverse=True)
        
        # Assign segment names
        segment_names = ['High-Value Champions', 'Engaged Buyers', 'Potential Customers', 'Low Engagement']
        
        for i, profile in enumerate(segment_profiles):
            profile['name'] = segment_names[i] if i < len(segment_names) else f'Segment {i+1}'
        
        self.segments = segment_profiles
        
        # Print segment profiles
        for profile in segment_profiles:
            print(f"\n🎯 {profile['name']} (Segment {profile['segment_id']})")
            print(f"   Size: {profile['size']} cohorts ({profile['size_pct']:.1f}%)")
            print(f"   Total Sales: IDR {profile['total_sales']/1e6:.1f}M")
            print(f"   Avg Sales/Period: IDR {profile['avg_sales']/1e6:.2f}M")
            print(f"   Avg Orders: {profile['avg_orders']:.0f}")
            print(f"   Avg Order Value: IDR {profile['avg_order_value']/1e3:.0f}K")
            print(f"   Engagement Score: {profile['avg_engagement']:.2f}")
            print(f"   CSAT Score: {profile['avg_csat']:.1f}%")
            print(f"   Conversion Rate: {profile['avg_conversion']:.2%}")
        
        return segment_profiles
    
    def get_recommendations(self):
        """Generate marketing recommendations for each segment"""
        print("\n" + "="*70)
        print("💡 MARKETING RECOMMENDATIONS BY SEGMENT")
        print("="*70)
        
        recommendations = {
            'High-Value Champions': {
                'strategy': 'Retention & VIP Treatment',
                'actions': [
                    '🎁 Exclusive VIP rewards and early access to sales',
                    '💎 Premium customer service with priority support',
                    '📧 Personalized product recommendations',
                    '🎯 Loyalty program with special benefits',
                    '💰 High-value product bundles and upsells'
                ]
            },
            'Engaged Buyers': {
                'strategy': 'Growth & Upselling',
                'actions': [
                    '📈 Encourage higher order values with bundles',
                    '🎪 Flash sale notifications for relevant products',
                    '⭐ Request reviews and referrals',
                    '🔔 Re-engagement campaigns for repeat purchases',
                    '💳 Introduce to premium product lines'
                ]
            },
            'Potential Customers': {
                'strategy': 'Activation & Conversion',
                'actions': [
                    '🎁 First-purchase discounts and vouchers',
                    '📱 Chat engagement to answer questions',
                    '🛒 Abandoned cart recovery campaigns',
                    '📊 Product education and demonstrations',
                    '💬 Proactive customer support'
                ]
            },
            'Low Engagement': {
                'strategy': 'Re-engagement & Win-back',
                'actions': [
                    '🔥 Aggressive promotional offers',
                    '📧 Win-back email campaigns',
                    '🎯 Targeted ads with special deals',
                    '💰 Deep discounts on popular products',
                    '📞 Direct outreach to understand barriers'
                ]
            }
        }
        
        for segment in self.segments:
            name = segment['name']
            if name in recommendations:
                rec = recommendations[name]
                print(f"\n🎯 {name}")
                print(f"   Strategy: {rec['strategy']}")
                print(f"   Actions:")
                for action in rec['actions']:
                    print(f"      {action}")
        
        return recommendations
    
    def save_model(self, filepath='ml/trained_models/customer_segmentation.pkl'):
        """Save trained model"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'pca': self.pca,
            'feature_names': self.feature_names,
            'segments': self.segments,
            'n_clusters': self.n_clusters
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\n💾 Model saved to {filepath}")


def main():
    """Main execution"""
    print("="*70)
    print("🎯 NAZAVA CUSTOMER SEGMENTATION MODEL")
    print("   Objective #3: Identify High-Value Customer Segments")
    print("="*70)
    
    # Initialize segmentation model
    segmenter = CustomerSegmentation(n_clusters=4)
    
    # Load and prepare data
    customer_df = segmenter.load_and_prepare_data()
    
    # Select features
    X, customer_df = segmenter.select_features(customer_df)
    
    # Train model
    cluster_labels, X_scaled, X_pca = segmenter.train_model(X)
    
    # Analyze segments
    segment_profiles = segmenter.analyze_segments(customer_df, cluster_labels, X)
    
    # Get recommendations
    recommendations = segmenter.get_recommendations()
    
    # Summary
    print("\n" + "="*70)
    print("📊 SEGMENTATION SUMMARY")
    print("="*70)
    
    total_sales = sum(s['total_sales'] for s in segment_profiles)
    high_value_sales = segment_profiles[0]['total_sales']
    
    print(f"\nTotal Customer Cohorts: {len(customer_df)}")
    print(f"Number of Segments: {segmenter.n_clusters}")
    print(f"Total Sales: IDR {total_sales/1e6:.1f}M")
    print(f"\n🏆 Top Segment: {segment_profiles[0]['name']}")
    print(f"   Contributes: IDR {high_value_sales/1e6:.1f}M ({high_value_sales/total_sales*100:.1f}% of total)")
    print(f"   Size: {segment_profiles[0]['size']} cohorts ({segment_profiles[0]['size_pct']:.1f}%)")
    
    print("\n✅ Customer segmentation complete!")
    print("🎯 Use these segments for targeted marketing campaigns")
    
    return segmenter, customer_df, segment_profiles


if __name__ == "__main__":
    segmenter, customer_df, segments = main()
