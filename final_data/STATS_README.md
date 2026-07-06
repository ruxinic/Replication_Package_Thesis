# Statistical Analysis — How the Notebooks Work

Both `data_analysis_RQ0.ipynb` (energy) and `data_analysis_RQ1.ipynb` (execution time) follow the exact same four-step statistical pipeline described in the thesis, applied separately to energy and to time. The only real difference between the two notebooks is which raw column they extract from the `.csv` files (`PACKAGE_ENERGY (J)` vs. `Time`).

## Step 0 - Extracting one value per run

For every run's `.csv` file, both EnergiBridge metrics are recorded as **monotonically increasing counters** across the run, so the actual per-run value is computed as the difference between the last and the first reading:

- **Energy** (`extract_run_energy`): `last(PACKAGE_ENERGY) - first(PACKAGE_ENERGY)`, in Joules.
- **Time** (`extract_run_time`): `last(Time) - first(Time)`, converted from milliseconds to seconds.

In both cases, runs where this delta is `<= 0` are discarded as invalid (e.g. counter rollovers, corrupted files, too few rows) rather than included as zero/negative values. The notebook prints how many runs were skipped per benchmark-guideline pair, if any.

## Step 1 - Normality testing (Shapiro-Wilk)

For each of the 30-run samples (baseline and optimized, separately), a Shapiro-Wilk test (`run_normality_test`) is run to check whether the data is normally distributed. The resulting p-values are stored per pair and exported to `shapiro_energy_results.csv` / `shapiro_results_time.csv`. As expected and reported in the thesis, the large majority of samples violate normality (p ≤ 0.05), which justifies using a non-parametric test in the next step instead of a standard ANOVA.

## Step 2 - Hypothesis testing (ART-ANOVA)

Since the data isn't normal, the baseline and optimized samples are combined, **rank-transformed** (`stats.rankdata`), and compared using an ANOVA on the ranks, this is the Aligned Rank Transform ANOVA (ART-ANOVA) approach:

1. Baseline and optimized values are pooled into one dataframe and labeled by `Group`.
2. The pooled values are converted to ranks (`Ranked_Energy` / equivalent for time).
3. An OLS model (`Ranked_Energy ~ Group`) is fit and an ANOVA table is computed; the p-value for the `Group` term (`ART_ANOVA_p`) tells us whether baseline and optimized medians differ significantly.

## Step 3 - Multiple comparisons correction (Holm-Bonferroni)

Because many benchmark-guideline pairs are tested (136 in total), running each test at α = 0.05 independently would inflate the false-positive rate. A **Holm-Bonferroni correction** (`statsmodels.stats.multitest.multipletests`, method = `"holm"`) is applied across *all* p-values at once, producing `ART_ANOVA_p_holm`. This corrected p-value is what determines the final, reported conclusion for each pair (`Conclusion_corrected`):

- `Significant_after_correction = True` and optimized median < baseline median → **Saves Energy/Time**
- `Significant_after_correction = True` and optimized median > baseline median → **Wastes Energy/Time**
- `Significant_after_correction = False` → **No Statistically Significant Impact**

## Step 4 - Effect size (Cliff's Delta)

Independently of significance, `run_fast_cliffs_delta` computes Cliff's Delta between the optimized and baseline samples, a vectorized implementation that compares every optimized value against every baseline value and averages the sign of the difference. This gives a value between -1 and +1:

- **-1**: every optimized run outperformed every baseline run (strong improvement)
- **+1**: every baseline run outperformed every optimized run (strong regression)
- **~0**: no consistent difference between the two groups

## Aggregation levels

Once every benchmark-guideline pair has been processed into `summary_df`, the notebooks aggregate the results at two additional levels:

1. **Per-guideline summary** - for each guideline (G1...G28), counts how many benchmarks it saved/wasted/had no impact on, and reports the median Cliff's Delta across all its benchmarks. Exported as `guideline_summary_energy_table_rows.tex` / `guideline_summary_time_table_rows.tex`.
2. **Per-family summary** - guidelines are grouped into their families (Code Optimization, Multithreading, Native Code, Function Calls, Network, Other) via the `GUIDELINE_FAMILY` mapping, and the same counts/median delta are computed per family, then ranked from most energy/time-saving to least. Exported as `family_energy_summary_table.csv` / `family_summary_time_table.csv`.

A separate cell in the RQ0 notebook also selects a representative set of 5 benchmarks per guideline (prioritizing the benchmarks tested across the most guidelines) to generate the compact `art_anova_energy_table_rows.tex` used in the main body of the thesis, since the full 136-row table was too long to include in full.

## Guideline → family mapping used throughout

```python
GUIDELINE_FAMILY = {
    'g1': 'Code Optimization', 'g2': 'Code Optimization', 'g3': 'Code Optimization',
    'g4': 'Code Optimization', 'g5': 'Code Optimization', 'g6': 'Code Optimization',
    'g7': 'Code Optimization',
    'g8': 'Multithreading', 'g13': 'Multithreading', 'g25': 'Multithreading',
    'g15': 'Native Code', 'g17': 'Native Code', 'g24': 'Native Code', 'g27': 'Native Code',
    'g18': 'Function Calls', 'g19': 'Function Calls',
    'g23': 'Network',
    'g26': 'Other', 'g28': 'Other',
}
```
