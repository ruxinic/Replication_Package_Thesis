import sys
import numpy as np
import numba

# G15: compile the performance-critical scalar math function with @njit
@numba.njit
def m(a):
    z = 0.0 + 0.0j  # declare initial z as a complex float type
    for n in range(1, 100):
        z = z**2 + a
        if abs(z) > 2.0:
            return n
    return 0

# G15: compile the nested loop execution to fully bypass interpreter loop overhead
@numba.njit
def compute_mandelbrot_grid(X, Y, Z):
    for iy in range(len(Y)):
        y = Y[iy]
        for ix in range(len(X)):
            x = X[ix]
            Z[iy, ix] = m(x + 1j * y)
    return Z

if __name__ == "__main__":
    # Get N from the bash script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    X = np.linspace(-2.0, 0.5, N)
    Y = np.linspace(-1.0, 1.0, N)
    Z = np.zeros((len(Y), len(X)), dtype=np.int32)

    Z = compute_mandelbrot_grid(X, Y, Z)
    print(f"Checksum: {int(Z.sum())}")