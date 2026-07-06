import sys
import numpy as np

def m(a):
    z = 0
    for n in range(1, 100):
        z = z**2 + a
        if abs(z) > 2:
            return n
    return 0  # Changed from NumPy NaN so the checksum doesn't break

#added/changed from rosetta code
if __name__ == "__main__":
    # Get N from the bash script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    # The original steps were 0.002 and 0.002. To scale with 'N',
    # we calculate the step dynamically based on the website's bounds. it was like this: 
    #X = arange(-2, .5, .002)
    #Y = arange(-1,  1, .002)
    #Z = zeros((len(Y), len(X)))
    
    X = np.linspace(-2, 0.5, N)
    Y = np.linspace(-1, 1, N)
    Z = np.zeros((len(Y), len(X)))

    for iy, y in enumerate(Y):
        for ix, x in enumerate(X):
            Z[iy, ix] = m(x + 1j * y)

    print(f"Checksum: {int(Z.sum())}")