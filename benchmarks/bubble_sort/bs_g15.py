from numba import jit
import sys
import random
import numpy as np

# G15: use the @jit to compile the critical sorting logic into native code
@jit(nopython=True)
def bubble_sort_g15(seq):
    n = len(seq)
    changed = True
    while changed:
        changed = False
        for i in range(n - 1):
            if seq[i] > seq[i+1]:
                seq[i], seq[i+1] = seq[i+1], seq[i]
                changed = True
    return seq

def run_benchmark(data):
    # Numba works best with NumPy arrays for efficiency
    filtered_data = np.array([x for x in data if x % 2 == 0])
    return bubble_sort_g15(filtered_data)
#ADDED:
if __name__ == "__main__":
    # N-value from the bash script (e.g., 2000)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    random.seed(42)
    
    # Generate input data
    input_data = [random.randint(1, 1000) for _ in range(N)]
    
    result = run_benchmark(input_data)
    
    print(f"Items sorted: {len(result)}")
    print(f"Checksum: {sum(result)}")