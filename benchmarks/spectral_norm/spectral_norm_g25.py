"""G25:

Same power-method algorithm as the baseline, but the matrix A is built and the
matrix-vector products run on the GPU (cuBLAS) -- the G25 treatment. Pure
deterministic float64 math, so the result matches the CPU baseline to within
floating-point rounding (validate by ~6 decimal places, not bit-equality).

A and u are built on the GPU inside the measured region,
so host<->device cost is included. For compute-only, build them beforehand.
"""
import sys
import cupy as cp

def build_A(n):
    i = cp.arange(n).reshape(-1, 1)
    j = cp.arange(n).reshape(1, -1)
    ij = i + j
    return 1.0 / (ij * (ij + 1) / 2.0 + i + 1.0)

def main(n):
    A = build_A(n)
    At = A.T.copy()
    u = cp.ones(n, dtype=cp.float64)
    v = cp.empty_like(u)
    for _ in range(10):
        v = At @ (A @ u)
        u = At @ (A @ v)
    vBv = float(u @ v)
    vv = float(v @ v)
    result = (vBv / vv) ** 0.5
    cp.cuda.Stream.null.synchronize() # required before timer ends
    return result

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    print("{0:.9f}".format(main(n)))