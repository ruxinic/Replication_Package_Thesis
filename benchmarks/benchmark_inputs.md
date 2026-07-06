# Benchmark Input Parameters

This file documents the input parameters used when running each benchmark during the experiments. If a benchmark is not listed below, it does not require any input value.

| Benchmark | Input Parameters |
|---|---|
| *Spectral Norm* | 500 |
| *N-Body* | 100000 |
| *Mandelbrot Set* | 700 |
| *Mandelbrot Set - G25* | 6000 |
| *Bubble Sort* | 25000 |
| *Django* | 2000 |
| *Binary Trees* | 23 |
| *Sieves of Eratosthenes* | 100000000 |
| *Scimark SOR* | `'sor': (bench_SOR, 100, 10, Array2D)` |
| *Scimark Sparse Mat Mult* | `'sparse_mat_mult': (bench_SparseMatMult, 50000, 1000000)` |
| *Scimark Monte Carlo* | `'monte_carlo': (bench_MonteCarlo, 1000000)` |
| *Scimark LU* | `'lu': (bench_LU, 256)` |
| *Scimark FFT* | `'fft': (bench_FFT, 16384, 7)` |
| *Insertion Sort* | 10000, 'semi-sorted' |
| *Selection Sort* | 30000, 'semi-sorted' |
| *Merge Sort* | 9000000, 'semi-sorted' |
| *Short Circuit Evaluation* | 50000000 |
