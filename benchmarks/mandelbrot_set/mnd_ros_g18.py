from functools import lru_cache
import sys
import numpy as np

# G18: add @lru_cache
@lru_cache(maxsize=1024) 
def m(a):
    z = 0
    for n in range(1, 100):
        z = z**2 + a
        if abs(z) > 2:
            return n
    return 0  # Changed from NumPy NaN so checksum doesn't break

if __name__ == "__main__":
    # Get N from your bash script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    X = np.linspace(-2, 0.5, N)
    Y = np.linspace(-1, 1, N)
    Z = np.zeros((len(Y), len(X)))

    for iy, y in enumerate(Y):
        for ix, x in enumerate(X):
            Z[iy, ix] = m(x + 1j * y)

    print(f"Checksum: {int(Z.sum())}")