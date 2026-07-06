import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def get_total_energy(file_path):
    df = pd.read_csv(file_path)
    # Calculate the difference between the last and first energy reading
    # Using 'CPU_ENERGY (J)' as the primary metric
    energy_diff = df['CPU_ENERGY (J)'].iloc[-1] - df['CPU_ENERGY (J)'].iloc[0]
    return energy_diff

# Change this to visualize other benchmarks
benchmarks = ['nbody', 'mandelbrot', 'binary-trees', 'fannkuch']
data = {}

for b in benchmarks:
    files = glob.glob(f"results/{b}*.csv")
    data[b] = [get_total_energy(f) for f in files]

plt.figure(figsize=(10, 6))
plt.boxplot(data.values(), labels=data.keys())
plt.title('Energy Consumption Comparison (30 Runs Each)')
plt.ylabel('Energy Consumed (Joules)')
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig('energy_boxplot.png')
print("Boxplot saved as energy_boxplot.png!")
plt.show()