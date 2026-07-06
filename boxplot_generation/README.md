# Box-plot Generation Scripts

This folder contains the scripts used to calculate energy and execution time from the raw EnergiBridge CSV files, and to generate the resulting box-plots.

There are two scripts:

- **Energy script** - calculates the total energy consumed per run as the difference between the last and first `PACKAGE_ENERGY (J)` readings:

```python
initial_energy = df['PACKAGE_ENERGY (J)'].iloc[0]
final_energy = df['PACKAGE_ENERGY (J)'].iloc[-1]
total_run_energy = final_energy - initial_energy
```

- **Time script** - follows the same logic, using the `Time` column instead, and additionally divides the result by 1000.0 to convert the measurement from milliseconds to seconds.

They both filter out rollovers!

## Usage

To generate box-plots for a different baseline or optimization, change the following lines at the top of either script:

```python
base_path = '../final_data/glg1-spectral'
desired_labels = ['baseline', 'g25']
```

- `base_path` - the folder containing the runs you want to analyze.
- `desired_labels` - the specific baseline/guideline version(s) to include in the plot.
