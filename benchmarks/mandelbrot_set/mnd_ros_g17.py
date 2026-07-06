import sys
import numpy as np

# G17: heavy function calls are eliminated from inside the nested loop by 
# refactoring the function to process the entire workload in a single call
def compute_mandelbrot_vectorized(X, Y):
    # broadcast X and Y into a 2D complex plane grid
    # C becomes an NxN matrix of complex numbers (x + 1j * y)
    C = X + 1j * Y[:, np.newaxis]
    
    # initialize Z as an NxN matrix of zeros matching the shape of C
    Z = np.zeros_like(C, dtype=np.complex128)
    
    # initialize the output matrix to track escape iterations
    output = np.zeros(C.shape, dtype=np.int32)
    
    # track which pixels have already escaped (> 2) using a boolean mask matrix
    not_escaped = np.ones(C.shape, bool)
    
    # the loop now runs globally exactly 99 times (instead of N * N * 99 times)
    for n in range(1, 100):
        # only update elements that haven't escaped yet
        Z[not_escaped] = Z[not_escaped]**2 + C[not_escaped]
        
        # create a temporary mask of elements that just crossed the escape threshold
        escaped_this_turn = (np.abs(Z) > 2) & not_escaped
        
        # record the current iteration number for those specific elements
        output[escaped_this_turn] = n
        
        # update the master mask to remove newly escaped elements
        not_escaped[escaped_this_turn] = False
        
    return output

if __name__ == "__main__":
    # Get N from the bash script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    X = np.linspace(-2, 0.5, N)
    Y = np.linspace(-1, 1, N)

    # G17: call the heavy processing logic exactly once instead of N*N times
    Z_matrix = compute_mandelbrot_vectorized(X, Y)

    print(f"Checksum: {int(Z_matrix.sum())}")