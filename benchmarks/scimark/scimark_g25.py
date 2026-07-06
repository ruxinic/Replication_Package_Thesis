"""
G25: offload parallelizable workloads to the GPU.

Kept kernels:
  - lu          : LU factorization with partial pivoting (cuSOLVER on GPU)
  - sparse      : sparse CSR matrix * vector (cuSPARSE on GPU)
  - monte_carlo : Monte Carlo pi estimation (parallel sampling on GPU)

SOR was removed: its in-place stencil is order-dependent (Gauss-Seidel) and a
naive ElementwiseKernel computes a different (Jacobi-like) result in parallel,
so it could not be validated against the sequential SciMark baseline.

VALIDATION NOTES:
  - lu, sparse  : deterministic; GPU result matches the CPU equivalent.
  - monte_carlo : the GPU uses a PARALLEL RNG and cannot reproduce the SciMark
    baseline's sequential custom-RNG stream. Validate by CONVERGENCE to pi
    (|pi_est - 3.14159| within tolerance for the sample count), NOT by equality.

IMPORTANT: this file prints which backend actually ran (GPU vs CPU fallback).
The fallback exists ONLY for local laptop development. For real measurements,
confirm the banner says GPU. Run on the GPU server (glg1, RTX 4090).
"""
import sys
import pyperf as perf

IS_REALLY_GPU = False
try:
    import cupy as cp
    import cupyx.scipy.sparse as csp
    import cupyx.scipy.linalg as cpx_linalg
    cp.cuda.runtime.getDeviceCount() # raises if no usable CUDA device
    _ = cp.cuda.Device(0).attributes # touch the device
    IS_REALLY_GPU = True
except ImportError:
    # CuPy not installed at all -> laptop fallback to NumPy/SciPy (CPU).
    import numpy as cp
    import scipy.sparse as csp
    import scipy.linalg as cpx_linalg
    if not hasattr(cp, "cuda"):
        class _FakeDevice:
            def synchronize(self): pass
        class _FakeCuda:
            def Device(self, _id): return _FakeDevice()
        cp.cuda = _FakeCuda()
except Exception as e:
    # CuPy IS installed but the GPU isn't usable here. Do NOT silently fall
    # back - surface it, so you don't accidentally record CPU data as GPU
    print(f"[FATAL] CuPy present but GPU unusable on this host: {e}", file=sys.stderr)
    print("[HINT ] Run on the GPU server (glg1). For laptop CPU testing, "
          "uninstall cupy so the import fallback engages.", file=sys.stderr)
    raise

_BACKEND = "GPU (CuPy/CUDA)" if IS_REALLY_GPU else "CPU FALLBACK (NumPy/SciPy)"
print(f"[G25 backend] {_BACKEND}", file=sys.stderr)


def _sync():
    if IS_REALLY_GPU:
        cp.cuda.Device(0).synchronize() # block until GPU queue clears


def run_lu_gpu(n, cycles):
    A = cp.random.rand(n, n).astype(cp.float64)
    for _ in range(cycles):
        # CuPy LU lives in cupyx.scipy.linalg (NOT cp.linalg). On the CPU
        # fallback this name resolves to scipy.linalg.lu - same signature.
        P, L, U = cpx_linalg.lu(A)
    _sync()
    return float(U[0, 0]) # touch result so nothing is optimized away


def run_sparse_gpu(N, nz, cycles):
    nr = nz // N
    anz = nr * N
    data = cp.ones(anz, dtype=cp.float64)
    rows = cp.repeat(cp.arange(N, dtype=cp.int32), nr)
    cols = cp.tile(cp.arange(nr, dtype=cp.int32), N)
    A = csp.csr_matrix((data, (rows, cols)), shape=(N, N))
    x = cp.ones(N, dtype=cp.float64)
    y = None
    for _ in range(cycles):
        y = A.dot(x)
    _sync()
    return float(y[0])


_MC_SEED = 113

def run_montecarlo_gpu(num_samples, cycles):
    rng = cp.random.default_rng(_MC_SEED)
    pi_est = 0.0
    for _ in range(cycles):
        x = rng.random(num_samples, dtype=cp.float64)
        y = rng.random(num_samples, dtype=cp.float64)
        inside = (x * x + y * y) <= 1.0 # parallel point-in-circle test
        under_curve = int(cp.count_nonzero(inside))
        pi_est = under_curve / num_samples * 4.0
    _sync()
    return pi_est

def bench_lu(loops, n):
    t0 = perf.perf_counter()
    for _ in range(loops):
        run_lu_gpu(n, 1)
    return perf.perf_counter() - t0


def bench_sparse(loops, N, nz):
    t0 = perf.perf_counter()
    for _ in range(loops):
        run_sparse_gpu(N, nz, 1)
    return perf.perf_counter() - t0


def bench_montecarlo(loops, num_samples):
    t0 = perf.perf_counter()
    for _ in range(loops):
        run_montecarlo_gpu(num_samples, 1)
    return perf.perf_counter() - t0


def add_cmdline_args(cmd, args):
    if args.bench:
        cmd.extend(("--bench", args.bench))


if __name__ == "__main__":
    runner = perf.Runner(add_cmdline_args=add_cmdline_args)
    runner.argparser.add_argument(
        "--bench",
        choices=["lu", "sparse", "monte_carlo"],
        default="lu",
        help="Which GPU-accelerated benchmark kernel to run",
    )
    args = runner.parse_args()

    if args.bench == "lu":
        runner.bench_time_func("g25_lu", bench_lu, 256)
    elif args.bench == "sparse":
        runner.bench_time_func("g25_sparse", bench_sparse, 1000, 10000)
    elif args.bench == "monte_carlo":
        runner.bench_time_func("g25_monte_carlo", bench_montecarlo, 1000000)