import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import os

base_path = './final_data/glg1-spectral'
desired_labels = ['baseline', 'g25']
versions = [d for d in sorted(os.listdir(base_path))
            if os.path.isdir(os.path.join(base_path, d))]
data_list = []

for version in versions:
    folder_path = os.path.join(base_path, version)
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(os.path.join(folder_path, file))
                    
                    initial_energy = df['PACKAGE_ENERGY (J)'].iloc[0]
                    final_energy = df['PACKAGE_ENERGY (J)'].iloc[-1]
                    total_run_energy = final_energy - initial_energy
                    
                    # Filter out hardware counter rollovers
                    if total_run_energy < 0:
                        print(f"Skipping rollover in {file}: {total_run_energy} J")
                        continue

                    label = version.replace('spectral_norm_', '').replace('.py', '')
                    if label in desired_labels:
                        data_list.append({'Version': label, 'Total Energy (J)': total_run_energy})
                except Exception as e:
                    print(f"Error processing {file}: {e}")

plot_df = pd.DataFrame(data_list)
order = desired_labels
# 4. Visualizing
plt.figure(figsize=(12, 7))
sns.set_theme(style="whitegrid")

# Create the boxplot
ax = sns.boxplot(x='Version', y='Total Energy (J)', data=plot_df, palette='Set2', hue=None, legend=False, order=order)
sns.stripplot(x='Version', y='Total Energy (J)', data=plot_df, color=".25", alpha=0.5, order=order) # Adds dots for each run

plt.title('GLG1 Spectral Norm - energy', fontsize=16)
plt.xlabel('Guideline Version', fontsize=12)
plt.ylabel('Total Energy (Joules)', fontsize=12)

plt.tight_layout()
plt.savefig('energy_boxplot.png')
