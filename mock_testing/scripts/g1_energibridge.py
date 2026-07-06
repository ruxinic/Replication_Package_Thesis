import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
folder_path = '../mock_results'
print(f"Checking for files in: {os.path.abspath(folder_path)}")

def get_total_energy(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()
        # Calculate energy
        energy_diff = df['CPU_ENERGY (J)'].iloc[-1] - df['CPU_ENERGY (J)'].iloc[0]
        return energy_diff
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

benchmarks = ['g24_baseline', 'g24_optimized']
data = {}

for b in benchmarks:
    files = glob.glob(os.path.join(folder_path, f"{b}*.csv"))
    print(f"Found {len(files)} files for {b}")
    
    # Only keep valid results
    results = [get_total_energy(f) for f in files]
    data[b] = [r for r in results if r is not None]
if not any(data.values()):
    print("CRITICAL: No data was collected. Check your folder path and CSV headers!")
else:
    plt.figure(figsize=(10, 6))
    plt.boxplot(data.values(), labels=data.keys())
    plt.title('Energy Consumption Comparison (30 Runs Each)')
    plt.ylabel('Energy Consumed (Joules)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig('../g24_energy_boxplot.png')
    print("Boxplot saved as g2_energy_boxplot.png!")
    plt.close()