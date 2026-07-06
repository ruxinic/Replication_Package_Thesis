import sys
import numpy as np

def m(a):
    z = 0
    for n in range(1, 100):
        z = z**2 + a
        if abs(z) > 2:
            return n
    return 0

if __name__ == "__main__":
    # Get N from the the script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    X = np.linspace(-2, 0.5, N)
    Y = np.linspace(-1, 1, N)
    Z = np.zeros((N, N))

    # G3: caching loop bounds and variables
    # moving NumPy array items into a standard Python list eliminates 
    # array wrapper indexing delays inside the O(N^2) inner iterations
    X_list = X.tolist()
    Y_list = Y.tolist()
    m_cached = m

    for iy in range(N):
        y = Y_list[iy] # G3: take the row coordinate out of the inner loop 
        for ix in range(N):
            Z[iy, ix] = m_cached(X_list[ix] + 1j * y)

    print(f"Checksum: {int(Z.sum())}")