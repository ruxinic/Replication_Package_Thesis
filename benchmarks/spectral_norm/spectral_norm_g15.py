import numpy as np
from numba import njit, prange
from math import sqrt
from sys import argv

# G15: add @njit
@njit(fastmath=True, cache=True)
def eval_A(i, j):
    ij = i + j
    return 1.0 / (ij * (ij + 1) / 2 + i + 1)

# G15: parallel compiled loop; releases the GIL and 
# executes critical sections in a multi-threaded compiled environment
@njit(parallel=True, fastmath=True)
def A_sum(n, u, out):
    for i in prange(n):
        s = 0.0
        for j in range(n):
            s += eval_A(i, j) * u[j]
        out[i] = s

@njit(parallel=True, fastmath=True)
def At_sum(n, u, out):
    for i in prange(n):
        s = 0.0
        for j in range(n):
            s += eval_A(j, i) * u[j]
        out[i] = s

def main():
    n = int(argv[1])
    
    # G15: use NumPy arrays for direct memory access by compiled code
    u = np.ones(n, dtype=np.float64)
    v = np.empty(n, dtype=np.float64)
    tmp = np.empty(n, dtype=np.float64)

    for _ in range(10):
        # A_sum and At_sum - compiled machine-code functions
        A_sum(n, u, tmp)
        At_sum(n, tmp, v)
        A_sum(n, v, tmp)
        At_sum(n, tmp, u)

    # performance-critical reduction handled by compiled NumPy methods
    vBv = np.dot(u, v)
    vv = np.dot(v, v)

    print("{0:.9f}".format(sqrt(vBv / vv)))

if __name__ == '__main__':
    main()