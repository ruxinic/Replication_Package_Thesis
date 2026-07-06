import numpy as np
from scipy.sparse import csr_matrix
from scipy.linalg import lu_factor
import pyperf as perf


def MonteCarlo(Num_samples):
    rng = np.random.default_rng(113)
    points = rng.random((Num_samples, 2))
    dist_sq = np.sum(np.square(points), axis=1)
    under_curve = np.count_nonzero(dist_sq <= 1.0)
    return (under_curve / Num_samples) * 4.0

def SparseMatMult_logic(A, x):
    return A.dot(x)

def LU_factor_logic(A):
    # lu_factor modifies in-place or returns LU depending on SciPy version
    return lu_factor(A)

def SOR_execute(omega, G, cycles):
    # use vectorized slicing
    # pre-calculate constants outside the loop
    inv_omega = 1.0 - omega
    quarter_omega = 0.25 * omega
    
    for _ in range(cycles):
        # stencil operation: (Top + Bottom + Left + Right)
        # vectorized slices allow C-level execution speed
        res = (G[:-2, 1:-1] + G[2:, 1:-1] + 
               G[1:-1, :-2] + G[1:-1, 2:])
        
        # update interior points
        G[1:-1, 1:-1] = (inv_omega * G[1:-1, 1:-1]) + (quarter_omega * res)

def bench_SOR(loops, n, cycles):
    t0 = perf.perf_counter()
    for _ in range(loops):
        # Create a zero-filled N x N grid
        G = np.zeros((n, n), dtype=np.float64)
        SOR_execute(1.25, G, cycles)
    return perf.perf_counter() - t0


def bench_SparseMatMult(cycles, N, nz):
    # G24: use SciPy's CSR format
    rng = np.random.default_rng(42) # consistent seeding
    
    val = rng.random(nz)
    col = rng.integers(0, N, nz)
    row = np.sort(rng.integers(0, nz, N + 1))
    row[0], row[-1] = 0, nz
    
    A = csr_matrix((val, col, row), shape=(N, N))
    x = rng.random(N)
    
    t0 = perf.perf_counter()
    for _ in range(cycles):
        # A.dot(x) invokes optimized BLAS-like sparse kernels
        y = A.dot(x)
    return perf.perf_counter() - t0


def bench_MonteCarlo(loops, Num_samples):
    # Monte Carlo Pi estimation using batch random generation
    rng = np.random.default_rng(113)
    t0 = perf.perf_counter()
    for _ in range(loops):
        # generate all X and Y coordinates at once 
        points = rng.random((Num_samples, 2))
        # square values and sum horizontally: x^2 + y^2
        dist_sq = np.sum(np.square(points), axis=1)
        # fast boolean counting
        under_curve = np.count_nonzero(dist_sq <= 1.0)
        _pi = (under_curve / Num_samples) * 4.0
    return perf.perf_counter() - t0


def bench_LU(cycles, N):
    # G24: use SciPy LAPACK wrappers
    rng = np.random.default_rng(7)
    # original matrix to copy from (to ensure each cycle starts fresh)
    A_init = rng.random((N, N))
    
    t0 = perf.perf_counter()
    for _ in range(cycles):
        # copy to avoid factorizing an already factorized matrix
        A = A_init.copy()
        # lu_factor uses standard LAPACK dgetrf
        lu_factor(A)
    return perf.perf_counter() - t0


def bench_FFT(loops, N, cycles):
    # G24: use NumPy's Fast Fourier Transform (FFTW-style)
    rng = np.random.default_rng(7)
    # create a complex vector (interleaved real/imaginary equivalent)
    data = rng.random(N) + 1j * rng.random(N)
    
    t0 = perf.perf_counter()
    for _ in range(loops):
        x = data.copy()
        for _ in range(cycles):
            # Llibrary calls replace hundreds of lines of bit-reversal logic
            x = np.fft.fft(x)
            x = np.fft.ifft(x)
    return perf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    if args.benchmark:
        cmd.append(args.benchmark)

BENCHMARKS = {
    'sor': (bench_SOR, 100, 10),
    'sparse_mat_mult': (bench_SparseMatMult, 50000, 1000000),
    'monte_carlo': (bench_MonteCarlo, 1000000),
    'lu': (bench_LU, 256),
    'fft': (bench_FFT, 16384, 7),
}

if __name__ == "__main__":
    runner = perf.Runner(add_cmdline_args=add_cmdline_args)
    runner.argparser.add_argument("benchmark", nargs='?',
                                  choices=sorted(BENCHMARKS))

    args = runner.parse_args()
    bench_names = (args.benchmark,) if args.benchmark else sorted(BENCHMARKS)

    for name in bench_names:
        func_args = BENCHMARKS[name]
        runner.bench_time_func(f'scimark_g24_{name}', *func_args)