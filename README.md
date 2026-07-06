# Towards Energy-Aware Coding for Python-based Applications - Replication Package

This repository contains the full replication package for the BSc thesis *"Towards Energy-Aware Coding for Python-based Applications"* (Ruxandra-Maria Nicu, Vrije Universiteit Amsterdam). The study empirically evaluates the impact of 19 Python optimization guidelines, drawn from 6 families, on both **energy consumption** (RQ0) and **execution time** (RQ1), across 26 benchmarks and ~4000 measured runs.

Each guideline was applied to at least 5 benchmarks, executed 30 times per version (baseline and optimized) on a dedicated remote server, and measured using [EnergiBridge](https://github.com/tdurieux/EnergiBridge). Results were analyzed with Shapiro-Wilk, ART-ANOVA, Holm-Bonferroni correction, and Cliff's Delta.

## Repository structure

| Folder | Description |
|---|---|
| [`benchmarks/`](./benchmarks/README.md) | Source code for every benchmark used in the experiment (baseline + optimized versions per guideline), extracted from the Benchmarks Game, PyPerformance, and Rosetta Code, plus custom-written benchmarks where no suitable published one existed. See the folder's own README for details on sourcing, modifications, and documentation conventions. |
| [`final_data/`](./final_data/README.md) | All raw EnergiBridge `.csv` output files from the all experiment runs, organized per benchmark/guideline, together with the Jupyter notebooks (`data_analysis_RQ0.ipynb`, `data_analysis_RQ1.ipynb`) used to run the statistical pipeline and produce the tables reported in the thesis. See `STATS_README.md` inside this folder for a full walkthrough of the statistical analysis. |
| `boxplot_generation/` | Scripts used to generate the box-plot visualizations of energy/time results (baseline vs. optimized) shown in the thesis. |
| `mock_testing/` | Non-complex scripts used to validate each guideline's implementation before running the full-scale experiment. |
| `run_server/` | Scripts used to execute the benchmarks on the remote servers and collect measurements via EnergiBridge (see its own README for usage instructions). |

## How the pieces fit together

1. **`benchmarks/`** - the code that was actually executed and measured.
2. **`run_server/`** - the scripts that ran that code on the remote servers, 30 times per baseline/guideline version, and collected raw EnergiBridge output.
3. **`final_data/`** - where all the raw `.csv` output from those runs lives, plus the notebooks that turn it into the statistical results (Shapiro-Wilk, ART-ANOVA, Holm-Bonferroni, Cliff's Delta) reported in the thesis.
4. **`boxplot_generation/`** - turns the same data into the box-plot figures used throughout the Results section.
5. **`mock_testing/`** - earlier, smaller-scale runs used to check that each guideline's optimized version behaved correctly before committing to the full 30-run experiment.

## Guideline families

| Family | Guidelines |
|---|---|
| Code Optimization | G1–G7 |
| Multithreading | G8, G13, G25 |
| Native Code | G15, G17, G24, G27 |
| Function Calls | G18, G19 |
| Network | G23 |
| Other | G26, G28 |

*(Object Orientation was part of the original taxonomy but excluded from this study due to insufficient supporting literature.)*

## Requirements

- Python 3.13 (see individual benchmark folders for any additional per-benchmark dependencies, e.g. Numba, Cython, NumPy/SciPy, Polars)
- [EnergiBridge](https://github.com/tdurieux/EnergiBridge) for energy/time measurement
- Jupyter, `pandas`, `numpy`, `scipy`, `statsmodels` for the data analysis notebooks in `final_data/`

## Author

Ruxandra-Maria Nicu,
Vrije Universiteit Amsterdam · r.nicu@student.vu.nl
