# Benchmarks

This folder contains all the benchmarks used to evaluate the 19 optimization guidelines discussed in the thesis. Each subfolder corresponds to one benchmark and contains its baseline version along with the optimized version(s) produced by applying the relevant guideline(s).

## Folder structure

| Folder | Benchmark |
|---|---|
| `binary-trees` | Binary Trees |
| `bubble_sort` | Bubble Sort |
| `django` | Django |
| `mandelbrot_set` | Mandelbrot Set |
| `n-body` | N-Body |
| `richards` | Richards 
| `richards_g26` | Richards changed to fit G26|
| `scimark` | Scimark (fft, lu, sor, monte_carlo, sparse_mat_mult) |
| `sieves` | Sieve of Eratosthenes |
| `spectral_norm` | Spectral Norm |
| `test_g2` | Insertion Sort, Selection Sort, Merge Sort |
| `test_g4` | Log Processing, Network, Short Circ Eval, README |
| `test_g5` | Pi, Roots of a Function |
| `test_g13` | Concurrent Worker Sync, Disk, Hot Flag, Polling, Sleep Block, README|

## Source of the benchmarks

The benchmarks were extracted from three sources:

- **[The Benchmarks Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)**
- **[PyPerformance](https://github.com/python/pyperformance)**
- **[Rosetta Code](https://rosettacode.org/)**

For a few guidelines, no suitable published benchmark could be found, so custom benchmarks were written from scratch. This applies to `test_g4`, and `test_g13`, since these guidelines target very specific coding patterns (e.g. short-circuit evaluation, approximation of computations, sleep-on-wait behavior) that are hard to isolate in existing benchmark suites.

## Modifications to Rosetta Code benchmarks

The benchmarks sourced from Rosetta Code were adapted from their original form. Since Rosetta Code snippets are typically small code fragments rather than runnable programs, we added the structural elements needed to actually execute and measure them, such as:

- a `main` function / entry point
- the ability to pass in input parameters, so the workload size can be adjusted per run

These additions do not change the algorithmic logic of the original snippet - they only make it runnable and configurable for our experiments.

## Documentation conventions

Changes made to the code are mostly commented directly in the source files. This includes:

- structural changes made to the **baseline** (e.g. added `main` function, input parameter handling, for benchmarks sourced from Rosetta Code)
- the actual **optimization** applied for each guideline, with a comment marking what was changed

This means each file is self-documenting: reading the comments in a given benchmark folder should be enough to understand exactly what was modified between the baseline and the optimized versions.

## Input parameters

The input parameters used for each benchmark during testing are documented separately in [`benchmark_inputs.md`](./benchmark_inputs.md), which lists, per benchmark, the exact parameters/arguments used to run the experiments.
