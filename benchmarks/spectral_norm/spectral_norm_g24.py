import sys
import numpy as np
from math import sqrt

def main():
    n = int(sys.argv[1])
    
    # G24: use NumPy arrays for high-performance data structures 
    u = np.ones(n)
    
    # G24: vectorized matrix creation
    i, j = np.ogrid[0:n, 0:n]
    A = 1.0 / ((i + j) * (i + j + 1) / 2 + i + 1)
    At = A.T

    for _ in range(10):
        # G24: high-performance matrix-vector multiplication using @ 
        v = At @ (A @ u)
        u = At @ (A @ v)
    
    # G24: use NumPy's optimized math functions instead of manual loops 
    vBv = np.dot(u, v)
    vv = np.dot(v, v)

    result = sqrt(vBv / vv)
    print("{0:.9f}".format(result))

if __name__ == '__main__':
    main()