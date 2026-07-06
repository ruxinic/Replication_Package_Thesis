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
    # Get N from the bash script (e.g., 400)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    
    # G6: avoid storing coordinate arrays or an entire NxN results matrix
    # pre-calculate step intervals using the original bounds to avoid allocating arrays
    x_start, x_end = -2.0, 0.5
    y_start, y_end = -1.0, 1.0
    
    x_step = (x_end - x_start) / (N - 1) if N > 1 else 0
    y_step = (y_end - y_start) / (N - 1) if N > 1 else 0

    # G6: track a single running scalar accumulator instead of storing the whole grid in memory
    total_checksum = 0

    for iy in range(N):
        # compute coordinate values dynamically on-the-fly
        y = y_start + iy * y_step
        for ix in range(N):
            x = x_start + ix * x_step
            # aggregate the value directly into the running sum
            total_checksum += m(x + 1j * y)
    print(f"Checksum: {int(total_checksum)}")