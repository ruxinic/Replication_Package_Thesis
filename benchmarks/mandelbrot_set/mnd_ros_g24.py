import sys
import numpy as np

def mandelbrot_hpc_numpy(N):
    # G24: use high-performance library operations to build a coordinate matrix.
    # np.linspace constructs memory-contiguous arrays optimized for vector pipelines
    X = np.linspace(-2, 0.5, N)
    Y = np.linspace(-1, 1, N)
    
    # G24: broadcast 1D arrays into a 2D complex plane grid using high-performance indexing
    C = X + 1j * Y[:, np.newaxis]
    
    # pre-allocate tracking matrices using optimized native NumPy types
    Z = np.zeros_like(C, dtype=np.complex128)
    output = np.zeros(C.shape, dtype=np.int32)
    not_escaped = np.ones(C.shape, dtype=bool)
    
    # G24: perform the computationally intensive Mandelbrot evaluations as bulk matrix operations
    for n in range(1, 100):
        # math is calculated across the entire grid simultaneously using NumPy's C-compiled backend
        Z[not_escaped] = Z[not_escaped]**2 + C[not_escaped]
        
        # pointwise magnitude evaluations are calculated using NumPy's internal vector math
        escaped_this_turn = (np.abs(Z) > 2) & not_escaped
        output[escaped_this_turn] = n
        not_escaped[escaped_this_turn] = False
        
    return output

if __name__ == "__main__":
    # Get N from the bash script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    # G24: invoke high-performance computing matrix function
    Z_matrix = mandelbrot_hpc_numpy(N)

    # G24: use NumPy's highly optimized, multi-threaded .sum() reduction method 
    # instead of a slow native Python iterative sum loop
    print(f"Checksum: {int(Z_matrix.sum())}")