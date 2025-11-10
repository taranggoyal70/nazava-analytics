"""
Campaign ROI Optimizer
Analyzes campaign performance and recommends optimal marketing spend allocation
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


class CampaignOptimizer:
    """Optimize marketing campaign spend for maximum ROI"""
    
    def __init__(self, data_path=None):
        self.data_path = data_path or "/Users/tarang/CascadeProjects/windsurf-project/analytical-showdown-pipeline/cleaned_data"
        self.campaign_performance = {}
        self.recommendations = {}
        
    def load_campaign_data(self):
        """Load all campaign data"""
        print("📊 Loading campaign data...")
        
        # Load different campaign types
        flash_df = pd.read_csv(f"{self.data_path}/flash_sale_cleaned.csv")
        voucher_df = pd.read_csv(f"{self.data_path}/voucher_cleaned.csv")
        
        print(f"   Flash sales: {len(flash_df)} periods")
        print(f"   Vouchers: {len(voucher_df)} periods")
        
        return flash_df, voucher_df
    
    def analyze_flash_sales(self, flash_df):
        """Analyze flash sale performance"""
        print("\n🔥 Analyzing Flash Sale Performance...")
        
        # Convert to numeric
        sales = pd.to_numeric(flash_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
        orders = pd.to_numeric(flash_df['Orders_Ready_To_Ship'], errors='coerce').sum()
        products_clicked = pd.to_numeric(flash_df['Products_Clicked'], errors='coerce').sum()
        products_viewed = pd.to_numeric(flash_df['Number_Of_Products_Viewed'], errors='coerce').sum()
        click_rate_avg = pd.to_numeric(flash_df['Click_Rate'], errors='coerce').mean()
        
        # Calculate metrics
        avg_order_value = sales / orders if orders > 0 else 0
        click_rate = click_rate_avg  # Already a percentage
        conversion_rate = (orders / products_clicked * 100) if products_clicked > 0 else 0
        
        # Estimate cost (typical flash sale discount is 20-30%)
        estimated_cost = sales * 0.25  # 25% discount average
        roi = ((sales - estimated_cost) / estimated_cost * 100) if estimated_cost > 0 else 0
        
        performance = {
            'campaign_type': 'Flash Sales',
            'total_sales': sales,
            'total_orders': orders,
            'avg_order_value': avg_order_value,
            'total_clicks': products_clicked,
            'total_views': products_viewed,
            'click_rate': click_rate,
            'conversion_rate': conversion_rate,
            'estimated_cost': estimated_cost,
            'roi': roi,
            'profit': sales - estimated_cost
        }
        
        self.campaign_performance['flash_sales'] = performance
        
        print(f"   Total Sales: IDR {sales/1e6:.1f}M")
        print(f"   Total Orders: {int(orders):,}")
        print(f"   Avg Order Value: IDR {avg_order_value/1e3:.0f}K")
        print(f"   Click Rate: {click_rate:.2f}%")
        print(f"   Conversion Rate: {conversion_rate:.2f}%")
        print(f"   Estimated Cost: IDR {estimated_cost/1e6:.1f}M")
        print(f"   ROI: {roi:.1f}%")
        
        return performance
    
    def analyze_vouchers(self, voucher_df):
        """Analyze voucher performance"""
        print("\n🎫 Analyzing Voucher Performance...")
        
        # Convert to numeric
        sales = pd.to_numeric(voucher_df['Sales_Ready_To_Ship_IDR'], errors='coerce').sum()
        orders = pd.to_numeric(voucher_df['Orders_Ready_To_Ship'], errors='coerce').sum()
        voucher_cost = pd.to_numeric(voucher_df['Total_Cost_Ready_To_Ship_IDR'], errors='coerce').sum()
        
        # Calculate metrics
        avg_order_value = sales / orders if orders > 0 else 0
        cost_per_order = voucher_cost / orders if orders > 0 else 0
        roi = ((sales - voucher_cost) / voucher_cost * 100) if voucher_cost > 0 else 0
        
        performance = {
            'campaign_type': 'Vouchers',
            'total_sales': sales,
            'total_orders': orders,
            'avg_order_value': avg_order_value,
            'voucher_cost': voucher_cost,
            'cost_per_order': cost_per_order,
            'roi': roi,
            'profit': sales - voucher_cost
        }
        
        self.campaign_performance['vouchers'] = performance
        
        print(f"   Total Sales: IDR {sales/1e6:.1f}M")
        print(f"   Total Orders: {int(orders):,}")
        print(f"   Avg Order Value: IDR {avg_order_value/1e3:.0f}K")
        print(f"   Voucher Cost: IDR {voucher_cost/1e6:.1f}M")
        print(f"   Cost per Order: IDR {cost_per_order/1e3:.0f}K")
        print(f"   ROI: {roi:.1f}%")
        
        return performance
    
    def compare_campaigns(self):
        """Compare all campaigns and rank by ROI"""
        print("\n" + "="*70)
        print("📊 CAMPAIGN COMPARISON & RANKING")
        print("="*70)
        
        # Sort by ROI
        campaigns = sorted(
            self.campaign_performance.values(),
            key=lambda x: x['roi'],
            reverse=True
        )
        
        print(f"\n{'Rank':<6} {'Campaign':<15} {'Sales':<15} {'ROI':<10} {'Profit':<15}")
        print("-" * 70)
        
        for i, camp in enumerate(campaigns, 1):
            print(f"{i:<6} {camp['campaign_type']:<15} IDR {camp['total_sales']/1e6:>6.1f}M   {camp['roi']:>6.1f}%   IDR {camp['profit']/1e6:>6.1f}M")
        
        return campaigns
    
    def generate_recommendations(self, campaigns):
        """Generate optimization recommendations"""
        print("\n" + "="*70)
        print("💡 CAMPAIGN OPTIMIZATION RECOMMENDATIONS")
        print("="*70)
        
        total_sales = sum(c['total_sales'] for c in campaigns)
        total_cost = sum(c.get('estimated_cost', c.get('voucher_cost', 0)) for c in campaigns)
        
        print(f"\n📊 Overall Performance:")
        print(f"   Total Sales: IDR {total_sales/1e6:.1f}M")
        print(f"   Total Marketing Cost: IDR {total_cost/1e6:.1f}M")
        print(f"   Marketing Cost as % of Revenue: {total_cost/total_sales*100:.1f}%")
        print(f"   Overall ROI: {((total_sales - total_cost)/total_cost*100):.1f}%")
        
        # Recommendations by campaign type
        print("\n🎯 Campaign-Specific Recommendations:")
        
        for camp in campaigns:
            camp_type = camp['campaign_type']
            roi = camp['roi']
            
            print(f"\n{'='*70}")
            print(f"📌 {camp_type}")
            print(f"{'='*70}")
            
            if roi > 300:
                print("   ✅ EXCELLENT ROI - Increase investment")
                print(f"   💰 Current ROI: {roi:.1f}%")
                print("   📈 Recommendation: Increase budget by 30-50%")
                print("   🎯 Action: Scale up this campaign type")
                self.recommendations[camp_type] = {
                    'status': 'Excellent',
                    'action': 'Scale Up',
                    'budget_change': '+30-50%',
                    'priority': 'High'
                }
                
            elif roi > 200:
                print("   ✅ GOOD ROI - Maintain and optimize")
                print(f"   💰 Current ROI: {roi:.1f}%")
                print("   📈 Recommendation: Maintain current budget")
                print("   🎯 Action: Optimize targeting and timing")
                self.recommendations[camp_type] = {
                    'status': 'Good',
                    'action': 'Maintain & Optimize',
                    'budget_change': '0-10%',
                    'priority': 'Medium'
                }
                
            elif roi > 100:
                print("   ⚠️  MODERATE ROI - Optimize or reduce")
                print(f"   💰 Current ROI: {roi:.1f}%")
                print("   📈 Recommendation: Optimize campaign efficiency")
                print("   🎯 Action: Test different approaches")
                self.recommendations[camp_type] = {
                    'status': 'Moderate',
                    'action': 'Optimize',
                    'budget_change': '-10-0%',
                    'priority': 'Medium'
                }
                
            else:
                print("   ❌ LOW ROI - Reduce or restructure")
                print(f"   💰 Current ROI: {roi:.1f}%")
                print("   📈 Recommendation: Reduce budget significantly")
                print("   🎯 Action: Restructure or pause campaign")
                self.recommendations[camp_type] = {
                    'status': 'Low',
                    'action': 'Reduce/Restructure',
                    'budget_change': '-30-50%',
                    'priority': 'Low'
                }
        
        return self.recommendations
    
    def calculate_optimal_budget_allocation(self, total_budget=100e6):
        """Calculate optimal budget allocation across campaigns"""
        print("\n" + "="*70)
        print(f"💰 OPTIMAL BUDGET ALLOCATION (Total: IDR {total_budget/1e6:.0f}M)")
        print("="*70)
        
        # Weight by ROI
        campaigns = list(self.campaign_performance.values())
        total_roi_weight = sum(max(0, c['roi']) for c in campaigns)
        
        print(f"\n{'Campaign':<20} {'Current %':<12} {'Optimal %':<12} {'Allocation':<15}")
        print("-" * 70)
        
        allocations = {}
        
        for camp in campaigns:
            camp_type = camp['campaign_type']
            current_cost = camp.get('estimated_cost', camp.get('voucher_cost', 0))
            current_pct = (current_cost / sum(c.get('estimated_cost', c.get('voucher_cost', 0)) for c in campaigns)) * 100
            
            # Optimal allocation based on ROI
            roi_weight = max(0, camp['roi'])
            optimal_pct = (roi_weight / total_roi_weight * 100) if total_roi_weight > 0 else 0
            optimal_allocation = total_budget * (optimal_pct / 100)
            
            allocations[camp_type] = {
                'current_pct': current_pct,
                'optimal_pct': optimal_pct,
                'optimal_amount': optimal_allocation
            }
            
            print(f"{camp_type:<20} {current_pct:>6.1f}%      {optimal_pct:>6.1f}%      IDR {optimal_allocation/1e6:>6.1f}M")
        
        return allocations
    
    def get_action_plan(self):
        """Generate actionable plan"""
        print("\n" + "="*70)
        print("📋 ACTION PLAN - NEXT 30 DAYS")
        print("="*70)
        
        actions = []
        
        # High priority actions
        print("\n🔥 HIGH PRIORITY:")
        for camp_type, rec in self.recommendations.items():
            if rec['priority'] == 'High':
                action = f"   • {camp_type}: {rec['action']} (Budget: {rec['budget_change']})"
                print(action)
                actions.append(action)
        
        # Medium priority actions
        print("\n⚠️  MEDIUM PRIORITY:")
        for camp_type, rec in self.recommendations.items():
            if rec['priority'] == 'Medium':
                action = f"   • {camp_type}: {rec['action']} (Budget: {rec['budget_change']})"
                print(action)
                actions.append(action)
        
        # General recommendations
        print("\n💡 GENERAL RECOMMENDATIONS:")
        general_recs = [
            "   • Monitor campaign performance weekly",
            "   • A/B test different discount levels",
            "   • Target high-value customer segments",
            "   • Optimize campaign timing (weekends, paydays)",
            "   • Integrate with chat for better conversion",
            "   • Track customer lifetime value by campaign source"
        ]
        
        for rec in general_recs:
            print(rec)
            actions.append(rec)
        
        return actions


def main():
    """Main execution"""
    print("="*70)
    print("💰 NAZAVA CAMPAIGN ROI OPTIMIZER")
    print("   Objective #3: Optimize Marketing Spend for Maximum ROI")
    print("="*70)
    
    # Initialize optimizer
    optimizer = CampaignOptimizer()
    
    # Load data
    flash_df, voucher_df = optimizer.load_campaign_data()
    
    # Analyze campaigns
    flash_performance = optimizer.analyze_flash_sales(flash_df)
    voucher_performance = optimizer.analyze_vouchers(voucher_df)
    
    # Compare campaigns
    ranked_campaigns = optimizer.compare_campaigns()
    
    # Generate recommendations
    recommendations = optimizer.generate_recommendations(ranked_campaigns)
    
    # Calculate optimal budget allocation
    allocations = optimizer.calculate_optimal_budget_allocation(total_budget=100e6)
    
    # Get action plan
    actions = optimizer.get_action_plan()
    
    print("\n" + "="*70)
    print("✅ CAMPAIGN OPTIMIZATION COMPLETE!")
    print("="*70)
    print("\n🎯 Key Takeaways:")
    print(f"   • Best performing campaign: {ranked_campaigns[0]['campaign_type']} ({ranked_campaigns[0]['roi']:.1f}% ROI)")
    print(f"   • Total marketing efficiency: {sum(c['profit'] for c in ranked_campaigns)/1e6:.1f}M profit")
    print(f"   • Recommended actions: {len(actions)} items")
    
    return optimizer, ranked_campaigns, recommendations


if __name__ == "__main__":
    optimizer, campaigns, recommendations = main()
