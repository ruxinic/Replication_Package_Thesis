# final_data

This folder contains the complete raw and processed data for the experiment, along with the two Jupyter notebooks used to run the statistical analysis. The notebooks are kept in this same folder because they read the raw `.csv` files directly from the subfolders below via a relative/local path, moving the notebooks elsewhere without the data will break them.

## Structure

Each benchmark has its own folder (e.g. `results-sor`, `results-sparse_mat_mult`, `results-spectral`, `results_richards_g26`, `spectral_norm`, ...). Inside each benchmark folder there are subfolders for the baseline and for every guideline that was applied to it, following the pattern:
<benchmark_folder>/

├── <benchmark>_baseline/     ← 30 raw EnergiBridge .csv files (baseline run)

├── <benchmark>_g<N>/         ← 30 raw EnergiBridge .csv files (optimized run for guideline N)

└── ...                       ← one subfolder per guideline applied to this benchmark

Each `.csv` file is a single EnergiBridge run and contains, among other columns, `PACKAGE_ENERGY (J)` (cumulative energy counter) and `Time` (execution time in milliseconds).

## Important Note

While most folders' name starts with `results_` in this repository, this prefix was avoided in the thesis's tables, and so they reflect only the benchmark's name.
e.g.: `results_lu` -> `lu`.

## Notebooks

- **`data_analysis_RQ0.ipynb`** — processes energy consumption data (RQ0)
- **`data_analysis_RQ1.ipynb`** — processes execution time data (RQ1)

Both notebooks scan every benchmark subfolder above, pair each guideline's runs with its baseline, and run the full statistical pipeline (Shapiro-Wilk → ART-ANOVA → Holm-Bonferroni → Cliff's Delta) described in the thesis. See `STATS_README.md` for details on what each notebook does and how to (re)run them.

## Generated output files

Running the notebooks (re)produces the following files directly in this folder:

| File | Produced by | Content |
|---|---|---|
| `shapiro_energy_results.csv` | RQ0 notebook | Per-benchmark-guideline Shapiro-Wilk p-values (energy) |
| `shapiro_results_time.csv` | RQ1 notebook | Per-benchmark-guideline Shapiro-Wilk p-values (time) |
| `art_anova_energy_table_rows.tex` | RQ0 notebook | LaTeX table rows: ART-ANOVA results per guideline-benchmark pair (energy) |
| `artanova_time_table_rows.tex` | RQ1 notebook | LaTeX table rows: ART-ANOVA results per guideline-benchmark pair (time) |
| `guideline_summary_energy_table_rows.tex` | RQ0 notebook | LaTeX table rows: per-guideline energy summary |
| `guideline_summary_time_table_rows.tex` | RQ1 notebook | LaTeX table rows: per-guideline time summary |
| `family_energy_summary_table.csv` | RQ0 notebook | Per-family energy impact summary |
| `family_summary_time_table.csv` | RQ1 notebook | Per-family time impact summary |

These are the same tables/figures referenced throughout the Results and Discussion sections of the thesis.

## How to reproduce

1. Make sure the notebooks stay in this folder (same level as all the `results-*` / benchmark subfolders).
2. Open `data_analysis_RQ0.ipynb` and `data_analysis_RQ1.ipynb` in Jupyter.
3. Update the `DATA_DIR` path at the top of each notebook's first code cell to point to the local path of this `final_data` folder on your machine.
4. Run all cells top to bottom. Each notebook will print progress, warn about any skipped/invalid runs, and write its output files into this folder.
