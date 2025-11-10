#!/usr/bin/env python3
"""
Compare Original vs Enhanced Forecast Models
Shows the improvement in prediction variability
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load both forecasts
original = pd.read_csv('weekly_sales_forecast_6months_FINAL.csv')
enhanced = pd.read_csv('weekly_sales_forecast_6months_ENHANCED.csv')

# Convert dates
original['Week'] = pd.to_datetime(original['Week'])
enhanced['Week'] = pd.to_datetime(enhanced['Week'])

# Calculate statistics
print("="*70)
print("FORECAST COMPARISON: Original vs Enhanced Model")
print("="*70)

print("\n📊 ORIGINAL MODEL (Flat Predictions):")
print(f"  Avg Weekly Sales: IDR {original['Predicted_Sales'].mean()/1e6:.2f}M")
print(f"  Min Weekly: IDR {original['Predicted_Sales'].min()/1e6:.2f}M")
print(f"  Max Weekly: IDR {original['Predicted_Sales'].max()/1e6:.2f}M")
print(f"  Range: IDR {(original['Predicted_Sales'].max() - original['Predicted_Sales'].min())/1e6:.2f}M")
print(f"  Std Dev: IDR {original['Predicted_Sales'].std()/1e6:.2f}M")
print(f"  Coefficient of Variation: {(original['Predicted_Sales'].std()/original['Predicted_Sales'].mean())*100:.2f}%")

print("\n🚀 ENHANCED MODEL (Captures Variability):")
print(f"  Avg Weekly Sales: IDR {enhanced['Predicted_Sales'].mean()/1e6:.2f}M")
print(f"  Min Weekly: IDR {enhanced['Predicted_Sales'].min()/1e6:.2f}M")
print(f"  Max Weekly: IDR {enhanced['Predicted_Sales'].max()/1e6:.2f}M")
print(f"  Range: IDR {(enhanced['Predicted_Sales'].max() - enhanced['Predicted_Sales'].min())/1e6:.2f}M")
print(f"  Std Dev: IDR {enhanced['Predicted_Sales'].std()/1e6:.2f}M")
print(f"  Coefficient of Variation: {(enhanced['Predicted_Sales'].std()/enhanced['Predicted_Sales'].mean())*100:.2f}%")

print("\n✅ IMPROVEMENT:")
range_improvement = ((enhanced['Predicted_Sales'].max() - enhanced['Predicted_Sales'].min()) / 
                     (original['Predicted_Sales'].max() - original['Predicted_Sales'].min())) * 100
std_improvement = (enhanced['Predicted_Sales'].std() / original['Predicted_Sales'].std()) * 100
print(f"  Range increased by: {range_improvement:.1f}x")
print(f"  Std Dev increased by: {std_improvement:.1f}x")
print(f"  ✅ Model now captures {std_improvement:.0f}% more variability!")

print("\n" + "="*70)

# Create comparison plot
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Plot 1: Side-by-side comparison
ax1 = axes[0]
ax1.plot(original['Week'], original['Predicted_Sales']/1e6, 
         marker='o', linewidth=2, label='Original (Flat)', color='#FF6B6B', alpha=0.7)
ax1.plot(enhanced['Week'], enhanced['Predicted_Sales']/1e6, 
         marker='s', linewidth=2, label='Enhanced (Variable)', color='#4ECDC4', alpha=0.7)
ax1.set_title('📊 Forecast Comparison: Original vs Enhanced Model', fontsize=14, fontweight='bold')
ax1.set_xlabel('Week', fontsize=11)
ax1.set_ylabel('Predicted Sales (Million IDR)', fontsize=11)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Difference plot
ax2 = axes[1]
difference = enhanced['Predicted_Sales'] - original['Predicted_Sales']
colors = ['green' if x > 0 else 'red' for x in difference]
ax2.bar(enhanced['Week'], difference/1e6, color=colors, alpha=0.6)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.set_title('📈 Difference: Enhanced - Original (Shows Variability Captured)', 
              fontsize=14, fontweight='bold')
ax2.set_xlabel('Week', fontsize=11)
ax2.set_ylabel('Difference (Million IDR)', fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('forecast_comparison.png', dpi=300, bbox_inches='tight')
print("\n✅ Saved comparison plot: forecast_comparison.png")
plt.show()

# Show week-by-week comparison
print("\n📋 WEEK-BY-WEEK COMPARISON (First 10 weeks):")
print("-"*70)
comparison = pd.DataFrame({
    'Week': original['Week'].dt.strftime('%Y-%m-%d'),
    'Original (M IDR)': (original['Predicted_Sales']/1e6).round(2),
    'Enhanced (M IDR)': (enhanced['Predicted_Sales']/1e6).round(2),
    'Diff (M IDR)': ((enhanced['Predicted_Sales'] - original['Predicted_Sales'])/1e6).round(2)
})
print(comparison.head(10).to_string(index=False))
print("-"*70)
