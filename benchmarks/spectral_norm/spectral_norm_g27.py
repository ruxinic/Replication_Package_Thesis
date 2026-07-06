import sys
from math import sqrt
import numpy as np # G27: use NumPy for efficient memory structures

def eval_A(i, j):
    ij = i + j
    return 1.0 / (ij * (ij + 1) / 2 + i + 1)

def A_sum(u, i, n):
    x = 0
    # G27: iterate over a contiguous NumPy array
    for j in range(n):
        x += eval_A(i, j) * u[j]
    return x

def At_sum(u, i, n):
    x = 0
    for j in range(n):
        x += eval_A(j, i) * u[j]
    return x

def main():
    n = int(sys.argv[1])
    
    # G27: initialize u and v as NumPy arrays instead of [1] * n
    # allocates a single contiguous block of memory.
    u = np.ones(n, dtype=np.float64)
    v = np.zeros(n, dtype=np.float64)

    for _ in range(10):
        # multiply by A
        tmp = np.array([A_sum(u, i, n) for i in range(n)])
        # multiply by At
        v = np.array([At_sum(tmp, i, n) for i in range(n)])
        
        # repeat to update u
        tmp = np.array([A_sum(v, i, n) for i in range(n)])
        u = np.array([At_sum(tmp, i, n) for i in range(n)])

    # G27: use NumPy's internal math functions to process the dense arrays
    vBv = np.sum(u * v)
    vv = np.sum(v * v)

    print("{0:.9f}".format(sqrt(vBv/vv)))

if __name__ == '__main__':
    main()