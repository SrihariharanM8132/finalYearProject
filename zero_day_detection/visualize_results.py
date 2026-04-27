import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

print("Creating visualizations...")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ===== Plot 1: Model Comparison =====
print("\n[1/3] Creating model comparison chart...")

models = ['CNN', 'Decision Tree', 'Random Forest', 'KNN', 'Naive Bayes']
accuracies = [0.99, 1.00, 1.00, 0.99, 0.98]  # Replace with your actual results

plt.figure(figsize=(10, 6))
bars = plt.bar(models, accuracies, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
plt.title('Model Performance Comparison', fontsize=16, fontweight='bold')
plt.ylabel('Accuracy', fontsize=12)
plt.ylim([0.95, 1.02])

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.005,
             f'{height:.3f}', ha='center', va='bottom', fontweight='bold')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('results/model_comparison.png', dpi=300)
print("✓ Saved: results/model_comparison.png")
plt.close()

# ===== Plot 2: Attack Distribution =====
print("\n[2/3] Creating attack distribution chart...")

attacks = ['Normal', 'DoS', 'Probe', 'R2L', 'U2R']
counts = [67343, 45927, 11656, 995, 52]  # NSL-KDD actual distribution

plt.figure(figsize=(10, 6))
plt.pie(counts, labels=attacks, autopct='%1.1f%%', startangle=90,
        colors=['#95E1D3', '#F38181', '#EAFFD0', '#FCE38A', '#AA96DA'])
plt.title('Attack Type Distribution in Dataset', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('results/attack_distribution.png', dpi=300)
print("✓ Saved: results/attack_distribution.png")
plt.close()

# ===== Plot 3: Framework Phases =====
print("\n[3/3] Creating framework diagram...")

phases = ['Phase 1\nData\nCollection', 'Phase 2\nSupervised\nClassification',
          'Phase 3\nClustering', 'Phase 4\nCorrelation', 'Phase 5\nZero-Day\nDetection']
completion = [100, 100, 100, 100, 100]

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(phases, completion, color=['#667BC6', '#7BC9FF', '#DA7297', '#FEFF86', '#A1D6B2'])
ax.set_xlabel('Completion (%)', fontsize=12)
ax.set_title('Framework Implementation Progress', fontsize=16, fontweight='bold')
ax.set_xlim([0, 110])

# Add percentage labels
for i, (bar, value) in enumerate(zip(bars, completion)):
    ax.text(value + 2, i, f'{value}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('results/framework_progress.png', dpi=300)
print("✓ Saved: results/framework_progress.png")
plt.close()

print("\n✅ All visualizations created in results/ folder!")